from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QMessageBox
)

from PySide6.QtCore import Qt

from database.database import get_connection
from screens.dashboard import DashboardWindow


class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()

        # ==================================================
        # LƯU CỬA SỔ DASHBOARD
        # ==================================================

        self.dashboard = None
        self.register_dialog = None

        # ==================================================
        # CẤU HÌNH CỬA SỔ
        # ==================================================

        self.setWindowTitle(
            "Đăng nhập - Nhà thuốc Ý Như"
        )

        self.setFixedSize(
            500,
            680
        )

        # ==================================================
        # STYLE
        # ==================================================

        self.setStyleSheet("""

            QWidget {
                font-family: "Segoe UI";
                background-color: #F8FAFC;
            }

            QFrame#loginCard {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 20px;
            }

            QLabel#logo {
                font-size: 46px;
                border: none;
                background: transparent;
            }

            QLabel#title {
                color: #0F766E;
                font-size: 26px;
                font-weight: bold;
                border: none;
                background: transparent;
            }

            QLabel#subtitle {
                color: #6B7280;
                font-size: 14px;
                border: none;
                background: transparent;
            }

            QLabel#fieldLabel {
                color: #374151;
                font-size: 13px;
                font-weight: bold;
                border: none;
                background: transparent;
            }

            QLineEdit {
                background-color: #F9FAFB;
                border: 1px solid #D1D5DB;
                border-radius: 10px;
                padding: 11px;
                font-size: 14px;
                color: #1F2937;
            }

            QLineEdit:focus {
                background-color: white;
                border: 2px solid #14B8A6;
            }

            QPushButton#loginButton {
                background-color: #0F766E;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 13px;
                font-size: 15px;
                font-weight: bold;
            }

            QPushButton#loginButton:hover {
                background-color: #115E59;
            }

            QPushButton#loginButton:pressed {
                background-color: #134E4A;
            }

            QPushButton#registerButton {
                background-color: white;
                color: #0F766E;
                border: 1px solid #14B8A6;
                border-radius: 10px;
                padding: 11px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton#registerButton:hover {
                background-color: #ECFDF5;
            }

            QPushButton#showPasswordButton {
                background-color: #F9FAFB;
                color: #374151;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                font-size: 14px;
                padding: 5px 10px;
            }

            QPushButton#showPasswordButton:hover {
                background-color: #ECFDF5;
                color: #0F766E;
            }

            QLabel#footer {
                color: #9CA3AF;
                font-size: 12px;
                border: none;
                background: transparent;
            }

            QLabel#roleLabel {
                color: #0F766E;
                background-color: #ECFDF5;
                border-radius: 8px;
                padding: 8px;
                font-size: 13px;
                font-weight: bold;
            }

        """)

        # ==================================================
        # KHUNG ĐĂNG NHẬP
        # ==================================================

        card = QFrame()

        card.setObjectName(
            "loginCard"
        )

        # ==================================================
        # LOGO
        # ==================================================

        logo = QLabel(
            "💊"
        )

        logo.setObjectName(
            "logo"
        )

        logo.setAlignment(
            Qt.AlignCenter
        )

        # ==================================================
        # TÊN NHÀ THUỐC
        # ==================================================

        title = QLabel(
            "NHÀ THUỐC Ý NHƯ"
        )

        title.setObjectName(
            "title"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        # ==================================================
        # MÔ TẢ
        # ==================================================

        subtitle = QLabel(
            "Hệ thống quản lý nhà thuốc"
        )

        subtitle.setObjectName(
            "subtitle"
        )

        subtitle.setAlignment(
            Qt.AlignCenter
        )

        # ==================================================
        # NHÃN TÀI KHOẢN
        # ==================================================

        username_label = QLabel(
            "Tên tài khoản"
        )

        username_label.setObjectName(
            "fieldLabel"
        )

        # ==================================================
        # Ô TÀI KHOẢN
        # ==================================================

        self.username = QLineEdit()

        self.username.setPlaceholderText(
            "Nhập tên tài khoản"
        )

        self.username.setMinimumHeight(
            44
        )

        # ==================================================
        # NHÃN MẬT KHẨU
        # ==================================================

        password_label = QLabel(
            "Mật khẩu"
        )

        password_label.setObjectName(
            "fieldLabel"
        )

        # ==================================================
        # Ô MẬT KHẨU + HIỆN / ẨN
        # ==================================================

        password_layout = QHBoxLayout()

        password_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        password_layout.setSpacing(
            5
        )

        self.password = QLineEdit()

        self.password.setPlaceholderText(
            "Nhập mật khẩu"
        )

        self.password.setEchoMode(
            QLineEdit.Password
        )

        self.password.setMinimumHeight(
            44
        )

        self.show_password_button = QPushButton(
            "👁"
        )

        self.show_password_button.setObjectName(
            "showPasswordButton"
        )

        self.show_password_button.setFixedSize(
            48,
            44
        )

        self.show_password_button.setToolTip(
            "Hiện / ẩn mật khẩu"
        )

        self.show_password_button.clicked.connect(
            self.toggle_password
        )

        password_layout.addWidget(
            self.password
        )

        password_layout.addWidget(
            self.show_password_button
        )

        self.password.returnPressed.connect(
            self.login
        )

        # ==================================================
        # NÚT ĐĂNG NHẬP
        # ==================================================

        login_button = QPushButton(
            "🔐  ĐĂNG NHẬP"
        )

        login_button.setObjectName(
            "loginButton"
        )

        login_button.setMinimumHeight(
            46
        )

        login_button.clicked.connect(
            self.login
        )

        # ==================================================
        # NÚT ĐĂNG KÝ
        # ==================================================

        register_button = QPushButton(
            "📝  ĐĂNG KÝ TÀI KHOẢN"
        )

        register_button.setObjectName(
            "registerButton"
        )

        register_button.setMinimumHeight(
            44
        )

        register_button.clicked.connect(
            self.register_account
        )

        # ==================================================
        # VAI TRÒ
        # ==================================================

        role_label = QLabel(
            "👑  Tài khoản đăng ký: Quản trị viên"
        )

        role_label.setObjectName(
            "roleLabel"
        )

        role_label.setAlignment(
            Qt.AlignCenter
        )

        # ==================================================
        # FOOTER
        # ==================================================

        footer = QLabel(
            "Uy tín • Tận tâm • Vì sức khỏe cộng đồng"
        )

        footer.setObjectName(
            "footer"
        )

        footer.setAlignment(
            Qt.AlignCenter
        )

        # ==================================================
        # LAYOUT CARD
        # ==================================================

        card_layout = QVBoxLayout()

        card_layout.setContentsMargins(
            45,
            30,
            45,
            28
        )

        card_layout.setSpacing(
            9
        )

        card_layout.addWidget(
            logo
        )

        card_layout.addWidget(
            title
        )

        card_layout.addWidget(
            subtitle
        )

        card_layout.addSpacing(
            18
        )

        card_layout.addWidget(
            username_label
        )

        card_layout.addWidget(
            self.username
        )

        card_layout.addSpacing(
            5
        )

        card_layout.addWidget(
            password_label
        )

        card_layout.addLayout(
            password_layout
        )

        card_layout.addSpacing(
            13
        )

        card_layout.addWidget(
            login_button
        )

        card_layout.addSpacing(
            7
        )

        card_layout.addWidget(
            register_button
        )

        card_layout.addSpacing(
            10
        )

        card_layout.addWidget(
            role_label
        )

        card_layout.addSpacing(
            12
        )

        card_layout.addWidget(
            footer
        )

        card.setLayout(
            card_layout
        )

        # ==================================================
        # LAYOUT CHÍNH
        # ==================================================

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            35,
            25,
            35,
            25
        )

        main_layout.addStretch()

        main_layout.addWidget(
            card
        )

        main_layout.addStretch()

        self.setLayout(
            main_layout
        )

        self.username.setFocus()

    # ==================================================
    # HIỆN / ẨN MẬT KHẨU
    # ==================================================

    def toggle_password(self):

        if self.password.echoMode() == QLineEdit.Password:

            self.password.setEchoMode(
                QLineEdit.Normal
            )

            self.show_password_button.setText(
                "🙈"
            )

            self.show_password_button.setToolTip(
                "Ẩn mật khẩu"
            )

        else:

            self.password.setEchoMode(
                QLineEdit.Password
            )

            self.show_password_button.setText(
                "👁"
            )

            self.show_password_button.setToolTip(
                "Hiện mật khẩu"
            )

    # ==================================================
    # ĐĂNG NHẬP
    # ==================================================

    def login(self):

        username = self.username.text().strip()
        password = self.password.text()

        if not username or not password:

            QMessageBox.warning(
                self,
                "Thông báo",
                "⚠️ Vui lòng nhập đầy đủ tài khoản và mật khẩu!"
            )

            return

        try:

            connection = get_connection()

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    username,
                    full_name,
                    role
                FROM users
                WHERE username = ?
                AND password = ?
                """,
                (
                    username,
                    password
                )
            )

            user = cursor.fetchone()

            connection.close()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Lỗi",
                f"Không thể kết nối database!\n\n{error}"
            )

            return

        if user:

            self.dashboard = DashboardWindow()

            self.dashboard.show()

            self.close()

        else:

            QMessageBox.warning(
                self,
                "Đăng nhập",
                "❌ Tên tài khoản hoặc mật khẩu không đúng!"
            )

    # ==================================================
    # ĐĂNG KÝ TÀI KHOẢN
    # ==================================================

    def register_account(self):

        # ==================================================
        # TẠO CỬA SỔ ĐĂNG KÝ
        # ==================================================

        dialog = QWidget()

        self.register_dialog = dialog

        dialog.setWindowTitle(
            "Đăng ký tài khoản"
        )

        # TĂNG KÍCH THƯỚC
        dialog.setFixedSize(
            500,
            500
        )

        dialog.setStyleSheet("""
            QWidget {
                font-family: "Segoe UI";
                background-color: #F8FAFC;
            }

            QFrame#registerCard {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 18px;
            }

            QLabel#registerTitle {
                color: #0F766E;
                font-size: 22px;
                font-weight: bold;
                background: transparent;
            }

            QLabel#registerLabel {
                color: #374151;
                font-size: 13px;
                font-weight: bold;
                background: transparent;
            }

            QLineEdit {
                background-color: #F9FAFB;
                color: #1F2937;
                border: 1px solid #D1D5DB;
                border-radius: 9px;
                padding: 9px 10px;
                font-size: 14px;
            }

            QLineEdit:focus {
                background-color: white;
                border: 2px solid #14B8A6;
            }

            QLabel#roleLabel {
                color: #0F766E;
                background-color: #ECFDF5;
                border-radius: 8px;
                padding: 8px;
                font-size: 13px;
                font-weight: bold;
            }

            QPushButton#registerConfirm {
                background-color: #0F766E;
                color: white;
                border: none;
                border-radius: 9px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton#registerConfirm:hover {
                background-color: #115E59;
            }

            QPushButton#cancelButton {
                background-color: #E5E7EB;
                color: #374151;
                border: none;
                border-radius: 9px;
                padding: 10px;
                font-size: 14px;
            }

            QPushButton#cancelButton:hover {
                background-color: #D1D5DB;
            }
        """)

        # ==================================================
        # CARD
        # ==================================================

        card = QFrame()

        card.setObjectName(
            "registerCard"
        )

        card_layout = QVBoxLayout()

        # Khoảng cách bên trong card
        card_layout.setContentsMargins(
            30,
            25,
            30,
            25
        )

        card_layout.setSpacing(
            8
        )

        # ==================================================
        # TIÊU ĐỀ
        # ==================================================

        title = QLabel(
            "📝  ĐĂNG KÝ TÀI KHOẢN"
        )

        title.setObjectName(
            "registerTitle"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        card_layout.addWidget(
            title
        )

        card_layout.addSpacing(
            8
        )

        # ==================================================
        # TÊN TÀI KHOẢN
        # ==================================================

        username_label = QLabel(
            "Tên tài khoản"
        )

        username_label.setObjectName(
            "registerLabel"
        )

        card_layout.addWidget(
            username_label
        )

        username_input = QLineEdit()

        username_input.setText(
            self.username.text().strip()
        )

        username_input.setPlaceholderText(
            "Nhập tên tài khoản"
        )

        username_input.setMinimumHeight(
            42
        )

        card_layout.addWidget(
            username_input
        )

        # ==================================================
        # MẬT KHẨU
        # ==================================================

        password_label = QLabel(
            "Mật khẩu"
        )

        password_label.setObjectName(
            "registerLabel"
        )

        card_layout.addWidget(
            password_label
        )

        password_box = QLineEdit()

        password_box.setPlaceholderText(
            "Nhập mật khẩu"
        )

        password_box.setEchoMode(
            QLineEdit.Password
        )

        password_box.setMinimumHeight(
            42
        )

        card_layout.addWidget(
            password_box
        )

        # ==================================================
        # XÁC NHẬN MẬT KHẨU
        # ==================================================

        confirm_label = QLabel(
            "Xác nhận mật khẩu"
        )

        confirm_label.setObjectName(
            "registerLabel"
        )

        card_layout.addWidget(
            confirm_label
        )

        confirm_box = QLineEdit()

        confirm_box.setPlaceholderText(
            "Nhập lại mật khẩu"
        )

        confirm_box.setEchoMode(
            QLineEdit.Password
        )

        confirm_box.setMinimumHeight(
            42
        )

        card_layout.addWidget(
            confirm_box
        )

        # ==================================================
        # VAI TRÒ
        # ==================================================

        role_label = QLabel(
            "👑  Vai trò: Quản trị viên"
        )

        role_label.setObjectName(
            "roleLabel"
        )

        role_label.setAlignment(
            Qt.AlignCenter
        )

        card_layout.addWidget(
            role_label
        )

        card_layout.addSpacing(
            8
        )

        # ==================================================
        # NÚT
        # ==================================================

        button_layout = QHBoxLayout()

        button_layout.setSpacing(
            10
        )

        register_confirm = QPushButton(
            "✅  Đăng ký"
        )

        register_confirm.setObjectName(
            "registerConfirm"
        )

        register_confirm.setMinimumHeight(
            44
        )

        cancel_button = QPushButton(
            "❌  Hủy"
        )

        cancel_button.setObjectName(
            "cancelButton"
        )

        cancel_button.setMinimumHeight(
            44
        )

        button_layout.addWidget(
            register_confirm
        )

        button_layout.addWidget(
            cancel_button
        )

        card_layout.addLayout(
            button_layout
        )

        card.setLayout(
            card_layout
        )

        # ==================================================
        # LAYOUT CỬA SỔ
        # ==================================================

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        main_layout.addWidget(
            card
        )

        dialog.setLayout(
            main_layout
        )

        # ==================================================
        # HÀM ĐĂNG KÝ
        # ==================================================

        def do_register():

            new_username = (
                username_input.text().strip()
            )

            new_password = (
                password_box.text()
            )

            confirm_password = (
                confirm_box.text()
            )

            # --------------------------------------------------
            # KIỂM TRA TÀI KHOẢN
            # --------------------------------------------------

            if not new_username:

                QMessageBox.warning(
                    dialog,
                    "Thông báo",
                    "⚠️ Vui lòng nhập tên tài khoản!"
                )

                username_input.setFocus()

                return

            # --------------------------------------------------
            # KIỂM TRA MẬT KHẨU
            # --------------------------------------------------

            if not new_password:

                QMessageBox.warning(
                    dialog,
                    "Thông báo",
                    "⚠️ Vui lòng nhập mật khẩu!"
                )

                password_box.setFocus()

                return

            # --------------------------------------------------
            # KIỂM TRA XÁC NHẬN
            # --------------------------------------------------

            if not confirm_password:

                QMessageBox.warning(
                    dialog,
                    "Thông báo",
                    "⚠️ Vui lòng xác nhận mật khẩu!"
                )

                confirm_box.setFocus()

                return

            # --------------------------------------------------
            # KIỂM TRA MẬT KHẨU
            # --------------------------------------------------

            if new_password != confirm_password:

                QMessageBox.warning(
                    dialog,
                    "Thông báo",
                    "⚠️ Mật khẩu xác nhận không khớp!"
                )

                confirm_box.clear()

                confirm_box.setFocus()

                return

            # ==================================================
            # DATABASE
            # ==================================================

            try:

                connection = get_connection()

                cursor = connection.cursor()

                cursor.execute(
                    """
                    SELECT id
                    FROM users
                    WHERE username = ?
                    """,
                    (
                        new_username,
                    )
                )

                existing_user = cursor.fetchone()

                if existing_user:

                    connection.close()

                    QMessageBox.warning(
                        dialog,
                        "Đăng ký",
                        "⚠️ Tên tài khoản đã tồn tại!"
                    )

                    username_input.setFocus()

                    return

                # --------------------------------------------------
                # THÊM TÀI KHOẢN
                # --------------------------------------------------

                cursor.execute(
                    """
                    INSERT INTO users
                    (
                        username,
                        password,
                        full_name,
                        role
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        new_username,
                        new_password,
                        "Quản trị viên",
                        "admin"
                    )
                )

                connection.commit()

                connection.close()

            except Exception as error:

                QMessageBox.critical(
                    dialog,
                    "Lỗi",
                    f"Không thể đăng ký tài khoản!\n\n{error}"
                )

                return

            # ==================================================
            # THÔNG BÁO THÀNH CÔNG
            # ==================================================

            QMessageBox.information(
                dialog,
                "Đăng ký thành công",
                "✅ Đăng ký tài khoản thành công!\n\n"
                "Vai trò: Quản trị viên\n\n"
                "Bạn có thể sử dụng tài khoản này để đăng nhập."
            )

            # Điền tài khoản vừa đăng ký
            self.username.setText(
                new_username
            )

            self.password.clear()

            dialog.close()

            self.password.setFocus()

        # ==================================================
        # KẾT NỐI NÚT
        # ==================================================

        register_confirm.clicked.connect(
            do_register
        )

        cancel_button.clicked.connect(
            dialog.close
        )

        confirm_box.returnPressed.connect(
            do_register
        )

        # ==================================================
        # HIỂN THỊ
        # ==================================================

        dialog.show()

        username_input.setFocus()


# ==========================================================
# CHẠY RIÊNG
# ==========================================================

if __name__ == "__main__":

    import sys

    from PySide6.QtWidgets import QApplication

    app = QApplication(
        sys.argv
    )

    window = LoginWindow()

    window.show()

    sys.exit(
        app.exec()
    )