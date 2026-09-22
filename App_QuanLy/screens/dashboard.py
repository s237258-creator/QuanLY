# ============================================================
# DASHBOARD - NHÀ THUỐC Ý NHƯ
# ============================================================

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QLineEdit,
    QMessageBox,
    QSizePolicy,
)

from PySide6.QtCore import Qt

from datetime import datetime, date

from database.database import get_connection

from screens.medicine import MedicineWindow
from screens.sale import SaleWindow
from screens.invoice import InvoiceWindow
from screens.stock_import import StockImportWindow
from screens.inventory import InventoryWindow
from screens.customer import CustomerWindow
from screens.statistics import StatisticsWindow
from screens.settings import SettingsWindow


class DashboardWindow(QWidget):

    def __init__(self):
        super().__init__()

        # =====================================================
        # CÁC CỬA SỔ CON
        # =====================================================

        self.medicine_window = None
        self.inventory_window = None
        self.sale_window = None
        self.invoice_window = None
        self.stock_import_window = None
        self.customer_window = None
        self.statistics_window = None
        self.settings_window = None

        # =====================================================
        # CẤU HÌNH CỬA SỔ
        # =====================================================

        self.setWindowTitle(
            "Nhà thuốc Ý Như - Dashboard"
        )

        self.setMinimumSize(
            1180,
            760
        )

        # =====================================================
        # STYLE RIÊNG CHO DASHBOARD
        # Giúp tránh nền trắng phía sau QLabel
        # =====================================================

        self.setStyleSheet("""
            QWidget#dashboardRoot {
                background-color: #F4F8FA;
            }

            QLabel {
                background-color: transparent;
            }

            QLineEdit {
                background-color: white;
                border: 1px solid #D8E7EA;
                border-radius: 22px;
                padding: 0 18px;
                color: #244B5A;
                font-size: 13px;
                selection-background-color: #18B69B;
            }

            QLineEdit:focus {
                border: 1px solid #18B69B;
            }

            QScrollBar:vertical {
                background: transparent;
                width: 8px;
                margin: 0;
            }

            QScrollBar::handle:vertical {
                background: #C8DDDF;
                border-radius: 4px;
                min-height: 30px;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0;
            }
        """)

        self.setObjectName(
            "dashboardRoot"
        )

        # =====================================================
        # GIAO DIỆN
        # =====================================================

        self.create_ui()

    # =========================================================
    # TẠO GIAO DIỆN
    # =========================================================

    def create_ui(self):

        # =====================================================
        # LAYOUT TỔNG
        # =====================================================

        main_layout = QHBoxLayout()

        main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        main_layout.setSpacing(0)

        # =====================================================
        # SIDEBAR
        # =====================================================

        sidebar = self.create_sidebar()

        main_layout.addWidget(
            sidebar
        )

        # =====================================================
        # KHU VỰC NỘI DUNG
        # =====================================================

        content = QWidget()

        content.setObjectName(
            "contentArea"
        )

        content_layout = QVBoxLayout()

        content_layout.setContentsMargins(
            28,
            20,
            28,
            18
        )

        content_layout.setSpacing(
            18
        )

        # =====================================================
        # BANNER CHÀO MỪNG
        # =====================================================

        welcome_banner = self.create_welcome_banner()

        content_layout.addWidget(
            welcome_banner
        )

        # =====================================================
        # CÁC CARD THỐNG KÊ
        # =====================================================

        cards_layout = QHBoxLayout()

        cards_layout.setSpacing(
            16
        )

        # Lấy dữ liệu database

        total_medicines = self.get_total_medicines()

        low_stock = self.get_low_stock()

        expired = self.get_expired_medicines()

        revenue = self.get_revenue()

        # Card 1

        medicine_card = self.create_stat_card(
            icon="💊",
            title="Tổng số thuốc",
            value=str(total_medicines),
            description="Thuốc đang quản lý",
            icon_bg="#DDF8EE",
            icon_color="#10A982",
            value_color="#10966F"
        )

        # Card 2

        low_stock_card = self.create_stat_card(
            icon="📦",
            title="Thuốc sắp hết",
            value=str(low_stock),
            description="Cần kiểm tra tồn kho",
            icon_bg="#E2F0FF",
            icon_color="#2388D9",
            value_color="#2180C7"
        )

        # Card 3

        expired_card = self.create_stat_card(
            icon="⚠️",
            title="Thuốc hết hạn",
            value=str(expired),
            description="Cần xử lý",
            icon_bg="#FFF0DD",
            icon_color="#EF8B20",
            value_color="#D9780C"
        )

        # Card 4

        revenue_card = self.create_stat_card(
            icon="📊",
            title="Doanh thu",
            value=f"{revenue:,.0f} đ",
            description="Tổng đã thanh toán",
            icon_bg="#F0E5FF",
            icon_color="#8A52D8",
            value_color="#7540C7"
        )

        cards_layout.addWidget(
            medicine_card
        )

        cards_layout.addWidget(
            low_stock_card
        )

        cards_layout.addWidget(
            expired_card
        )

        cards_layout.addWidget(
            revenue_card
        )

        content_layout.addLayout(
            cards_layout
        )

        # =====================================================
        # CHỨC NĂNG CHÍNH
        # =====================================================

        functions_panel = self.create_functions_panel()

        content_layout.addWidget(
            functions_panel
        )

        # =====================================================
        # THANH TRẠNG THÁI
        # =====================================================

        status_bar = self.create_status_bar()

        content_layout.addWidget(
            status_bar
        )

        # =====================================================
        # FOOTER
        # =====================================================

        footer = QLabel(
            "💚  Nhà thuốc Ý Như   •   Quản lý bán thuốc và kho thuốc"
        )

        footer.setObjectName(
            "footerLabel"
        )

        footer.setAlignment(
            Qt.AlignRight
        )

        footer.setStyleSheet("""
            QLabel#footerLabel {
                background-color: transparent;
                color: #8AA2AD;
                font-size: 11px;
                padding-right: 4px;
            }
        """)

        content_layout.addWidget(
            footer
        )

        content.setLayout(
            content_layout
        )

        main_layout.addWidget(
            content,
            1
        )

        self.setLayout(
            main_layout
        )

    # =========================================================
    # TẠO SIDEBAR
    # =========================================================

    def create_sidebar(self):

        sidebar = QFrame()

        sidebar.setObjectName(
            "sidebar"
        )

        sidebar.setFixedWidth(
            255
        )

        sidebar.setStyleSheet("""
            QFrame#sidebar {
                background-color: #064B49;
                border: none;
            }

            QLabel {
                background-color: transparent;
            }

            QLabel#brandIcon {
                background-color: #D7FFF0;
                color: #079477;
                border-radius: 18px;
                font-size: 28px;
                font-weight: bold;
            }

            QLabel#brandName {
                color: white;
                font-size: 21px;
                font-weight: 800;
            }

            QLabel#brandSub {
                color: #A9DED4;
                font-size: 11px;
            }

            QFrame#brandLine {
                background-color: #176B68;
                border: none;
            }

            QPushButton#sideButton {
                background-color: transparent;
                color: #E7F7F4;
                border: none;
                border-radius: 12px;
                text-align: left;
                padding: 0 16px;
                font-size: 13px;
                font-weight: 600;
            }

            QPushButton#sideButton:hover {
                background-color: #126B67;
            }

            QPushButton#sideButtonActive {
                background-color: #21AE92;
                color: white;
                border: none;
                border-radius: 12px;
                text-align: left;
                padding: 0 16px;
                font-size: 13px;
                font-weight: 700;
            }

            QPushButton#sideButtonActive:hover {
                background-color: #28BDA0;
            }

            QPushButton#logoutButton {
                background-color: transparent;
                color: #FFB3B3;
                border: none;
                border-radius: 12px;
                text-align: left;
                padding: 0 16px;
                font-size: 13px;
                font-weight: 600;
            }

            QPushButton#logoutButton:hover {
                background-color: #704347;
                color: white;
            }
        """)

        sidebar_layout = QVBoxLayout()

        sidebar_layout.setContentsMargins(
            14,
            22,
            14,
            18
        )

        sidebar_layout.setSpacing(
            5
        )

        # =====================================================
        # LOGO
        # =====================================================

        brand_layout = QHBoxLayout()

        brand_layout.setSpacing(
            10
        )

        # Icon

        brand_icon = QLabel(
            "✚"
        )

        brand_icon.setObjectName(
            "brandIcon"
        )

        brand_icon.setFixedSize(
            52,
            52
        )

        brand_icon.setAlignment(
            Qt.AlignCenter
        )

        # Tên nhà thuốc

        brand_text_layout = QVBoxLayout()

        brand_text_layout.setSpacing(
            0
        )

        brand_name = QLabel(
            "Nhà thuốc\nÝ Như"
        )

        brand_name.setObjectName(
            "brandName"
        )

        brand_sub = QLabel(
            "Vì sức khỏe của bạn"
        )

        brand_sub.setObjectName(
            "brandSub"
        )

        brand_text_layout.addWidget(
            brand_name
        )

        brand_text_layout.addWidget(
            brand_sub
        )

        brand_layout.addWidget(
            brand_icon
        )

        brand_layout.addLayout(
            brand_text_layout
        )

        sidebar_layout.addLayout(
            brand_layout
        )

        sidebar_layout.addSpacing(
            18
        )

        # =====================================================
        # ĐƯỜNG KẺ
        # =====================================================

        line = QFrame()

        line.setObjectName(
            "brandLine"
        )

        line.setFixedHeight(
            1
        )

        sidebar_layout.addWidget(
            line
        )

        sidebar_layout.addSpacing(
            18
        )

        # =====================================================
        # MENU SIDEBAR
        # =====================================================

        home_button = self.create_sidebar_button(
            "⌂",
            "Trang chủ",
            active=True
        )

        medicine_button = self.create_sidebar_button(
            "💊",
            "Quản lý thuốc"
        )

        customer_button = self.create_sidebar_button(
            "👤",
            "Khách hàng"
        )

        inventory_button = self.create_sidebar_button(
            "📦",
            "Quản lý kho"
        )

        sale_button = self.create_sidebar_button(
            "🛒",
            "Bán thuốc"
        )

        invoice_button = self.create_sidebar_button(
            "🧾",
            "Hóa đơn"
        )

        stock_import_button = self.create_sidebar_button(
            "📋",
            "Lịch sử nhập"
        )

        statistics_button = self.create_sidebar_button(
            "📊",
            "Thống kê"
        )

        settings_button = self.create_sidebar_button(
            "⚙",
            "Cài đặt"
        )

        # =====================================================
        # KẾT NỐI NÚT
        # =====================================================

        home_button.clicked.connect(
            self.go_home
        )

        medicine_button.clicked.connect(
            self.open_medicine
        )

        inventory_button.clicked.connect(
            self.open_inventory
        )

        sale_button.clicked.connect(
            self.open_sale
        )

        invoice_button.clicked.connect(
            self.open_invoice
        )

        stock_import_button.clicked.connect(
            self.open_stock_import
        )

        customer_button.clicked.connect(
            self.show_customer_message
        )

        statistics_button.clicked.connect(
            self.show_statistics_message
        )

        settings_button.clicked.connect(
            self.show_settings_message
        )

        # =====================================================
        # THÊM MENU
        # =====================================================

        sidebar_layout.addWidget(
            home_button
        )

        sidebar_layout.addWidget(
            medicine_button
        )

        sidebar_layout.addWidget(
            customer_button
        )

        sidebar_layout.addWidget(
            inventory_button
        )

        sidebar_layout.addWidget(
            sale_button
        )

        sidebar_layout.addWidget(
            invoice_button
        )

        sidebar_layout.addWidget(
            stock_import_button
        )

        sidebar_layout.addWidget(
            statistics_button
        )

        sidebar_layout.addWidget(
            settings_button
        )

        sidebar_layout.addStretch()

        # =====================================================
        # ĐĂNG XUẤT
        # =====================================================

        logout_button = QPushButton(
            "↪    Đăng xuất"
        )

        logout_button.setObjectName(
            "logoutButton"
        )

        logout_button.setFixedHeight(
            46
        )

        logout_button.clicked.connect(
            self.logout
        )

        sidebar_layout.addWidget(
            logout_button
        )

        sidebar.setLayout(
            sidebar_layout
        )

        return sidebar

    # =========================================================
    # TẠO NÚT SIDEBAR
    # =========================================================

    def create_sidebar_button(
        self,
        icon,
        text,
        active=False
    ):

        button = QPushButton(
            f"{icon}    {text}"
        )

        if active:

            button.setObjectName(
                "sideButtonActive"
            )

        else:

            button.setObjectName(
                "sideButton"
            )

        button.setFixedHeight(
            46
        )

        return button

    # =========================================================
    # THANH TOP BAR
    # =========================================================

    def create_top_bar(self):

        top_bar = QFrame()

        top_bar.setObjectName(
            "topBar"
        )

        top_bar.setFixedHeight(
            58
        )

        top_bar.setStyleSheet("""
            QFrame#topBar {
                background-color: transparent;
                border: none;
            }

            QLabel {
                background-color: transparent;
            }

            QLabel#notificationIcon {
                color: #25536A;
                font-size: 22px;
            }

            QLabel#adminAvatar {
                background-color: #18B69B;
                color: white;
                border-radius: 20px;
                font-size: 16px;
                font-weight: 700;
            }

            QLabel#adminName {
                color: #183D52;
                font-size: 13px;
                font-weight: 700;
            }

            QLabel#adminRole {
                color: #8AA0AE;
                font-size: 10px;
            }
        """)

        layout = QHBoxLayout()

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout.setSpacing(
            12
        )

        # =====================================================
        # Ô TÌM KIẾM
        # =====================================================

        search = QLineEdit()

        search.setPlaceholderText(
            "🔍    Tìm kiếm nhanh..."
        )

        search.setFixedHeight(
            44
        )

        search.setMaximumWidth(
            500
        )

        layout.addWidget(
            search
        )

        layout.addStretch()

        # =====================================================
        # THÔNG BÁO
        # =====================================================

        notification = QLabel(
            "♧"
        )

        notification.setObjectName(
            "notificationIcon"
        )

        notification.setAlignment(
            Qt.AlignCenter
        )

        notification.setFixedSize(
            42,
            42
        )

        layout.addWidget(
            notification
        )

        # =====================================================
        # AVATAR
        # =====================================================

        avatar = QLabel(
            "A"
        )

        avatar.setObjectName(
            "adminAvatar"
        )

        avatar.setAlignment(
            Qt.AlignCenter
        )

        avatar.setFixedSize(
            40,
            40
        )

        layout.addWidget(
            avatar
        )

        # =====================================================
        # THÔNG TIN ADMIN
        # =====================================================

        admin_layout = QVBoxLayout()

        admin_layout.setSpacing(
            0
        )

        admin_name = QLabel(
            "Admin"
        )

        admin_name.setObjectName(
            "adminName"
        )

        admin_role = QLabel(
            "Quản trị viên"
        )

        admin_role.setObjectName(
            "adminRole"
        )

        admin_layout.addWidget(
            admin_name
        )

        admin_layout.addWidget(
            admin_role
        )

        layout.addLayout(
            admin_layout
        )

        arrow = QLabel(
            "⌄"
        )

        arrow.setStyleSheet("""
            QLabel {
                background-color: transparent;
                color: #557789;
                font-size: 18px;
            }
        """)

        layout.addWidget(
            arrow
        )

        top_bar.setLayout(
            layout
        )

        return top_bar

    # =========================================================
    # BANNER CHÀO MỪNG
    # =========================================================

    def create_welcome_banner(self):

        banner = QFrame()

        banner.setObjectName(
            "welcomeBanner"
        )

        banner.setMinimumHeight(
            126
        )

        banner.setStyleSheet("""
            QFrame#welcomeBanner {
                background-color: #E6F9F3;
                border: 1px solid #C4EDE2;
                border-radius: 18px;
            }

            QLabel {
                background-color: transparent;
            }

            QLabel#welcomeTitle {
                color: #123E57;
                font-size: 25px;
                font-weight: 800;
            }

            QLabel#welcomeText {
                color: #67879A;
                font-size: 13px;
            }

            QLabel#welcomeSub {
                color: #119575;
                font-size: 12px;
                font-weight: 600;
            }

            QLabel#welcomeIcons {
                color: #159B82;
                font-size: 38px;
            }
        """)

        layout = QHBoxLayout()

        layout.setContentsMargins(
            30,
            20,
            30,
            20
        )

        # =====================================================
        # NỘI DUNG
        # =====================================================

        text_layout = QVBoxLayout()

        text_layout.setSpacing(
            5
        )

        title = QLabel(
            "👋  Xin chào, Admin!"
        )

        title.setObjectName(
            "welcomeTitle"
        )

        text = QLabel(
            "Chào mừng bạn đến với hệ thống quản lý nhà thuốc Ý Như"
        )

        text.setObjectName(
            "welcomeText"
        )

        sub = QLabel(
            "💚  Cùng quản lý hiệu quả - Vì sức khỏe cộng đồng"
        )

        sub.setObjectName(
            "welcomeSub"
        )

        text_layout.addWidget(
            title
        )

        text_layout.addWidget(
            text
        )

        text_layout.addSpacing(
            4
        )

        text_layout.addWidget(
            sub
        )

        layout.addLayout(
            text_layout
        )

        layout.addStretch()

        # =====================================================
        # ICON TRANG TRÍ
        # =====================================================

        icons = QLabel(
            "💊   🧴   ✚"
        )

        icons.setObjectName(
            "welcomeIcons"
        )

        icons.setAlignment(
            Qt.AlignCenter
        )

        icons.setMinimumWidth(
            210
        )

        layout.addWidget(
            icons
        )

        banner.setLayout(
            layout
        )

        return banner

    # =========================================================
    # TẠO CARD THỐNG KÊ
    # =========================================================

    def create_stat_card(
        self,
        icon,
        title,
        value,
        description,
        icon_bg,
        icon_color,
        value_color
    ):

        card = QFrame()

        card.setObjectName(
            "statCard"
        )

        card.setMinimumHeight(
            178
        )

        card.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

        card.setStyleSheet(f"""
            QFrame#statCard {{
                background-color: white;
                border: 1px solid #E0EAED;
                border-radius: 17px;
            }}

            QFrame#statCard:hover {{
                border: 1px solid #B9DDD7;
            }}

            QLabel {{
                background-color: transparent;
            }}

            QLabel#statIcon {{
                background-color: {icon_bg};
                color: {icon_color};
                border-radius: 34px;
                font-size: 26px;
            }}

            QLabel#statTitle {{
                color: #183F55;
                font-size: 14px;
                font-weight: 700;
            }}

            QLabel#statValue {{
                color: {value_color};
                font-size: 22px;
                font-weight: 800;
            }}

            QLabel#statDescription {{
                color: #91A5AF;
                font-size: 10px;
            }}

            QLabel#statBadge {{
                background-color: {icon_bg};
                color: {icon_color};
                border-radius: 10px;
                padding: 5px 9px;
                font-size: 10px;
                font-weight: 600;
            }}
        """)

        layout = QVBoxLayout()

        layout.setContentsMargins(
            18,
            17,
            18,
            16
        )

        layout.setSpacing(
            5
        )

        # =====================================================
        # HÀNG ICON + TIÊU ĐỀ
        # =====================================================

        top = QHBoxLayout()

        icon_label = QLabel(
            icon
        )

        icon_label.setObjectName(
            "statIcon"
        )

        icon_label.setFixedSize(
            60,
            60
        )

        icon_label.setAlignment(
            Qt.AlignCenter
        )

        top.addWidget(
            icon_label
        )

        top.addStretch()

        layout.addLayout(
            top
        )

        # =====================================================
        # TIÊU ĐỀ
        # =====================================================

        title_label = QLabel(
            title
        )

        title_label.setObjectName(
            "statTitle"
        )

        layout.addWidget(
            title_label
        )

        # =====================================================
        # GIÁ TRỊ
        # =====================================================

        value_label = QLabel(
            value
        )

        value_label.setObjectName(
            "statValue"
        )

        layout.addWidget(
            value_label
        )

        # =====================================================
        # MÔ TẢ
        # =====================================================

        description_label = QLabel(
            description
        )

        description_label.setObjectName(
            "statDescription"
        )

        layout.addWidget(
            description_label
        )

        card.setLayout(
            layout
        )

        return card

    # =========================================================
    # PANEL CHỨC NĂNG
    # =========================================================

    def create_functions_panel(self):

        panel = QFrame()

        panel.setObjectName(
            "functionsPanel"
        )

        panel.setMinimumHeight(
            240
        )

        panel.setStyleSheet("""
            QFrame#functionsPanel {
                background-color: white;
                border: 1px solid #E0EAED;
                border-radius: 17px;
            }

            QLabel {
                background-color: transparent;
            }

            QLabel#functionsTitle {
                color: #143F57;
                font-size: 19px;
                font-weight: 800;
            }

            QLabel#functionIcon {
                background-color: #E3F8F1;
                color: #159B80;
                border-radius: 21px;
                font-size: 18px;
            }

            QLabel#functionName {
                color: #214B60;
                font-size: 12px;
                font-weight: 700;
            }

            QLabel#functionDescription {
                color: #8299A6;
                font-size: 10px;
            }

            QFrame#functionSeparator {
                background-color: #DDE8EB;
                border: none;
            }
        """)

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            22,
            18,
            22,
            18
        )

        main_layout.setSpacing(
            12
        )

        # =====================================================
        # TIÊU ĐỀ
        # =====================================================

        title_layout = QHBoxLayout()

        title_icon = QLabel(
            "▤"
        )

        title_icon.setStyleSheet("""
            QLabel {
                background-color: transparent;
                color: #12A187;
                font-size: 25px;
                font-weight: bold;
            }
        """)

        title = QLabel(
            "Các chức năng chính"
        )

        title.setObjectName(
            "functionsTitle"
        )

        title_layout.addWidget(
            title_icon
        )

        title_layout.addWidget(
            title
        )

        title_layout.addStretch()

        main_layout.addLayout(
            title_layout
        )

        # =====================================================
        # 2 CỘT
        # =====================================================

        columns = QHBoxLayout()

        columns.setSpacing(
            24
        )

        # =====================================================
        # CỘT TRÁI
        # =====================================================

        left_column = QVBoxLayout()

        left_column.setSpacing(
            9
        )

        left_column.addWidget(
            self.create_function_item(
                "💊",
                "Quản lý thuốc",
                "Thêm, sửa, xóa, tìm kiếm thuốc"
            )
        )

        left_column.addWidget(
            self.create_function_item(
                "📦",
                "Quản lý kho",
                "Theo dõi số lượng thuốc tồn kho"
            )
        )

        left_column.addWidget(
            self.create_function_item(
                "🛒",
                "Bán thuốc",
                "Chọn thuốc, tạo đơn và thanh toán"
            )
        )

        # =====================================================
        # ĐƯỜNG NGĂN
        # =====================================================

        separator = QFrame()

        separator.setObjectName(
            "functionSeparator"
        )

        separator.setFixedWidth(
            1
        )

        columns.addLayout(
            left_column,
            1
        )

        columns.addWidget(
            separator
        )

        # =====================================================
        # CỘT PHẢI
        # =====================================================

        right_column = QVBoxLayout()

        right_column.setSpacing(
            9
        )

        right_column.addWidget(
            self.create_function_item(
                "🧾",
                "Hóa đơn",
                "Xem và quản lý hóa đơn"
            )
        )

        right_column.addWidget(
            self.create_function_item(
                "📋",
                "Lịch sử nhập",
                "Xem lịch sử các lần nhập thuốc"
            )
        )

        right_column.addWidget(
            self.create_function_item(
                "👤",
                "Khách hàng",
                "Quản lý thông tin khách hàng"
            )
        )

        right_column.addWidget(
            self.create_function_item(
                "📊",
                "Thống kê",
                "Xem doanh thu, thuốc bán chạy và tồn kho"
            )
        )

        columns.addLayout(
            right_column,
            1
        )

        main_layout.addLayout(
            columns
        )

        panel.setLayout(
            main_layout
        )

        return panel

    # =========================================================
    # MỘT DÒNG CHỨC NĂNG
    # =========================================================

    def create_function_item(
        self,
        icon,
        name,
        description
    ):

        frame = QFrame()

        frame.setMinimumHeight(
            45
        )

        frame.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border: none;
            }

            QLabel {
                background-color: transparent;
            }

            QLabel#functionIcon {
                background-color: #E3F8F1;
                color: #149B81;
                border-radius: 21px;
                font-size: 17px;
            }

            QLabel#functionName {
                color: #214B60;
                font-size: 12px;
                font-weight: 700;
            }

            QLabel#functionDescription {
                color: #8299A6;
                font-size: 10px;
            }
        """)

        layout = QHBoxLayout()

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout.setSpacing(
            10
        )

        # =====================================================
        # ICON
        # =====================================================

        icon_label = QLabel(
            icon
        )

        icon_label.setObjectName(
            "functionIcon"
        )

        icon_label.setFixedSize(
            42,
            42
        )

        icon_label.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            icon_label
        )

        # =====================================================
        # TEXT
        # =====================================================

        text_layout = QVBoxLayout()

        text_layout.setSpacing(
            1
        )

        name_label = QLabel(
            name
        )

        name_label.setObjectName(
            "functionName"
        )

        description_label = QLabel(
            description
        )

        description_label.setObjectName(
            "functionDescription"
        )

        text_layout.addWidget(
            name_label
        )

        text_layout.addWidget(
            description_label
        )

        layout.addLayout(
            text_layout
        )

        layout.addStretch()

        frame.setLayout(
            layout
        )

        return frame

    # =========================================================
    # THANH TRẠNG THÁI
    # =========================================================

    def create_status_bar(self):

        status = QFrame()

        status.setFixedHeight(
            48
        )

        status.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E0EAED;
                border-radius: 14px;
            }

            QLabel {
                background-color: transparent;
            }

            QLabel#statusText {
                color: #129878;
                font-size: 11px;
                font-weight: 700;
            }

            QLabel#databaseText {
                color: #8AA1AD;
                font-size: 10px;
            }

            QLabel#statusDot {
                background-color: #2CCB91;
                border-radius: 6px;
            }
        """)

        layout = QHBoxLayout()

        layout.setContentsMargins(
            14,
            0,
            14,
            0
        )

        layout.setSpacing(
            8
        )

        # =====================================================
        # CHẤM XANH
        # =====================================================

        dot = QLabel()

        dot.setObjectName(
            "statusDot"
        )

        dot.setFixedSize(
            12,
            12
        )

        layout.addWidget(
            dot
        )

        # =====================================================
        # TRẠNG THÁI
        # =====================================================

        status_text = QLabel(
            "Hệ thống đang hoạt động"
        )

        status_text.setObjectName(
            "statusText"
        )

        layout.addWidget(
            status_text
        )

        layout.addStretch()

        # =====================================================
        # DATABASE
        # =====================================================

        database_text = QLabel(
            "Cơ sở dữ liệu: pharmacy.db"
        )

        database_text.setObjectName(
            "databaseText"
        )

        layout.addWidget(
            database_text
        )

        status.setLayout(
            layout
        )

        return status

    # =========================================================
    # QUAY VỀ TRANG CHỦ
    # =========================================================

    def go_home(self):

        # Dashboard hiện tại đã là trang chủ.
        # Không cần mở cửa sổ mới.

        pass

    # =========================================================
    # LẤY TỔNG SỐ THUỐC
    # =========================================================

    def get_total_medicines(self):

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM medicines
            """)

            result = cursor.fetchone()

            return result[0] if result else 0

        finally:

            connection.close()

    # =========================================================
    # LẤY SỐ THUỐC SẮP HẾT
    # =========================================================

    def get_low_stock(self):

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM medicines
                WHERE quantity > 0
                AND quantity <= 10
            """)

            result = cursor.fetchone()

            return result[0] if result else 0

        finally:

            connection.close()

    # =========================================================
    # LẤY SỐ THUỐC HẾT HẠN
    # =========================================================

    def get_expired_medicines(self):

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute("""
                SELECT expiry_date
                FROM medicines
                WHERE expiry_date IS NOT NULL
                AND expiry_date != ''
            """)

            medicines = cursor.fetchall()

        finally:

            connection.close()

        today = date.today()

        count = 0

        for medicine in medicines:

            expiry_value = medicine[0]

            if not expiry_value:
                continue

            try:

                expiry = datetime.strptime(
                    expiry_value,
                    "%Y-%m-%d"
                ).date()

                if expiry < today:

                    count += 1

            except (ValueError, TypeError):

                pass

        return count

    # =========================================================
    # LẤY DOANH THU
    # =========================================================

    def get_revenue(self):

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute("""
                SELECT COALESCE(SUM(total), 0)
                FROM invoices
                WHERE payment_status = 'Đã thanh toán'
            """)

            result = cursor.fetchone()

            return result[0] if result else 0

        finally:

            connection.close()

    # =========================================================
    # MỞ QUẢN LÝ THUỐC
    # =========================================================

    def open_medicine(self):

        try:

            self.medicine_window = MedicineWindow()

            self.medicine_window.show()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Lỗi",
                f"Không thể mở Quản lý thuốc:\n\n{e}"
            )

    # =========================================================
    # MỞ QUẢN LÝ KHO
    # =========================================================

    def open_inventory(self):

        try:

            self.inventory_window = InventoryWindow()

            self.inventory_window.show()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Lỗi",
                f"Không thể mở Quản lý kho:\n\n{e}"
            )

    # =========================================================
    # MỞ BÁN THUỐC
    # =========================================================

    def open_sale(self):

        try:

            self.sale_window = SaleWindow()

            self.sale_window.show()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Lỗi",
                f"Không thể mở Bán thuốc:\n\n{e}"
            )

    # =========================================================
    # MỞ HÓA ĐƠN
    # =========================================================

    def open_invoice(self):

        try:

            self.invoice_window = InvoiceWindow()

            self.invoice_window.show()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Lỗi",
                f"Không thể mở Hóa đơn:\n\n{e}"
            )

    # =========================================================
    # MỞ LỊCH SỬ NHẬP THUỐC
    # =========================================================

    def open_stock_import(self):

        try:

            self.stock_import_window = StockImportWindow()

            self.stock_import_window.show()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Lỗi",
                f"Không thể mở Lịch sử nhập:\n\n{e}"
            )

    # =========================================================
    # KHÁCH HÀNG
    # =========================================================

    def show_customer_message(self):
        try:
            self.customer_window = CustomerWindow()
            self.customer_window.show()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể mở Quản lý khách hàng:\n\n{e}")

    # =========================================================
    # THỐNG KÊ
    # =========================================================

    def show_statistics_message(self):
        try:
            self.statistics_window = StatisticsWindow()
            self.statistics_window.show()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể mở Thống kê:\n\n{e}")

    # =========================================================
    # CÀI ĐẶT
    # =========================================================

    def show_settings_message(self):
        try:
            self.settings_window = SettingsWindow()
            self.settings_window.show()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể mở Cài đặt:\n\n{e}")

    # =========================================================
    # ĐĂNG XUẤT
    # =========================================================

    def logout(self):

        reply = QMessageBox.question(
            self,
            "Đăng xuất",
            "Bạn có chắc muốn đăng xuất khỏi hệ thống không?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Đóng các cửa sổ con đang mở để tránh cửa sổ cũ còn tồn tại
            for window in (
                self.medicine_window,
                self.inventory_window,
                self.sale_window,
                self.invoice_window,
                self.stock_import_window,
                self.customer_window,
                self.statistics_window,
                self.settings_window,
            ):
                if window is not None:
                    window.close()

            from screens.login import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
            self.close()


# =============================================================
# CHẠY THỬ DASHBOARD
# =============================================================

if __name__ == "__main__":

    import sys

    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    window = DashboardWindow()

    window.show()

    sys.exit(
        app.exec()
    )