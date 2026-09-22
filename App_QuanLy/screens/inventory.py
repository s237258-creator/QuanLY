from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QFrame,
    QMessageBox
)

from PySide6.QtCore import Qt

from database.database import get_connection

from datetime import datetime, date


class InventoryWindow(QWidget):

    def __init__(self):
        super().__init__()

        # ==================================================
        # CẤU HÌNH CỬA SỔ
        # ==================================================

        self.setWindowTitle(
            "Nhà thuốc Ý Như - Quản lý kho"
        )

        self.setMinimumSize(
            1150,
            720
        )

        # ==================================================
        # STYLE
        # ==================================================

        self.setStyleSheet("""

            QWidget {
                font-family: "Segoe UI";
            }

            QLabel#pageTitle {
                color: #0F766E;
                font-size: 27px;
                font-weight: bold;
                background-color: transparent;
            }

            QLabel#pageSubtitle {
                color: #6B7280;
                font-size: 13px;
                background-color: transparent;
            }

            QFrame#panel {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
            }

            QFrame#statCard {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 10px;
            }

            QFrame#statCard:hover {
                border: 1px solid #14B8A6;
            }

            QLabel#statIcon {
                background-color: #ECFDF5;
                color: #0F766E;
                border-radius: 8px;
                font-size: 19px;
            }

            QLabel#statTitle {
                color: #6B7280;
                background-color: transparent;
                font-size: 10px;
                font-weight: bold;
            }

            QLabel#statValue {
                color: #111827;
                background-color: transparent;
                font-size: 19px;
                font-weight: bold;
            }

            QLabel#searchLabel {
                color: #374151;
                background-color: transparent;
                font-weight: bold;
            }

            QLineEdit {
                background-color: #F9FAFB;
                color: #1F2937;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 7px 12px;
                min-height: 20px;
            }

            QLineEdit:focus {
                background-color: white;
                border: 2px solid #14B8A6;
            }

            QPushButton {
                background-color: white;
                color: #374151;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 7px 14px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #ECFDF5;
                border-color: #14B8A6;
                color: #0F766E;
            }

            QPushButton:pressed {
                background-color: #D1FAE5;
            }

            QPushButton#primaryButton {
                background-color: #0F766E;
                color: white;
                border: none;
            }

            QPushButton#primaryButton:hover {
                background-color: #115E59;
            }

            QPushButton#closeButton {
                background-color: #F3F4F6;
                color: #374151;
                border: none;
            }

            QPushButton#closeButton:hover {
                background-color: #E5E7EB;
            }

            QTableWidget {
                background-color: white;
                color: #1F2937;
                border: 1px solid #E5E7EB;
                border-radius: 10px;
                gridline-color: #E5E7EB;
                selection-background-color: #CCFBF1;
                selection-color: #134E4A;
                alternate-background-color: #F9FAFB;
            }

            QTableWidget::item {
                padding: 7px;
            }

            QTableWidget::item:selected {
                background-color: #CCFBF1;
                color: #134E4A;
            }

            QHeaderView::section {
                background-color: #F0FDFA;
                color: #0F766E;
                font-weight: bold;
                border: none;
                border-bottom: 1px solid #D1D5DB;
                padding: 9px;
            }

        """)

        # ==================================================
        # TIÊU ĐỀ
        # ==================================================

        title = QLabel(
            "📦  Quản lý kho thuốc"
        )

        title.setObjectName(
            "pageTitle"
        )

        subtitle = QLabel(
            "Theo dõi tồn kho, tình trạng thuốc và hạn sử dụng tại Nhà thuốc Ý Như"
        )

        subtitle.setObjectName(
            "pageSubtitle"
        )

        # ==================================================
        # CARD THỐNG KÊ
        # ==================================================

        self.total_card = self.create_card(
            "💊",
            "LOẠI THUỐC",
            "0"
        )

        self.available_card = self.create_card(
            "🟢",
            "CÒN HÀNG",
            "0"
        )

        self.low_card = self.create_card(
            "🟡",
            "SẮP HẾT",
            "0"
        )

        self.out_card = self.create_card(
            "🔴",
            "HẾT HÀNG",
            "0"
        )

        self.near_expiry_card = self.create_card(
            "🟠",
            "SẮP HẾT HẠN",
            "0"
        )

        self.expired_card = self.create_card(
            "⚠️",
            "HẾT HẠN",
            "0"
        )

        # ==================================================
        # LAYOUT CARD
        # ==================================================

        cards_layout = QHBoxLayout()

        cards_layout.setSpacing(
            7
        )

        cards_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        cards_layout.addWidget(
            self.total_card
        )

        cards_layout.addWidget(
            self.available_card
        )

        cards_layout.addWidget(
            self.low_card
        )

        cards_layout.addWidget(
            self.out_card
        )

        cards_layout.addWidget(
            self.near_expiry_card
        )

        cards_layout.addWidget(
            self.expired_card
        )

        # ==================================================
        # PANEL TÌM KIẾM
        # ==================================================

        search_panel = QFrame()

        search_panel.setObjectName(
            "panel"
        )

        search_panel.setFixedHeight(
            65
        )

        search_layout = QHBoxLayout()

        search_layout.setContentsMargins(
            15,
            8,
            15,
            8
        )

        search_layout.setSpacing(
            8
        )

        search_label = QLabel(
            "🔎  Tìm kiếm thuốc:"
        )

        search_label.setObjectName(
            "searchLabel"
        )

        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "Nhập tên thuốc cần tìm..."
        )

        self.search_input.setMinimumHeight(
            36
        )

        self.search_input.returnPressed.connect(
            self.search_medicine
        )

        search_button = QPushButton(
            "🔎 Tìm kiếm"
        )

        search_button.setObjectName(
            "primaryButton"
        )

        search_button.setFixedHeight(
            36
        )

        search_button.clicked.connect(
            self.search_medicine
        )

        refresh_button = QPushButton(
            "🔄 Làm mới"
        )

        refresh_button.setFixedHeight(
            36
        )

        refresh_button.clicked.connect(
            self.refresh_data
        )

        search_layout.addWidget(
            search_label
        )

        search_layout.addWidget(
            self.search_input,
            1
        )

        search_layout.addWidget(
            search_button
        )

        search_layout.addWidget(
            refresh_button
        )

        search_panel.setLayout(
            search_layout
        )

        # ==================================================
        # TIÊU ĐỀ DANH SÁCH
        # ==================================================

        table_title = QLabel(
            "📋  Danh sách tồn kho"
        )

        table_title.setStyleSheet("""
            QLabel {
                color: #111827;
                font-size: 16px;
                font-weight: bold;
                background-color: transparent;
            }
        """)

        # ==================================================
        # BẢNG
        # ==================================================

        self.table = QTableWidget()

        self.table.setColumnCount(
            7
        )

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Tên thuốc",
            "Loại",
            "Đơn vị",
            "Giá",
            "Tồn kho",
            "Hạn sử dụng"
        ])

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.table.setAlternatingRowColors(
            True
        )

        self.table.verticalHeader().setVisible(
            False
        )

        # ==================================================
        # NÚT ĐÓNG
        # ==================================================

        close_button = QPushButton(
            "❌  Đóng"
        )

        close_button.setObjectName(
            "closeButton"
        )

        close_button.setFixedHeight(
            38
        )

        close_button.clicked.connect(
            self.close
        )

        # ==================================================
        # LAYOUT CHÍNH
        # ==================================================

        layout = QVBoxLayout()

        layout.setContentsMargins(
            25,
            15,
            25,
            15
        )

        layout.setSpacing(
            8
        )

        layout.addWidget(
            title
        )

        layout.addWidget(
            subtitle
        )

        layout.addSpacing(
            2
        )

        layout.addLayout(
            cards_layout
        )

        layout.addSpacing(
            3
        )

        layout.addWidget(
            search_panel
        )

        layout.addWidget(
            table_title
        )

        layout.addWidget(
            self.table
        )

        layout.addWidget(
            close_button
        )

        self.setLayout(
            layout
        )

        # ==================================================
        # TẢI DỮ LIỆU
        # ==================================================

        self.update_statistics()

        self.load_inventory()

    # ==================================================
    # TẠO CARD
    # ==================================================

    def create_card(
        self,
        icon,
        title,
        value
    ):

        card = QFrame()

        card.setObjectName(
            "statCard"
        )

        card.setFixedHeight(
            82
        )

        layout = QHBoxLayout()

        layout.setContentsMargins(
            10,
            7,
            10,
            7
        )

        layout.setSpacing(
            8
        )

        icon_label = QLabel(
            icon
        )

        icon_label.setObjectName(
            "statIcon"
        )

        icon_label.setAlignment(
            Qt.AlignCenter
        )

        icon_label.setFixedSize(
            38,
            38
        )

        text_layout = QVBoxLayout()

        text_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        text_layout.setSpacing(
            0
        )

        title_label = QLabel(
            title
        )

        title_label.setObjectName(
            "statTitle"
        )

        value_label = QLabel(
            value
        )

        value_label.setObjectName(
            "statValue"
        )

        title_label.setAlignment(
            Qt.AlignLeft |
            Qt.AlignVCenter
        )

        value_label.setAlignment(
            Qt.AlignLeft |
            Qt.AlignVCenter
        )

        text_layout.addWidget(
            title_label
        )

        text_layout.addWidget(
            value_label
        )

        layout.addWidget(
            icon_label
        )

        layout.addLayout(
            text_layout
        )

        layout.addStretch()

        card.setLayout(
            layout
        )

        # Lưu label để cập nhật sau
        card.value_label = value_label

        return card

    # ==================================================
    # CẬP NHẬT THỐNG KÊ
    # ==================================================

    def update_statistics(self):

        total = self.get_total_medicines()

        available = self.get_available_medicines()

        low_stock = self.get_low_stock()

        out_of_stock = self.get_out_of_stock()

        near_expiry = self.get_near_expiry_medicines()

        expired = self.get_expired_medicines()

        self.total_card.value_label.setText(
            str(total)
        )

        self.available_card.value_label.setText(
            str(available)
        )

        self.low_card.value_label.setText(
            str(low_stock)
        )

        self.out_card.value_label.setText(
            str(out_of_stock)
        )

        self.near_expiry_card.value_label.setText(
            str(near_expiry)
        )

        self.expired_card.value_label.setText(
            str(expired)
        )

    # ==================================================
    # TỔNG SỐ LOẠI THUỐC
    # ==================================================

    def get_total_medicines(self):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM medicines
        """)

        result = cursor.fetchone()

        connection.close()

        return result[0]

    # ==================================================
    # THUỐC CÒN HÀNG
    # ==================================================

    def get_available_medicines(self):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM medicines
            WHERE quantity > 10
        """)

        result = cursor.fetchone()

        connection.close()

        return result[0]

    # ==================================================
    # THUỐC SẮP HẾT
    # ==================================================

    def get_low_stock(self):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM medicines
            WHERE quantity > 0
            AND quantity <= 10
        """)

        result = cursor.fetchone()

        connection.close()

        return result[0]

    # ==================================================
    # THUỐC HẾT HÀNG
    # ==================================================

    def get_out_of_stock(self):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM medicines
            WHERE quantity <= 0
        """)

        result = cursor.fetchone()

        connection.close()

        return result[0]

    # ==================================================
    # THUỐC SẮP HẾT HẠN
    # CÒN TỪ 0 ĐẾN 30 NGÀY
    # ==================================================

    def get_near_expiry_medicines(self):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT expiry_date
            FROM medicines
            WHERE expiry_date IS NOT NULL
            AND expiry_date != ''
        """)

        medicines = cursor.fetchall()

        connection.close()

        today = date.today()

        count = 0

        for medicine in medicines:

            try:

                expiry = datetime.strptime(
                    str(medicine[0]),
                    "%Y-%m-%d"
                ).date()

                days_left = (
                    expiry - today
                ).days

                if 0 <= days_left <= 30:

                    count += 1

            except (
                ValueError,
                TypeError
            ):

                pass

        return count

    # ==================================================
    # THUỐC HẾT HẠN
    # ==================================================

    def get_expired_medicines(self):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT expiry_date
            FROM medicines
            WHERE expiry_date IS NOT NULL
            AND expiry_date != ''
        """)

        medicines = cursor.fetchall()

        connection.close()

        today = date.today()

        count = 0

        for medicine in medicines:

            try:

                expiry = datetime.strptime(
                    str(medicine[0]),
                    "%Y-%m-%d"
                ).date()

                if expiry < today:

                    count += 1

            except (
                ValueError,
                TypeError
            ):

                pass

        return count

    # ==================================================
    # TẢI DANH SÁCH KHO
    # ==================================================

    def load_inventory(self):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                category,
                unit,
                price,
                quantity,
                expiry_date

            FROM medicines

            ORDER BY
                quantity ASC,
                id DESC
        """)

        medicines = cursor.fetchall()

        connection.close()

        self.display_medicines(
            medicines
        )

    # ==================================================
    # HIỂN THỊ THUỐC
    # ==================================================

    def display_medicines(
        self,
        medicines
    ):

        self.table.setRowCount(
            len(medicines)
        )

        today = date.today()

        for row, medicine in enumerate(
            medicines
        ):

            medicine_id = medicine[0]

            name = medicine[1]

            category = medicine[2]

            unit = medicine[3]

            price = medicine[4]

            quantity = medicine[5]

            expiry_date = medicine[6]

            # ==================================================
            # ID
            # ==================================================

            id_item = QTableWidgetItem(
                str(medicine_id)
            )

            id_item.setTextAlignment(
                Qt.AlignCenter
            )

            self.table.setItem(
                row,
                0,
                id_item
            )

            # ==================================================
            # TÊN
            # ==================================================

            name_item = QTableWidgetItem(
                str(name)
            )

            self.table.setItem(
                row,
                1,
                name_item
            )

            # ==================================================
            # LOẠI
            # ==================================================

            category_item = QTableWidgetItem(
                str(category or "")
            )

            self.table.setItem(
                row,
                2,
                category_item
            )

            # ==================================================
            # ĐƠN VỊ
            # ==================================================

            unit_item = QTableWidgetItem(
                str(unit or "")
            )

            unit_item.setTextAlignment(
                Qt.AlignCenter
            )

            self.table.setItem(
                row,
                3,
                unit_item
            )

            # ==================================================
            # GIÁ
            # ==================================================

            try:

                price_text = (
                    f"{float(price):,.0f} đ"
                )

            except (
                ValueError,
                TypeError
            ):

                price_text = "0 đ"

            price_item = QTableWidgetItem(
                price_text
            )

            price_item.setTextAlignment(
                Qt.AlignRight |
                Qt.AlignVCenter
            )

            self.table.setItem(
                row,
                4,
                price_item
            )

            # ==================================================
            # TỒN KHO
            # ==================================================

            try:

                quantity_number = int(
                    quantity
                )

            except (
                ValueError,
                TypeError
            ):

                quantity_number = 0

            quantity_item = QTableWidgetItem()

            quantity_item.setTextAlignment(
                Qt.AlignCenter
            )

            if quantity_number <= 0:

                quantity_item.setText(
                    "🔴 HẾT"
                )

            elif quantity_number <= 10:

                quantity_item.setText(
                    f"🟡 {quantity_number}"
                )

            else:

                quantity_item.setText(
                    f"🟢 {quantity_number}"
                )

            self.table.setItem(
                row,
                5,
                quantity_item
            )

            # ==================================================
            # HẠN SỬ DỤNG
            # ==================================================

            expiry_item = QTableWidgetItem(
                str(expiry_date or "")
            )

            expiry_item.setTextAlignment(
                Qt.AlignCenter
            )

            if expiry_date:

                try:

                    expiry = datetime.strptime(
                        str(expiry_date),
                        "%Y-%m-%d"
                    ).date()

                    days_left = (
                        expiry - today
                    ).days

                    if days_left < 0:

                        expiry_item.setText(
                            f"🔴 {expiry_date} - ĐÃ HẾT HẠN"
                        )

                    elif days_left <= 30:

                        expiry_item.setText(
                            f"🟠 {expiry_date} - CÒN {days_left} NGÀY"
                        )

                    else:

                        expiry_item.setText(
                            str(expiry_date)
                        )

                except (
                    ValueError,
                    TypeError
                ):

                    pass

            self.table.setItem(
                row,
                6,
                expiry_item
            )

        # ==================================================
        # ĐỘ RỘNG CỘT
        # ==================================================

        self.table.setColumnWidth(
            0,
            55
        )

        self.table.setColumnWidth(
            1,
            230
        )

        self.table.setColumnWidth(
            2,
            130
        )

        self.table.setColumnWidth(
            3,
            80
        )

        self.table.setColumnWidth(
            4,
            120
        )

        self.table.setColumnWidth(
            5,
            150
        )

        self.table.setColumnWidth(
            6,
            260
        )

    # ==================================================
    # TÌM KIẾM
    # ==================================================

    def search_medicine(self):

        keyword = (
            self.search_input.text().strip()
        )

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                category,
                unit,
                price,
                quantity,
                expiry_date

            FROM medicines

            WHERE name LIKE ?

            ORDER BY
                quantity ASC,
                id DESC
        """, (
            f"%{keyword}%",
        ))

        medicines = cursor.fetchall()

        connection.close()

        self.display_medicines(
            medicines
        )

    # ==================================================
    # LÀM MỚI
    # ==================================================

    def refresh_data(self):

        self.search_input.clear()

        self.update_statistics()

        self.load_inventory()


# ==========================================================
# CHẠY RIÊNG FILE
# ==========================================================

if __name__ == "__main__":

    import sys

    from PySide6.QtWidgets import QApplication

    app = QApplication(
        sys.argv
    )

    window = InventoryWindow()

    window.show()

    sys.exit(
        app.exec()
    )