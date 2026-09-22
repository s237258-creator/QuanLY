from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QSpinBox,
    QMessageBox,
    QGroupBox,
    QLineEdit,
    QComboBox
)

from PySide6.QtCore import Qt
from datetime import datetime

from database.database import get_connection


class SaleWindow(QWidget):

    def __init__(self):
        super().__init__()

        # ==================================================
        # CẤU HÌNH CỬA SỔ
        # ==================================================

        self.setWindowTitle(
            "Nhà thuốc Ý Như - Bán thuốc"
        )

        self.setMinimumSize(
            1150,
            720
        )

        # ==================================================
        # GIAO DIỆN
        # ==================================================

        self.setStyleSheet("""

            QWidget {
                font-family: "Segoe UI";
                color: #1F2937;
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

            QGroupBox {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
                margin-top: 10px;
                padding: 12px;
                font-size: 15px;
                font-weight: bold;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 6px;
                color: #0F766E;
                background-color: #F5F7FA;
            }

            QLineEdit,
            QComboBox {

                background-color: #F9FAFB;
                color: #1F2937;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 8px 12px;
                min-height: 20px;
            }

            QLineEdit:focus,
            QComboBox:focus {

                background-color: white;
                border: 2px solid #14B8A6;
            }

            QSpinBox {

                background-color: white;
                color: #1F2937;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 7px;
                min-height: 20px;
            }

            QSpinBox:focus {

                border: 2px solid #14B8A6;
            }

            QPushButton {

                background-color: white;
                color: #374151;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 8px 14px;
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

            QPushButton#paymentButton {

                background-color: #10B981;
                color: white;
                border: none;
                border-radius: 9px;
                font-size: 16px;
                font-weight: bold;
                padding: 10px 20px;
            }

            QPushButton#paymentButton:hover {

                background-color: #059669;
            }

            QPushButton#paymentButton:pressed {

                background-color: #047857;
            }

            QPushButton#dangerButton {

                background-color: #FEF2F2;
                color: #DC2626;
                border: 1px solid #FECACA;
            }

            QPushButton#dangerButton:hover {

                background-color: #FEE2E2;
                border-color: #EF4444;
            }

            QTableWidget {

                background-color: white;
                color: #1F2937;
                border: 1px solid #E5E7EB;
                border-radius: 9px;
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

            QLabel#totalTitle {

                color: #6B7280;
                font-size: 13px;
                font-weight: bold;
                background-color: transparent;
            }

            QLabel#totalLabel {

                color: #0F766E;
                font-size: 23px;
                font-weight: bold;
                background-color: transparent;
            }

            QLabel#cartInfo {

                color: #6B7280;
                font-size: 12px;
                background-color: transparent;
            }

            QLabel#customerLabel {

                color: #374151;
                font-size: 13px;
                font-weight: bold;
                background-color: transparent;
            }

        """)

        # ==================================================
        # TIÊU ĐỀ
        # ==================================================

        title = QLabel(
            "🛒  Bán thuốc"
        )

        title.setObjectName(
            "pageTitle"
        )

        subtitle = QLabel(
            "Bán hàng nhanh chóng và quản lý đơn thuốc tại Nhà thuốc Ý Như"
        )

        subtitle.setObjectName(
            "pageSubtitle"
        )

        # ==================================================
        # DANH SÁCH THUỐC
        # ==================================================

        medicine_group = QGroupBox(
            "💊  Danh sách thuốc"
        )

        medicine_layout = QVBoxLayout()

        medicine_layout.setContentsMargins(
            8,
            10,
            8,
            8
        )

        medicine_layout.setSpacing(
            8
        )

        # ==================================================
        # THANH TÌM KIẾM
        # ==================================================

        search_layout = QHBoxLayout()

        search_layout.setSpacing(
            8
        )

        search_label = QLabel(
            "🔎 Tìm thuốc:"
        )

        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "Nhập tên thuốc cần tìm..."
        )

        self.search_input.setMinimumHeight(
            36
        )

        self.search_input.textChanged.connect(
            self.search_medicine
        )

        refresh_button = QPushButton(
            "🔄 Làm mới"
        )

        refresh_button.setFixedHeight(
            36
        )

        refresh_button.clicked.connect(
            self.refresh_medicines
        )

        search_layout.addWidget(
            search_label
        )

        search_layout.addWidget(
            self.search_input,
            1
        )

        search_layout.addWidget(
            refresh_button
        )

        # ==================================================
        # BẢNG THUỐC
        # ==================================================

        self.medicine_table = QTableWidget()

        self.medicine_table.setColumnCount(
            5
        )

        self.medicine_table.setHorizontalHeaderLabels([
            "ID",
            "Tên thuốc",
            "Đơn vị",
            "Đơn giá",
            "Tồn kho"
        ])

        self.medicine_table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.medicine_table.setSelectionMode(
            QTableWidget.SingleSelection
        )

        self.medicine_table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.medicine_table.setAlternatingRowColors(
            True
        )

        self.medicine_table.verticalHeader().setVisible(
            False
        )

        # ==================================================
        # CHỌN SỐ LƯỢNG
        # ==================================================

        quantity_layout = QHBoxLayout()

        quantity_layout.setSpacing(
            8
        )

        quantity_label = QLabel(
            "Số lượng:"
        )

        self.quantity = QSpinBox()

        self.quantity.setMinimum(
            1
        )

        self.quantity.setMaximum(
            1000
        )

        self.quantity.setValue(
            1
        )

        self.quantity.setFixedWidth(
            90
        )

        self.quantity.setFixedHeight(
            36
        )

        add_button = QPushButton(
            "➕  Thêm vào giỏ"
        )

        add_button.setObjectName(
            "primaryButton"
        )

        add_button.setFixedHeight(
            36
        )

        add_button.clicked.connect(
            self.add_to_cart
        )

        quantity_layout.addWidget(
            quantity_label
        )

        quantity_layout.addWidget(
            self.quantity
        )

        quantity_layout.addWidget(
            add_button
        )

        quantity_layout.addStretch()

        medicine_layout.addLayout(
            search_layout
        )

        medicine_layout.addWidget(
            self.medicine_table
        )

        medicine_layout.addLayout(
            quantity_layout
        )

        medicine_group.setLayout(
            medicine_layout
        )

        # ==================================================
        # GIỎ HÀNG
        # ==================================================

        cart_group = QGroupBox(
            "🛒  Giỏ hàng"
        )

        cart_layout = QVBoxLayout()

        cart_layout.setContentsMargins(
            8,
            10,
            8,
            8
        )

        cart_layout.setSpacing(
            8
        )

        # ==================================================
        # KHÁCH HÀNG
        # ==================================================

        customer_layout = QHBoxLayout()

        customer_label = QLabel(
            "👤 Khách hàng:"
        )

        customer_label.setObjectName(
            "customerLabel"
        )

        self.customer_combo = QComboBox()

        self.customer_combo.setMinimumHeight(
            36
        )

        self.customer_combo.setMinimumWidth(
            280
        )

        customer_refresh_button = QPushButton(
            "🔄"
        )

        customer_refresh_button.setToolTip(
            "Làm mới danh sách khách hàng"
        )

        customer_refresh_button.setFixedSize(
            42,
            36
        )

        customer_refresh_button.clicked.connect(
            self.load_customers
        )

        customer_layout.addWidget(
            customer_label
        )

        customer_layout.addWidget(
            self.customer_combo,
            1
        )

        customer_layout.addWidget(
            customer_refresh_button
        )

        # ==================================================
        # THÔNG TIN GIỎ
        # ==================================================

        self.cart_info = QLabel(
            "Chưa có sản phẩm trong giỏ hàng"
        )

        self.cart_info.setObjectName(
            "cartInfo"
        )

        # ==================================================
        # BẢNG GIỎ HÀNG
        # ==================================================

        self.cart_table = QTableWidget()

        self.cart_table.setColumnCount(
            5
        )

        self.cart_table.setHorizontalHeaderLabels([
            "ID",
            "Tên thuốc",
            "Số lượng",
            "Đơn giá",
            "Thành tiền"
        ])

        self.cart_table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.cart_table.setSelectionMode(
            QTableWidget.SingleSelection
        )

        self.cart_table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.cart_table.setAlternatingRowColors(
            True
        )

        self.cart_table.verticalHeader().setVisible(
            False
        )

        # ==================================================
        # NÚT GIỎ HÀNG
        # ==================================================

        cart_button_layout = QHBoxLayout()

        cart_button_layout.setSpacing(
            6
        )

        decrease_button = QPushButton(
            "➖ Giảm"
        )

        increase_button = QPushButton(
            "➕ Tăng"
        )

        remove_button = QPushButton(
            "🗑️ Xóa"
        )

        remove_button.setObjectName(
            "dangerButton"
        )

        decrease_button.setFixedHeight(
            36
        )

        increase_button.setFixedHeight(
            36
        )

        remove_button.setFixedHeight(
            36
        )

        decrease_button.clicked.connect(
            self.decrease_quantity
        )

        increase_button.clicked.connect(
            self.increase_quantity
        )

        remove_button.clicked.connect(
            self.remove_from_cart
        )

        cart_button_layout.addWidget(
            decrease_button
        )

        cart_button_layout.addWidget(
            increase_button
        )

        cart_button_layout.addWidget(
            remove_button
        )

        cart_button_layout.addStretch()

        # ==================================================
        # TỔNG TIỀN
        # ==================================================

        total_layout = QHBoxLayout()

        total_title = QLabel(
            "TỔNG THANH TOÁN"
        )

        total_title.setObjectName(
            "totalTitle"
        )

        self.total_label = QLabel(
            "0 đ"
        )

        self.total_label.setObjectName(
            "totalLabel"
        )

        self.total_label.setAlignment(
            Qt.AlignRight |
            Qt.AlignVCenter
        )

        total_layout.addWidget(
            total_title
        )

        total_layout.addStretch()

        total_layout.addWidget(
            self.total_label
        )

        # ==================================================
        # NÚT THANH TOÁN
        # ==================================================

        payment_button = QPushButton(
            "💳  THANH TOÁN"
        )

        payment_button.setObjectName(
            "paymentButton"
        )

        payment_button.setMinimumHeight(
            48
        )

        payment_button.clicked.connect(
            self.payment
        )

        # ==================================================
        # THÊM VÀO GIỎ
        # ==================================================

        cart_layout.addLayout(
            customer_layout
        )

        cart_layout.addWidget(
            self.cart_info
        )

        cart_layout.addWidget(
            self.cart_table
        )

        cart_layout.addLayout(
            cart_button_layout
        )

        cart_layout.addLayout(
            total_layout
        )

        cart_layout.addWidget(
            payment_button
        )

        cart_group.setLayout(
            cart_layout
        )

        # ==================================================
        # CHIA 2 CỘT
        # ==================================================

        content_layout = QHBoxLayout()

        content_layout.setSpacing(
            12
        )

        content_layout.addWidget(
            medicine_group,
            1
        )

        content_layout.addWidget(
            cart_group,
            1
        )

        # ==================================================
        # NÚT ĐÓNG
        # ==================================================

        close_button = QPushButton(
            "❌  Đóng"
        )

        close_button.setFixedHeight(
            38
        )

        close_button.clicked.connect(
            self.close
        )

        close_layout = QHBoxLayout()

        close_layout.addStretch()

        close_layout.addWidget(
            close_button
        )

        # ==================================================
        # LAYOUT CHÍNH
        # ==================================================

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            22,
            15,
            22,
            15
        )

        main_layout.setSpacing(
            8
        )

        main_layout.addWidget(
            title
        )

        main_layout.addWidget(
            subtitle
        )

        main_layout.addSpacing(
            3
        )

        main_layout.addLayout(
            content_layout
        )

        main_layout.addLayout(
            close_layout
        )

        self.setLayout(
            main_layout
        )

        # ==================================================
        # TẢI DỮ LIỆU
        # ==================================================

        self.load_customers()

        self.load_medicines()

    # ==================================================
    # TẢI DANH SÁCH KHÁCH HÀNG
    # ==================================================

    def load_customers(self):

        current_customer_id = (
            self.customer_combo.currentData()
        )

        self.customer_combo.blockSignals(
            True
        )

        self.customer_combo.clear()

        # Khách lẻ
        self.customer_combo.addItem(
            "👤 Khách lẻ",
            None
        )

        connection = get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute("""
                SELECT
                    id,
                    name,
                    phone
                FROM customers
                ORDER BY name COLLATE NOCASE ASC
            """)

            customers = cursor.fetchall()

        except Exception as error:

            connection.close()

            self.customer_combo.blockSignals(
                False
            )

            QMessageBox.warning(
                self,
                "Lỗi",
                f"Không thể tải danh sách khách hàng!\n\n{error}"
            )

            return

        connection.close()

        # ==================================================
        # THÊM KHÁCH HÀNG VÀO COMBOBOX
        # ==================================================

        for customer in customers:

            customer_id = customer[0]

            customer_name = customer[1]

            customer_phone = customer[2]

            text = str(
                customer_name
            )

            if customer_phone:

                text += (
                    f" - {customer_phone}"
                )

            self.customer_combo.addItem(
                text,
                customer_id
            )

        # ==================================================
        # GIỮ LẠI KHÁCH HÀNG ĐANG CHỌN
        # ==================================================

        if current_customer_id is not None:

            index = self.customer_combo.findData(
                current_customer_id
            )

            if index >= 0:

                self.customer_combo.setCurrentIndex(
                    index
                )

            else:

                self.customer_combo.setCurrentIndex(
                    0
                )

        else:

            self.customer_combo.setCurrentIndex(
                0
            )

        self.customer_combo.blockSignals(
            False
        )

    # ==================================================
    # LẤY TÊN KHÁCH HÀNG ĐANG CHỌN
    # ==================================================

    def get_selected_customer_name(self):

        index = self.customer_combo.currentIndex()

        # Khách lẻ
        if index <= 0:

            return "Khách lẻ"

        customer_text = (
            self.customer_combo.currentText()
        )

        # Nếu có số điện thoại
        if " - " in customer_text:

            customer_name = (
                customer_text.split(
                    " - ",
                    1
                )[0]
            )

        else:

            customer_name = customer_text

        customer_name = (
            customer_name.strip()
        )

        if not customer_name:

            return "Khách lẻ"

        return customer_name

    # ==================================================
    # TẢI DANH SÁCH THUỐC
    # ==================================================

    def load_medicines(self):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                unit,
                price,
                quantity
            FROM medicines
            ORDER BY id DESC
        """)

        medicines = cursor.fetchall()

        connection.close()

        self.all_medicines = medicines

        self.display_medicines(
            medicines
        )

    # ==================================================
    # LÀM MỚI THUỐC
    # ==================================================

    def refresh_medicines(self):

        self.search_input.clear()

        self.load_medicines()

    # ==================================================
    # HIỂN THỊ THUỐC
    # ==================================================

    def display_medicines(
        self,
        medicines
    ):

        self.medicine_table.setRowCount(
            len(medicines)
        )

        for row, medicine in enumerate(
            medicines
        ):

            medicine_id = medicine[0]

            medicine_name = medicine[1]

            unit = medicine[2]

            price = medicine[3]

            quantity = medicine[4]

            # ==================================================
            # ID
            # ==================================================

            id_item = QTableWidgetItem(
                str(medicine_id)
            )

            id_item.setTextAlignment(
                Qt.AlignCenter
            )

            self.medicine_table.setItem(
                row,
                0,
                id_item
            )

            # ==================================================
            # TÊN
            # ==================================================

            name_item = QTableWidgetItem(
                str(medicine_name)
            )

            self.medicine_table.setItem(
                row,
                1,
                name_item
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

            self.medicine_table.setItem(
                row,
                2,
                unit_item
            )

            # ==================================================
            # GIÁ
            # ==================================================

            try:

                price_number = float(
                    price
                )

                price_text = (
                    f"{price_number:,.0f} đ"
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

            self.medicine_table.setItem(
                row,
                3,
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

            if quantity_number <= 0:

                quantity_text = "🔴 HẾT"

            elif quantity_number <= 10:

                quantity_text = (
                    f"🟡 {quantity_number}"
                )

            else:

                quantity_text = (
                    f"🟢 {quantity_number}"
                )

            quantity_item = QTableWidgetItem(
                quantity_text
            )

            quantity_item.setTextAlignment(
                Qt.AlignCenter
            )

            self.medicine_table.setItem(
                row,
                4,
                quantity_item
            )

        # ==================================================
        # CHIỀU RỘNG CỘT
        # ==================================================

        self.medicine_table.setColumnWidth(
            0,
            55
        )

        self.medicine_table.setColumnWidth(
            1,
            230
        )

        self.medicine_table.setColumnWidth(
            2,
            80
        )

        self.medicine_table.setColumnWidth(
            3,
            125
        )

        self.medicine_table.setColumnWidth(
            4,
            100
        )

    # ==================================================
    # TÌM KIẾM THUỐC
    # ==================================================

    def search_medicine(
        self,
        keyword
    ):

        keyword = (
            keyword
            .strip()
            .lower()
        )

        if not keyword:

            self.display_medicines(
                self.all_medicines
            )

            return

        filtered_medicines = []

        for medicine in self.all_medicines:

            medicine_name = str(
                medicine[1]
            ).lower()

            if keyword in medicine_name:

                filtered_medicines.append(
                    medicine
                )

        self.display_medicines(
            filtered_medicines
        )

    # ==================================================
    # THÊM THUỐC VÀO GIỎ
    # ==================================================

    def add_to_cart(self):

        selected_row = (
            self.medicine_table.currentRow()
        )

        if selected_row < 0:

            QMessageBox.warning(
                self,
                "Thông báo",
                "Vui lòng chọn thuốc!"
            )

            return

        # ==================================================
        # LẤY THÔNG TIN THUỐC
        # ==================================================

        medicine_id = int(
            self.medicine_table.item(
                selected_row,
                0
            ).text()
        )

        medicine_name = (
            self.medicine_table.item(
                selected_row,
                1
            ).text()
        )

        price_text = (
            self.medicine_table.item(
                selected_row,
                3
            ).text()
        )

        price = float(
            price_text
            .replace(",", "")
            .replace(" đ", "")
        )

        stock_text = (
            self.medicine_table.item(
                selected_row,
                4
            ).text()
        )

        stock_text = (
            stock_text
            .replace("🟢 ", "")
            .replace("🟡 ", "")
            .replace("🔴 HẾT", "0")
        )

        stock = int(
            stock_text
        )

        quantity = (
            self.quantity.value()
        )

        # ==================================================
        # KIỂM TRA TỒN KHO
        # ==================================================

        if stock <= 0:

            QMessageBox.warning(
                self,
                "Hết hàng",
                f"Thuốc {medicine_name} đã hết hàng!"
            )

            return

        if quantity > stock:

            QMessageBox.warning(
                self,
                "Không đủ thuốc",
                f"Kho chỉ còn {stock} thuốc!"
            )

            return

        # ==================================================
        # KIỂM TRA THUỐC ĐÃ CÓ TRONG GIỎ
        # ==================================================

        for row in range(
            self.cart_table.rowCount()
        ):

            cart_id = int(
                self.cart_table.item(
                    row,
                    0
                ).text()
            )

            if cart_id == medicine_id:

                old_quantity = int(
                    self.cart_table.item(
                        row,
                        2
                    ).text()
                )

                new_quantity = (
                    old_quantity + quantity
                )

                if new_quantity > stock:

                    QMessageBox.warning(
                        self,
                        "Không đủ thuốc",
                        f"Kho chỉ còn {stock} thuốc!"
                    )

                    return

                self.cart_table.setItem(
                    row,
                    2,
                    QTableWidgetItem(
                        str(new_quantity)
                    )
                )

                total = (
                    price *
                    new_quantity
                )

                total_item = QTableWidgetItem(
                    f"{total:,.0f}"
                )

                total_item.setTextAlignment(
                    Qt.AlignRight |
                    Qt.AlignVCenter
                )

                self.cart_table.setItem(
                    row,
                    4,
                    total_item
                )

                self.update_total()

                return

        # ==================================================
        # THÊM DÒNG MỚI
        # ==================================================

        total = (
            price *
            quantity
        )

        row = (
            self.cart_table.rowCount()
        )

        self.cart_table.insertRow(
            row
        )

        # ID

        id_item = QTableWidgetItem(
            str(medicine_id)
        )

        id_item.setTextAlignment(
            Qt.AlignCenter
        )

        self.cart_table.setItem(
            row,
            0,
            id_item
        )

        # Tên thuốc

        self.cart_table.setItem(
            row,
            1,
            QTableWidgetItem(
                medicine_name
            )
        )

        # Số lượng

        quantity_item = QTableWidgetItem(
            str(quantity)
        )

        quantity_item.setTextAlignment(
            Qt.AlignCenter
        )

        self.cart_table.setItem(
            row,
            2,
            quantity_item
        )

        # Đơn giá

        price_item = QTableWidgetItem(
            f"{price:,.0f}"
        )

        price_item.setTextAlignment(
            Qt.AlignRight |
            Qt.AlignVCenter
        )

        self.cart_table.setItem(
            row,
            3,
            price_item
        )

        # Thành tiền

        total_item = QTableWidgetItem(
            f"{total:,.0f}"
        )

        total_item.setTextAlignment(
            Qt.AlignRight |
            Qt.AlignVCenter
        )

        self.cart_table.setItem(
            row,
            4,
            total_item
        )

        self.update_total()

    # ==================================================
    # XÓA THUỐC KHỎI GIỎ
    # ==================================================

    def remove_from_cart(self):

        selected_row = (
            self.cart_table.currentRow()
        )

        if selected_row < 0:

            QMessageBox.warning(
                self,
                "Thông báo",
                "Vui lòng chọn thuốc trong giỏ!"
            )

            return

        self.cart_table.removeRow(
            selected_row
        )

        self.update_total()

    # ==================================================
    # TĂNG SỐ LƯỢNG
    # ==================================================

    def increase_quantity(self):

        selected_row = (
            self.cart_table.currentRow()
        )

        if selected_row < 0:

            QMessageBox.warning(
                self,
                "Thông báo",
                "Vui lòng chọn thuốc trong giỏ!"
            )

            return

        medicine_id = int(
            self.cart_table.item(
                selected_row,
                0
            ).text()
        )

        current_quantity = int(
            self.cart_table.item(
                selected_row,
                2
            ).text()
        )

        # ==================================================
        # LẤY TỒN KHO THỰC TẾ
        # ==================================================

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                quantity,
                price
            FROM medicines
            WHERE id = ?
        """, (
            medicine_id,
        ))

        medicine = cursor.fetchone()

        connection.close()

        if medicine is None:

            QMessageBox.warning(
                self,
                "Lỗi",
                "Không tìm thấy thuốc!"
            )

            return

        stock = medicine[0]

        price = medicine[1]

        # ==================================================
        # KIỂM TRA TỒN
        # ==================================================

        if current_quantity >= stock:

            QMessageBox.warning(
                self,
                "Không đủ thuốc",
                f"Kho chỉ còn {stock} thuốc!"
            )

            return

        # ==================================================
        # TĂNG
        # ==================================================

        new_quantity = (
            current_quantity + 1
        )

        self.cart_table.setItem(
            selected_row,
            2,
            QTableWidgetItem(
                str(new_quantity)
            )
        )

        total = (
            float(price) *
            new_quantity
        )

        total_item = QTableWidgetItem(
            f"{total:,.0f}"
        )

        total_item.setTextAlignment(
            Qt.AlignRight |
            Qt.AlignVCenter
        )

        self.cart_table.setItem(
            selected_row,
            4,
            total_item
        )

        self.update_total()

    # ==================================================
    # GIẢM SỐ LƯỢNG
    # ==================================================

    def decrease_quantity(self):

        selected_row = (
            self.cart_table.currentRow()
        )

        if selected_row < 0:

            QMessageBox.warning(
                self,
                "Thông báo",
                "Vui lòng chọn thuốc trong giỏ!"
            )

            return

        current_quantity = int(
            self.cart_table.item(
                selected_row,
                2
            ).text()
        )

        # ==================================================
        # KHÔNG CHO NHỎ HƠN 1
        # ==================================================

        if current_quantity <= 1:

            QMessageBox.information(
                self,
                "Thông báo",
                "Số lượng tối thiểu là 1!"
            )

            return

        new_quantity = (
            current_quantity - 1
        )

        price = float(
            self.cart_table.item(
                selected_row,
                3
            ).text()
            .replace(",", "")
        )

        self.cart_table.setItem(
            selected_row,
            2,
            QTableWidgetItem(
                str(new_quantity)
            )
        )

        total = (
            price *
            new_quantity
        )

        total_item = QTableWidgetItem(
            f"{total:,.0f}"
        )

        total_item.setTextAlignment(
            Qt.AlignRight |
            Qt.AlignVCenter
        )

        self.cart_table.setItem(
            selected_row,
            4,
            total_item
        )

        self.update_total()

    # ==================================================
    # TÍNH TỔNG TIỀN
    # ==================================================

    def update_total(self):

        total = 0

        for row in range(
            self.cart_table.rowCount()
        ):

            value = (
                self.cart_table.item(
                    row,
                    4
                ).text()
            )

            value = (
                value
                .replace(",", "")
                .replace(" đ", "")
            )

            total += float(
                value
            )

        self.total_label.setText(
            f"{total:,.0f} đ"
        )

        # ==================================================
        # CẬP NHẬT THÔNG TIN GIỎ
        # ==================================================

        count = (
            self.cart_table.rowCount()
        )

        if count == 0:

            self.cart_info.setText(
                "Chưa có sản phẩm trong giỏ hàng"
            )

        else:

            total_quantity = 0

            for row in range(
                self.cart_table.rowCount()
            ):

                quantity = int(
                    self.cart_table.item(
                        row,
                        2
                    ).text()
                )

                total_quantity += quantity

            self.cart_info.setText(
                f"Đang có {count} loại thuốc "
                f"• Tổng số lượng: {total_quantity}"
            )

    # ==================================================
    # LẤY TỔNG TIỀN
    # ==================================================

    def get_cart_total(self):

        total = 0

        for row in range(
            self.cart_table.rowCount()
        ):

            value = (
                self.cart_table.item(
                    row,
                    4
                ).text()
            )

            value = (
                value
                .replace(",", "")
                .replace(" đ", "")
            )

            total += float(
                value
            )

        return total

    # ==================================================
    # THANH TOÁN
    # ==================================================

    def payment(self):

        # ==================================================
        # KIỂM TRA GIỎ
        # ==================================================

        if self.cart_table.rowCount() == 0:

            QMessageBox.warning(
                self,
                "Thông báo",
                "Giỏ hàng đang trống!"
            )

            return

        # ==================================================
        # LẤY KHÁCH HÀNG ĐÃ CHỌN
        # ==================================================

        customer_name = (
            self.get_selected_customer_name()
        )

        # ==================================================
        # TỔNG TIỀN
        # ==================================================

        total = (
            self.get_cart_total()
        )

        # ==================================================
        # XÁC NHẬN
        # ==================================================

        answer = QMessageBox.question(
            self,
            "Xác nhận thanh toán",
            f"Nhà thuốc Ý Như\n\n"
            f"Khách hàng: {customer_name}\n"
            f"Tổng tiền: {total:,.0f} đ\n\n"
            f"Bạn có chắc muốn thanh toán không?",
            QMessageBox.Yes |
            QMessageBox.No
        )

        if answer != QMessageBox.Yes:

            return

        # ==================================================
        # KẾT NỐI DATABASE
        # ==================================================

        connection = get_connection()

        cursor = connection.cursor()

        try:

            # ==================================================
            # KIỂM TRA TỒN KHO LẦN CUỐI
            # ==================================================

            for row in range(
                self.cart_table.rowCount()
            ):

                medicine_id = int(
                    self.cart_table.item(
                        row,
                        0
                    ).text()
                )

                cart_quantity = int(
                    self.cart_table.item(
                        row,
                        2
                    ).text()
                )

                cursor.execute("""
                    SELECT
                        name,
                        quantity,
                        price
                    FROM medicines
                    WHERE id = ?
                """, (
                    medicine_id,
                ))

                medicine = (
                    cursor.fetchone()
                )

                if medicine is None:

                    raise Exception(
                        "Không tìm thấy thuốc trong database!"
                    )

                medicine_name = (
                    medicine[0]
                )

                stock = (
                    medicine[1]
                )

                if cart_quantity > stock:

                    raise Exception(
                        f"Thuốc {medicine_name} "
                        f"không đủ số lượng trong kho!"
                    )

            # ==================================================
            # TẠO THỜI GIAN
            # ==================================================

            created_at = (
                datetime.now()
                .strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )

            # ==================================================
            # TẠO HÓA ĐƠN
            # ==================================================

            cursor.execute("""
                INSERT INTO invoices
                (
                    customer_name,
                    total,
                    payment_status,
                    created_at
                )
                VALUES (?, ?, ?, ?)
            """, (
                customer_name,
                total,
                "Đã thanh toán",
                created_at
            ))

            invoice_id = (
                cursor.lastrowid
            )

            # ==================================================
            # THÊM CHI TIẾT HÓA ĐƠN
            # ==================================================

            for row in range(
                self.cart_table.rowCount()
            ):

                medicine_id = int(
                    self.cart_table.item(
                        row,
                        0
                    ).text()
                )

                quantity = int(
                    self.cart_table.item(
                        row,
                        2
                    ).text()
                )

                price = float(
                    self.cart_table.item(
                        row,
                        3
                    ).text()
                    .replace(",", "")
                )

                # ==================================================
                # LƯU CHI TIẾT HÓA ĐƠN
                # ==================================================

                cursor.execute("""
                    INSERT INTO invoice_details
                    (
                        invoice_id,
                        medicine_id,
                        quantity,
                        price
                    )
                    VALUES (?, ?, ?, ?)
                """, (
                    invoice_id,
                    medicine_id,
                    quantity,
                    price
                ))

                # ==================================================
                # TRỪ TỒN KHO
                # ==================================================

                cursor.execute("""
                    UPDATE medicines
                    SET quantity = quantity - ?
                    WHERE id = ?
                """, (
                    quantity,
                    medicine_id
                ))

            # ==================================================
            # LƯU DATABASE
            # ==================================================

            connection.commit()

            connection.close()

            # ==================================================
            # THÔNG BÁO THÀNH CÔNG
            # ==================================================

            QMessageBox.information(
                self,
                "Thanh toán thành công",
                f"🎉 Thanh toán thành công!\n\n"
                f"Nhà thuốc Ý Như\n"
                f"Mã hóa đơn: {invoice_id}\n"
                f"Khách hàng: {customer_name}\n"
                f"Tổng tiền: {total:,.0f} đ"
            )

            # ==================================================
            # XÓA GIỎ
            # ==================================================

            self.cart_table.setRowCount(
                0
            )

            self.update_total()

            # ==================================================
            # TẢI LẠI THUỐC
            # ==================================================

            self.load_medicines()

            # ==================================================
            # TẢI LẠI KHÁCH HÀNG
            # ==================================================

            self.load_customers()

        except Exception as error:

            connection.rollback()

            connection.close()

            QMessageBox.critical(
                self,
                "Lỗi thanh toán",
                f"Không thể thanh toán!\n\n"
                f"{error}"
            )


# ==========================================================
# CHẠY RIÊNG SALE.PY ĐỂ KIỂM TRA
# ==========================================================

if __name__ == "__main__":

    import sys

    from PySide6.QtWidgets import QApplication

    from database.database import create_database

    create_database()

    app = QApplication(
        sys.argv
    )

    window = SaleWindow()

    window.show()

    sys.exit(
        app.exec()
    )