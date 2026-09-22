from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QComboBox,
    QSpinBox,
    QGroupBox,
    QFormLayout
)

from PySide6.QtCore import Qt
from datetime import datetime

from database.database import get_connection


class StockImportWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Nhập thuốc"
        )

        self.setMinimumSize(
            950,
            650
        )

        self.create_ui()

        self.load_medicines()
        self.load_imports()

    # ==================================================
    # GIAO DIỆN
    # ==================================================

    def create_ui(self):

        # =========================
        # TIÊU ĐỀ
        # =========================

        title = QLabel(
            "📦 NHẬP THUỐC"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            padding: 15px;
        """)

        # =========================
        # NHÓM NHẬP THUỐC
        # =========================

        import_group = QGroupBox(
            "📦 Thông tin nhập thuốc"
        )

        form_layout = QFormLayout()

        # =========================
        # CHỌN THUỐC
        # =========================

        self.medicine_combo = QComboBox()

        self.medicine_combo.setMinimumHeight(
            38
        )

        form_layout.addRow(
            "Tên thuốc:",
            self.medicine_combo
        )

        # =========================
        # SỐ LƯỢNG
        # =========================

        self.quantity_spin = QSpinBox()

        self.quantity_spin.setMinimum(
            1
        )

        self.quantity_spin.setMaximum(
            100000
        )

        self.quantity_spin.setValue(
            1
        )

        self.quantity_spin.setMinimumHeight(
            38
        )

        form_layout.addRow(
            "Số lượng nhập:",
            self.quantity_spin
        )

        import_group.setLayout(
            form_layout
        )

        # =========================
        # NÚT NHẬP THUỐC
        # =========================

        import_button = QPushButton(
            "📦 Nhập thuốc"
        )

        import_button.setMinimumHeight(
            42
        )

        import_button.clicked.connect(
            self.import_medicine
        )

        # =========================
        # NÚT LÀM MỚI
        # =========================

        refresh_button = QPushButton(
            "🔄 Làm mới"
        )

        refresh_button.setMinimumHeight(
            42
        )

        refresh_button.clicked.connect(
            self.refresh_data
        )

        # =========================
        # NÚT ĐÓNG
        # =========================

        close_button = QPushButton(
            "❌ Đóng"
        )

        close_button.setMinimumHeight(
            42
        )

        close_button.clicked.connect(
            self.close
        )

        # =========================
        # KHU VỰC NÚT
        # =========================

        button_layout = QHBoxLayout()

        button_layout.addWidget(
            import_button
        )

        button_layout.addWidget(
            refresh_button
        )

        button_layout.addWidget(
            close_button
        )

        # =========================
        # TIÊU ĐỀ LỊCH SỬ
        # =========================

        history_title = QLabel(
            "📋 LỊCH SỬ NHẬP THUỐC"
        )

        history_title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            padding: 10px 0px;
        """)

        # =========================
        # BẢNG LỊCH SỬ
        # =========================

        self.table = QTableWidget()

        self.table.setColumnCount(
            5
        )

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Tên thuốc",
            "Loại",
            "Số lượng nhập",
            "Ngày giờ nhập"
        ])

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        # =========================
        # LAYOUT CHÍNH
        # =========================

        layout = QVBoxLayout()

        layout.addWidget(
            title
        )

        layout.addWidget(
            import_group
        )

        layout.addLayout(
            button_layout
        )

        layout.addWidget(
            history_title
        )

        layout.addWidget(
            self.table
        )

        self.setLayout(
            layout
        )

    # ==================================================
    # TẢI DANH SÁCH THUỐC
    # ==================================================

    def load_medicines(self):

        self.medicine_combo.clear()

        connection = get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute("""
                SELECT
                    id,
                    name,
                    category,
                    quantity
                FROM medicines
                ORDER BY name ASC
            """)

            medicines = cursor.fetchall()

            for medicine in medicines:

                medicine_id = medicine[0]
                name = medicine[1]
                category = medicine[2] or ""
                quantity = medicine[3] or 0

                text = (
                    f"{name} "
                    f"({category}) "
                    f"- Tồn kho: {quantity}"
                )

                self.medicine_combo.addItem(
                    text,
                    medicine_id
                )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Lỗi",
                "Không thể tải danh sách thuốc!\n\n"
                f"{error}"
            )

        finally:

            connection.close()

    # ==================================================
    # NHẬP THUỐC
    # ==================================================

    def import_medicine(self):

        medicine_id = self.medicine_combo.currentData()

        if medicine_id is None:

            QMessageBox.warning(
                self,
                "Thông báo",
                "Vui lòng chọn thuốc!"
            )

            return

        quantity = self.quantity_spin.value()

        if quantity <= 0:

            QMessageBox.warning(
                self,
                "Thông báo",
                "Số lượng nhập phải lớn hơn 0!"
            )

            return

        connection = get_connection()

        cursor = connection.cursor()

        try:

            # =========================
            # KIỂM TRA THUỐC
            # =========================

            cursor.execute("""
                SELECT
                    id,
                    name,
                    quantity
                FROM medicines
                WHERE id = ?
            """, (medicine_id,))

            medicine = cursor.fetchone()

            if medicine is None:

                QMessageBox.warning(
                    self,
                    "Thông báo",
                    "Không tìm thấy thuốc!"
                )

                connection.close()

                return

            medicine_name = medicine[1]
            old_quantity = medicine[2] or 0

            new_quantity = (
                old_quantity + quantity
            )

            # =========================
            # CẬP NHẬT TỒN KHO
            # =========================

            cursor.execute("""
                UPDATE medicines
                SET quantity = ?
                WHERE id = ?
            """, (
                new_quantity,
                medicine_id
            ))

            # =========================
            # LƯU LỊCH SỬ NHẬP
            # =========================

            imported_at = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            cursor.execute("""
                INSERT INTO stock_imports
                (
                    medicine_id,
                    quantity,
                    imported_at
                )
                VALUES (?, ?, ?)
            """, (
                medicine_id,
                quantity,
                imported_at
            ))

            connection.commit()

            QMessageBox.information(
                self,
                "Thành công",
                f"Đã nhập thuốc thành công!\n\n"
                f"Thuốc: {medicine_name}\n"
                f"Số lượng nhập: {quantity}\n"
                f"Tồn kho cũ: {old_quantity}\n"
                f"Tồn kho mới: {new_quantity}"
            )

            # =========================
            # CẬP NHẬT GIAO DIỆN
            # =========================

            self.load_medicines()

            self.load_imports()

            self.quantity_spin.setValue(
                1
            )

        except Exception as error:

            connection.rollback()

            QMessageBox.critical(
                self,
                "Lỗi",
                "Không thể nhập thuốc!\n\n"
                f"{error}"
            )

        finally:

            connection.close()

    # ==================================================
    # TẢI LỊCH SỬ NHẬP THUỐC
    # ==================================================

    def load_imports(self):

        connection = get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute("""
                SELECT
                    stock_imports.id,
                    medicines.name,
                    medicines.category,
                    stock_imports.quantity,
                    stock_imports.imported_at
                FROM stock_imports

                LEFT JOIN medicines
                ON stock_imports.medicine_id = medicines.id

                ORDER BY stock_imports.id DESC
            """)

            imports = cursor.fetchall()

            self.table.setRowCount(
                len(imports)
            )

            for row, item_data in enumerate(
                imports
            ):

                for column, value in enumerate(
                    item_data
                ):

                    if value is None:
                        value = ""

                    item = QTableWidgetItem(
                        str(value)
                    )

                    self.table.setItem(
                        row,
                        column,
                        item
                    )

            # =========================
            # CĂN GIỮA
            # =========================

            for row in range(
                self.table.rowCount()
            ):

                for column in [
                    0,
                    3,
                    4
                ]:

                    item = self.table.item(
                        row,
                        column
                    )

                    if item:

                        item.setTextAlignment(
                            Qt.AlignCenter
                        )

            # =========================
            # ĐIỀU CHỈNH CỘT
            # =========================

            self.table.resizeColumnsToContents()

            self.table.setColumnWidth(
                1,
                250
            )

            self.table.setColumnWidth(
                2,
                180
            )

            self.table.setColumnWidth(
                3,
                150
            )

            self.table.setColumnWidth(
                4,
                200
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Lỗi",
                "Không thể tải lịch sử nhập thuốc!\n\n"
                f"{error}"
            )

        finally:

            connection.close()

    # ==================================================
    # LÀM MỚI
    # ==================================================

    def refresh_data(self):

        self.load_medicines()

        self.load_imports()

    # ==================================================
    # CHẠY THỬ FILE
    # ==================================================

if __name__ == "__main__":

    import sys

    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    window = StockImportWindow()

    window.show()

    sys.exit(app.exec())