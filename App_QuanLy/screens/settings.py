from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QApplication
)

from PySide6.QtCore import Qt


class SettingsWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Nhà thuốc Ý Như - Cài đặt")
        self.setMinimumSize(900, 760)

        # Lưu các tiêu đề
        self.pharmacy_title = None
        self.account_title = None
        self.system_title = None

        self.create_ui()

    # ==================================================
    # TẠO GIAO DIỆN
    # ==================================================

    def create_ui(self):

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            30, 25, 30, 25
        )

        main_layout.setSpacing(12)

        # ==================================================
        # TIÊU ĐỀ
        # ==================================================

        self.title = QLabel(
            "⚙️  CÀI ĐẶT"
        )

        self.title.setObjectName(
            "pageTitle"
        )

        self.subtitle = QLabel(
            "Thiết lập thông tin cho hệ thống nhà thuốc"
        )

        self.subtitle.setObjectName(
            "pageSubtitle"
        )

        main_layout.addWidget(
            self.title
        )

        main_layout.addWidget(
            self.subtitle
        )

        # ==================================================
        # CARD CHÍNH
        # ==================================================

        card = QFrame()

        card.setObjectName(
            "mainCard"
        )

        card_layout = QVBoxLayout()

        card_layout.setContentsMargins(
            25, 20, 25, 25
        )

        card_layout.setSpacing(12)

        # ==================================================
        # 1. THÔNG TIN NHÀ THUỐC
        # ==================================================

        self.pharmacy_title = QLabel(
            "🏪  Thông tin nhà thuốc"
        )

        self.pharmacy_title.setObjectName(
            "sectionTitle"
        )

        card_layout.addWidget(
            self.pharmacy_title
        )

        card_layout.addSpacing(5)

        # Tên nhà thuốc
        card_layout.addWidget(
            self.create_info_row(
                "🏪",
                "Tên nhà thuốc",
                "Nhà thuốc Ý Như",
                "Tên hiển thị của nhà thuốc trong hệ thống."
            )
        )

        # Địa chỉ
        card_layout.addWidget(
            self.create_info_row(
                "📍",
                "Địa chỉ",
                "Cần Thơ",
                "Địa chỉ của nhà thuốc."
            )
        )

        # Số điện thoại
        card_layout.addWidget(
            self.create_info_row(
                "📞",
                "Số điện thoại",
                "Chưa cập nhật",
                "Số điện thoại liên hệ của nhà thuốc."
            )
        )

        # ==================================================
        # 2. TÀI KHOẢN
        # ==================================================

        self.account_title = QLabel(
            "👤  Tài khoản"
        )

        self.account_title.setObjectName(
            "sectionTitle"
        )

        card_layout.addSpacing(10)

        card_layout.addWidget(
            self.account_title
        )

        card_layout.addSpacing(5)

        card_layout.addWidget(
            self.create_info_row(
                "👑",
                "Quyền tài khoản",
                "Quản trị viên",
                "Tài khoản hiện tại có quyền quản trị hệ thống."
            )
        )

        # ==================================================
        # 3. HỆ THỐNG
        # ==================================================

        self.system_title = QLabel(
            "💻  Hệ thống"
        )

        self.system_title.setObjectName(
            "sectionTitle"
        )

        card_layout.addSpacing(10)

        card_layout.addWidget(
            self.system_title
        )

        card_layout.addSpacing(5)

        card_layout.addWidget(
            self.create_info_row(
                "🗄️",
                "Cơ sở dữ liệu",
                "SQLite - pharmacy.db",
                "Cơ sở dữ liệu đang được sử dụng."
            )
        )

        card_layout.addWidget(
            self.create_info_row(
                "ℹ️",
                "Phiên bản",
                "1.0.0",
                "Phiên bản hiện tại của ứng dụng."
            )
        )

        card.setLayout(
            card_layout
        )

        main_layout.addWidget(
            card
        )

        # ==================================================
        # NÚT ĐÓNG
        # ==================================================

        button_layout = QHBoxLayout()

        button_layout.addStretch()

        self.close_button = QPushButton(
            "Đóng"
        )

        self.close_button.setObjectName(
            "closeButton"
        )

        self.close_button.setMinimumSize(
            120,
            42
        )

        self.close_button.clicked.connect(
            self.close
        )

        button_layout.addWidget(
            self.close_button
        )

        main_layout.addLayout(
            button_layout
        )

        self.setLayout(
            main_layout
        )

        # Áp dụng giao diện
        self.apply_theme()

    # ==================================================
    # DÒNG THÔNG TIN
    # ==================================================

    def create_info_row(
        self,
        icon,
        title,
        value,
        description
    ):

        frame = QFrame()

        frame.setObjectName(
            "settingRow"
        )

        frame.setMinimumHeight(
            70
        )

        layout = QHBoxLayout()

        layout.setContentsMargins(
            15,
            10,
            15,
            10
        )

        layout.setSpacing(
            15
        )

        # ----------------------------------------------
        # BÊN TRÁI
        # ----------------------------------------------

        left_layout = QVBoxLayout()

        left_layout.setSpacing(
            3
        )

        title_label = QLabel(
            icon + "  " + title
        )

        title_label.setObjectName(
            "settingTitle"
        )

        description_label = QLabel(
            description
        )

        description_label.setObjectName(
            "settingDescription"
        )

        left_layout.addWidget(
            title_label
        )

        left_layout.addWidget(
            description_label
        )

        layout.addLayout(
            left_layout,
            1
        )

        # ----------------------------------------------
        # BÊN PHẢI
        # ----------------------------------------------

        value_label = QLabel(
            value
        )

        value_label.setObjectName(
            "valueLabel"
        )

        value_label.setMinimumWidth(
            220
        )

        value_label.setAlignment(
            Qt.AlignRight |
            Qt.AlignVCenter
        )

        layout.addWidget(
            value_label
        )

        frame.setLayout(
            layout
        )

        return frame

    # ==================================================
    # GIAO DIỆN
    # ==================================================

    def apply_theme(self):

        self.setStyleSheet("""
            QWidget {
                font-family: "Segoe UI";
                color: #1F2937;
                background-color: #F5F7FA;
            }

            QFrame#mainCard {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 14px;
            }

            QFrame#settingRow {
                background-color: #F8FAFC;
                border: 1px solid #E5E7EB;
                border-radius: 10px;
            }

            QLabel#pageTitle {
                color: #0F766E;
                font-size: 28px;
                font-weight: bold;
                background-color: transparent;
            }

            QLabel#pageSubtitle {
                color: #6B7280;
                font-size: 13px;
                background-color: transparent;
            }

            QLabel#sectionTitle {
                color: #0F766E;
                font-size: 17px;
                font-weight: bold;
                background-color: transparent;
            }

            QLabel#settingTitle {
                color: #1F2937;
                font-size: 14px;
                font-weight: bold;
                background-color: transparent;
            }

            QLabel#settingDescription {
                color: #6B7280;
                font-size: 12px;
                background-color: transparent;
            }

            QLabel#valueLabel {
                color: #0F766E;
                font-size: 13px;
                font-weight: bold;
                background-color: transparent;
            }

            QPushButton#closeButton {
                background-color: #0F766E;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 10px 22px;
                font-weight: bold;
            }

            QPushButton#closeButton:hover {
                background-color: #115E59;
            }
        """)


# ==================================================
# CHẠY RIÊNG
# ==================================================

if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)

    window = SettingsWindow()

    window.show()

    sys.exit(
        app.exec()
    )