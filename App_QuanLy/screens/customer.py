from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView
)

from database.database import get_connection


class CustomerWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Quản lý khách hàng")
        self.resize(1000, 650)

        self.create_ui()
        self.load_customers()

    # ==================================================
    # GIAO DIỆN
    # ==================================================

    def create_ui(self):

        main_layout = QVBoxLayout()

        # ==============================
        # TIÊU ĐỀ
        # ==============================

        title = QLabel("👤 QUẢN LÝ KHÁCH HÀNG")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                padding: 15px;
            }
        """)

        main_layout.addWidget(title)

        # ==============================
        # TÌM KIẾM
        # ==============================

        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Nhập tên hoặc số điện thoại khách hàng..."
        )

        search_button = QPushButton("🔍 Tìm kiếm")
        search_button.clicked.connect(self.search_customers)

        refresh_button = QPushButton("🔄 Làm mới")
        refresh_button.clicked.connect(self.load_customers)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        search_layout.addWidget(refresh_button)

        main_layout.addLayout(search_layout)

        # ==============================
        # THÔNG TIN KHÁCH HÀNG
        # ==============================

        form_layout = QVBoxLayout()

        name_layout = QHBoxLayout()

        name_label = QLabel("Họ tên:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nhập họ tên khách hàng")

        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)

        phone_layout = QHBoxLayout()

        phone_label = QLabel("Số điện thoại:")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Nhập số điện thoại")

        phone_layout.addWidget(phone_label)
        phone_layout.addWidget(self.phone_input)

        address_layout = QHBoxLayout()

        address_label = QLabel("Địa chỉ:")
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Nhập địa chỉ")

        address_layout.addWidget(address_label)
        address_layout.addWidget(self.address_input)

        note_layout = QHBoxLayout()

        note_label = QLabel("Ghi chú:")
        self.note_input = QLineEdit()
        self.note_input.setPlaceholderText("Nhập ghi chú")

        note_layout.addWidget(note_label)
        note_layout.addWidget(self.note_input)

        form_layout.addLayout(name_layout)
        form_layout.addLayout(phone_layout)
        form_layout.addLayout(address_layout)
        form_layout.addLayout(note_layout)

        main_layout.addLayout(form_layout)

        # ==============================
        # NÚT CHỨC NĂNG
        # ==============================

        button_layout = QHBoxLayout()

        add_button = QPushButton("➕ Thêm")
        add_button.clicked.connect(self.add_customer)

        edit_button = QPushButton("✏️ Sửa")
        edit_button.clicked.connect(self.edit_customer)

        delete_button = QPushButton("🗑️ Xóa")
        delete_button.clicked.connect(self.delete_customer)

        clear_button = QPushButton("🧹 Xóa nhập")
        clear_button.clicked.connect(self.clear_form)

        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(clear_button)

        main_layout.addLayout(button_layout)

        # ==============================
        # BẢNG KHÁCH HÀNG
        # ==============================

        self.table = QTableWidget()

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Họ tên",
            "Số điện thoại",
            "Địa chỉ",
            "Ghi chú"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.table.cellClicked.connect(
            self.select_customer
        )

        main_layout.addWidget(self.table)

        # ==============================
        # NÚT ĐÓNG
        # ==============================

        close_button = QPushButton("❌ Đóng")

        close_button.clicked.connect(
            self.close
        )

        main_layout.addWidget(close_button)

        self.setLayout(main_layout)

    # ==================================================
    # HIỂN THỊ KHÁCH HÀNG
    # ==================================================

    def load_customers(self):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, name, phone, address, note
            FROM customers
            ORDER BY id DESC
        """)

        customers = cursor.fetchall()

        connection.close()

        self.display_customers(customers)

    # ==================================================
    # HIỂN THỊ DỮ LIỆU LÊN BẢNG
    # ==================================================

    def display_customers(self, customers):

        self.table.setRowCount(0)

        for row_data in customers:

            row = self.table.rowCount()

            self.table.insertRow(row)

            for column, value in enumerate(row_data):

                item = QTableWidgetItem(
                    "" if value is None else str(value)
                )

                self.table.setItem(
                    row,
                    column,
                    item
                )

    # ==================================================
    # TÌM KIẾM
    # ==================================================

    def search_customers(self):

        keyword = self.search_input.text().strip()

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, name, phone, address, note
            FROM customers
            WHERE name LIKE ?
               OR phone LIKE ?
            ORDER BY id DESC
        """, (
            f"%{keyword}%",
            f"%{keyword}%"
        ))

        customers = cursor.fetchall()

        connection.close()

        self.display_customers(customers)

    # ==================================================
    # THÊM KHÁCH HÀNG
    # ==================================================

    def add_customer(self):

        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        address = self.address_input.text().strip()
        note = self.note_input.text().strip()

        if not name:

            QMessageBox.warning(
                self,
                "Thông báo",
                "Vui lòng nhập họ tên khách hàng!"
            )

            return

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO customers
            (
                name,
                phone,
                address,
                note
            )
            VALUES (?, ?, ?, ?)
        """, (
            name,
            phone,
            address,
            note
        ))

        connection.commit()
        connection.close()

        QMessageBox.information(
            self,
            "Thành công",
            "Đã thêm khách hàng!"
        )

        self.clear_form()
        self.load_customers()

    # ==================================================
    # CHỌN KHÁCH HÀNG
    # ==================================================

    def select_customer(self, row, column):

        self.name_input.setText(
            self.table.item(row, 1).text()
        )

        self.phone_input.setText(
            self.table.item(row, 2).text()
        )

        self.address_input.setText(
            self.table.item(row, 3).text()
        )

        self.note_input.setText(
            self.table.item(row, 4).text()
        )

    # ==================================================
    # LẤY ID KHÁCH HÀNG ĐANG CHỌN
    # ==================================================

    def get_selected_id(self):

        row = self.table.currentRow()

        if row < 0:

            return None

        return int(
            self.table.item(row, 0).text()
        )

    # ==================================================
    # SỬA KHÁCH HÀNG
    # ==================================================

    def edit_customer(self):

        customer_id = self.get_selected_id()

        if customer_id is None:

            QMessageBox.warning(
                self,
                "Thông báo",
                "Vui lòng chọn khách hàng cần sửa!"
            )

            return

        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        address = self.address_input.text().strip()
        note = self.note_input.text().strip()

        if not name:

            QMessageBox.warning(
                self,
                "Thông báo",
                "Vui lòng nhập họ tên khách hàng!"
            )

            return

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE customers
            SET
                name = ?,
                phone = ?,
                address = ?,
                note = ?
            WHERE id = ?
        """, (
            name,
            phone,
            address,
            note,
            customer_id
        ))

        connection.commit()
        connection.close()

        QMessageBox.information(
            self,
            "Thành công",
            "Đã cập nhật khách hàng!"
        )

        self.clear_form()
        self.load_customers()

    # ==================================================
    # XÓA KHÁCH HÀNG
    # ==================================================

    def delete_customer(self):

        customer_id = self.get_selected_id()

        if customer_id is None:

            QMessageBox.warning(
                self,
                "Thông báo",
                "Vui lòng chọn khách hàng cần xóa!"
            )

            return

        answer = QMessageBox.question(
            self,
            "Xác nhận",
            "Bạn có chắc muốn xóa khách hàng này?",
            QMessageBox.Yes | QMessageBox.No
        )

        if answer != QMessageBox.Yes:

            return

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM customers
            WHERE id = ?
        """, (customer_id,))

        connection.commit()
        connection.close()

        QMessageBox.information(
            self,
            "Thành công",
            "Đã xóa khách hàng!"
        )

        self.clear_form()
        self.load_customers()

    # ==================================================
    # XÓA FORM
    # ==================================================

    def clear_form(self):

        self.name_input.clear()
        self.phone_input.clear()
        self.address_input.clear()
        self.note_input.clear()

        self.table.clearSelection()


if __name__ == "__main__":

    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    window = CustomerWindow()
    window.show()

    sys.exit(app.exec())