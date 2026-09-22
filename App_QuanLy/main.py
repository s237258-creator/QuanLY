import sys

from PySide6.QtWidgets import QApplication

from database.database import create_database
from screens.login import LoginWindow
from styles.theme import apply_theme


if __name__ == "__main__":

    # Tạo database khi mở app
    create_database()

    # Khởi tạo ứng dụng

    app = QApplication(sys.argv)

    # Áp dụng giao diện chung
    apply_theme(app)

    # Mở màn hình đăng nhập
    window = LoginWindow()
    window.show()

    sys.exit(app.exec())