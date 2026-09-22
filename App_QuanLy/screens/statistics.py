import sqlite3

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QComboBox
)

from PySide6.QtCore import Qt
from pathlib import Path


# ============================================================
# ĐƯỜNG DẪN DATABASE
# ============================================================

DATABASE = Path(__file__).resolve().parent.parent / "pharmacy.db"


# ============================================================
# CỬA SỔ THỐNG KÊ
# ============================================================

class StatisticsWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("📊 Thống kê - Nhà thuốc Ý Như")
        self.setMinimumSize(1200, 750)

        self.create_ui()
        self.load_statistics()

    # ========================================================
    # KẾT NỐI DATABASE
    # ========================================================

    def get_connection(self):
        return sqlite3.connect(DATABASE)

    # ========================================================
    # TẠO GIAO DIỆN
    # ========================================================

    def create_ui(self):

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            30,
            25,
            30,
            25
        )

        main_layout.setSpacing(14)

        # ====================================================
        # TIÊU ĐỀ
        # ====================================================

        title = QLabel("📊  THỐNG KÊ NHÀ THUỐC")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Theo dõi doanh thu, hóa đơn, thuốc đã bán và tình hình tồn kho"
        )
        subtitle.setObjectName("pageSubtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # ====================================================
        # THANH CÔNG CỤ
        # ====================================================

        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        period_label = QLabel("Thời gian:")
        period_label.setObjectName("toolbarLabel")

        toolbar.addWidget(period_label)

        self.period_combo = QComboBox()

        self.period_combo.addItems([
            "Tất cả",
            "Hôm nay",
            "Tháng này"
        ])

        self.period_combo.setFixedSize(
            160,
            40
        )

        toolbar.addWidget(self.period_combo)

        self.period_combo.currentIndexChanged.connect(
            self.load_statistics
        )

        toolbar.addStretch()

        # NÚT LÀM MỚI

        refresh_button = QPushButton(
            "🔄  Làm mới"
        )

        refresh_button.setObjectName(
            "refreshButton"
        )

        refresh_button.setFixedSize(
            120,
            40
        )

        refresh_button.clicked.connect(
            self.load_statistics
        )

        toolbar.addWidget(refresh_button)

        # NÚT ĐÓNG

        close_button = QPushButton(
            "✖  Đóng"
        )

        close_button.setObjectName(
            "closeButton"
        )

        close_button.setFixedSize(
            100,
            40
        )

        close_button.clicked.connect(
            self.close
        )

        toolbar.addWidget(close_button)

        main_layout.addLayout(toolbar)

        # ====================================================
        # CÁC THẺ THỐNG KÊ
        # ====================================================

        cards_layout = QGridLayout()
        cards_layout.setSpacing(15)

        # DOANH THU

        self.revenue_card = self.create_stat_card(
            "💰",
            "DOANH THU",
            "0 đ"
        )

        # HÓA ĐƠN

        self.invoice_card = self.create_stat_card(
            "🧾",
            "HÓA ĐƠN",
            "0"
        )

        # THUỐC ĐÃ BÁN

        self.sold_card = self.create_stat_card(
            "💊",
            "THUỐC ĐÃ BÁN",
            "0"
        )

        # TỒN KHO

        self.inventory_card = self.create_stat_card(
            "📦",
            "TỒN KHO",
            "0"
        )

        cards_layout.addWidget(
            self.revenue_card,
            0,
            0
        )

        cards_layout.addWidget(
            self.invoice_card,
            0,
            1
        )

        cards_layout.addWidget(
            self.sold_card,
            0,
            2
        )

        cards_layout.addWidget(
            self.inventory_card,
            0,
            3
        )

        main_layout.addLayout(
            cards_layout
        )

        # ====================================================
        # KHU VỰC 2 BẢNG
        # ====================================================

        content_layout = QHBoxLayout()
        content_layout.setSpacing(15)

        # ====================================================
        # THUỐC BÁN CHẠY
        # ====================================================

        best_selling_frame = QFrame()

        best_selling_frame.setObjectName(
            "contentCard"
        )

        best_selling_layout = QVBoxLayout()

        best_selling_layout.setContentsMargins(
            18,
            18,
            18,
            18
        )

        best_selling_layout.setSpacing(10)

        best_selling_title = QLabel(
            "🔥  THUỐC BÁN CHẠY"
        )

        best_selling_title.setObjectName(
            "sectionTitle"
        )

        best_selling_layout.addWidget(
            best_selling_title
        )

        self.best_selling_table = QTableWidget()

        self.best_selling_table.setColumnCount(4)

        self.best_selling_table.setHorizontalHeaderLabels([
            "STT",
            "Tên thuốc",
            "Số lượng bán",
            "Doanh thu"
        ])

        self.setup_table(
            self.best_selling_table
        )

        best_selling_layout.addWidget(
            self.best_selling_table
        )

        best_selling_frame.setLayout(
            best_selling_layout
        )

        # ====================================================
        # TỒN KHO
        # ====================================================

        inventory_frame = QFrame()

        inventory_frame.setObjectName(
            "contentCard"
        )

        inventory_layout = QVBoxLayout()

        inventory_layout.setContentsMargins(
            18,
            18,
            18,
            18
        )

        inventory_layout.setSpacing(10)

        inventory_title = QLabel(
            "📦  TÌNH HÌNH TỒN KHO"
        )

        inventory_title.setObjectName(
            "sectionTitle"
        )

        inventory_layout.addWidget(
            inventory_title
        )

        self.inventory_table = QTableWidget()

        self.inventory_table.setColumnCount(5)

        self.inventory_table.setHorizontalHeaderLabels([
            "STT",
            "Tên thuốc",
            "Loại",
            "Số lượng",
            "Hạn sử dụng"
        ])

        self.setup_table(
            self.inventory_table
        )

        inventory_layout.addWidget(
            self.inventory_table
        )

        inventory_frame.setLayout(
            inventory_layout
        )

        content_layout.addWidget(
            best_selling_frame,
            1
        )

        content_layout.addWidget(
            inventory_frame,
            1
        )

        main_layout.addLayout(
            content_layout
        )

        # ====================================================
        # TRẠNG THÁI
        # ====================================================

        self.status_label = QLabel(
            "🟢  Đã tải dữ liệu thống kê"
        )

        self.status_label.setObjectName(
            "statusLabel"
        )

        main_layout.addWidget(
            self.status_label
        )

        self.setLayout(
            main_layout
        )

        # ====================================================
        # STYLE TOÀN BỘ GIAO DIỆN
        # ====================================================

        self.apply_theme()

    # ========================================================
    # TẠO THẺ THỐNG KÊ
    # ========================================================

    def create_stat_card(
        self,
        icon,
        title,
        value
    ):

        card = QFrame()

        card.setObjectName(
            "statCard"
        )

        card.setMinimumHeight(
            125
        )

        layout = QVBoxLayout()

        layout.setContentsMargins(
            20,
            17,
            20,
            17
        )

        layout.setSpacing(5)

        # ICON + TIÊU ĐỀ

        header_layout = QHBoxLayout()

        icon_label = QLabel(
            icon
        )

        icon_label.setObjectName(
            "cardIcon"
        )

        header_layout.addWidget(
            icon_label
        )

        title_label = QLabel(
            title
        )

        title_label.setObjectName(
            "cardTitle"
        )

        header_layout.addWidget(
            title_label
        )

        header_layout.addStretch()

        layout.addLayout(
            header_layout
        )

        # GIÁ TRỊ

        value_label = QLabel(
            value
        )

        value_label.setObjectName(
            "value_label"
        )

        layout.addWidget(
            value_label
        )

        card.setLayout(
            layout
        )

        return card

    # ========================================================
    # CÀI ĐẶT TABLE
    # ========================================================

    def setup_table(
        self,
        table
    ):

        table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        table.setSelectionMode(
            QTableWidget.SingleSelection
        )

        table.setAlternatingRowColors(
            True
        )

        table.verticalHeader().setVisible(
            False
        )

        table.horizontalHeader().setStretchLastSection(
            True
        )

        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        table.setStyleSheet("""
            QTableWidget {
                background-color: #FFFFFF;
                alternate-background-color: #F8FAFC;
                border: none;
                gridline-color: #E5E7EB;
                font-family: "Segoe UI";
                font-size: 13px;
                color: #1F2937;
            }

            QTableWidget::item {
                padding: 7px;
                border-bottom: 1px solid #F1F5F9;
            }

            QTableWidget::item:selected {
                background-color: #CCFBF1;
                color: #134E4A;
            }

            QHeaderView::section {
                background-color: #F0FDFA;
                color: #115E59;
                font-family: "Segoe UI";
                font-size: 13px;
                font-weight: bold;
                padding: 9px;
                border: none;
                border-bottom: 1px solid #D1FAE5;
            }
        """)

    # ========================================================
    # FORMAT TIỀN
    # ========================================================

    def format_money(
        self,
        value
    ):

        try:

            value = float(
                value
            )

            return f"{value:,.0f} đ"

        except:

            return "0 đ"

    # ========================================================
    # LẤY ĐIỀU KIỆN THỜI GIAN
    # ========================================================

    def get_time_condition(self):

        period = self.period_combo.currentText()

        if period == "Hôm nay":

            return """
                AND date(i.created_at)
                    = date('now', 'localtime')
            """

        elif period == "Tháng này":

            return """
                AND strftime('%Y-%m', i.created_at)
                    = strftime('%Y-%m', 'now', 'localtime')
            """

        return ""

    # ========================================================
    # LOAD TOÀN BỘ THỐNG KÊ
    # ========================================================

    def load_statistics(
        self
    ):

        try:

            connection = self.get_connection()

            cursor = connection.cursor()

            time_condition = (
                self.get_time_condition()
            )

            # =================================================
            # DOANH THU
            # =================================================

            revenue_query = f"""
                SELECT
                    COALESCE(SUM(i.total), 0)
                FROM invoices i
                WHERE i.payment_status = 'Đã thanh toán'
                {time_condition}
            """

            cursor.execute(
                revenue_query
            )

            revenue = cursor.fetchone()[0]

            # =================================================
            # SỐ HÓA ĐƠN
            # =================================================

            invoice_query = f"""
                SELECT
                    COUNT(*)
                FROM invoices i
                WHERE i.payment_status = 'Đã thanh toán'
                {time_condition}
            """

            cursor.execute(
                invoice_query
            )

            invoice_count = (
                cursor.fetchone()[0]
            )

            # =================================================
            # TỔNG THUỐC ĐÃ BÁN
            # =================================================

            sold_query = f"""
                SELECT
                    COALESCE(SUM(d.quantity), 0)
                FROM invoice_details d
                INNER JOIN invoices i
                    ON d.invoice_id = i.id
                WHERE i.payment_status = 'Đã thanh toán'
                {time_condition}
            """

            cursor.execute(
                sold_query
            )

            sold_quantity = (
                cursor.fetchone()[0]
            )

            # =================================================
            # TỔNG TỒN KHO
            # =================================================

            cursor.execute("""
                SELECT
                    COALESCE(SUM(quantity), 0)
                FROM medicines
            """)

            inventory_quantity = (
                cursor.fetchone()[0]
            )

            # =================================================
            # CẬP NHẬT CARD
            # =================================================

            self.set_card_value(
                self.revenue_card,
                self.format_money(
                    revenue
                )
            )

            self.set_card_value(
                self.invoice_card,
                f"{invoice_count:,}"
            )

            self.set_card_value(
                self.sold_card,
                f"{sold_quantity:,}"
            )

            self.set_card_value(
                self.inventory_card,
                f"{inventory_quantity:,}"
            )

            # =================================================
            # THUỐC BÁN CHẠY
            # =================================================

            self.load_best_selling(
                cursor,
                time_condition
            )

            # =================================================
            # TỒN KHO
            # =================================================

            self.load_inventory(
                cursor
            )

            connection.close()

            self.status_label.setText(
                "🟢  Đã cập nhật dữ liệu thống kê"
            )

        except Exception as e:

            self.status_label.setText(
                "🔴  Có lỗi khi tải thống kê"
            )

            QMessageBox.critical(
                self,
                "Lỗi thống kê",
                f"Không thể tải dữ liệu thống kê:\n\n{e}"
            )

    # ========================================================
    # CẬP NHẬT GIÁ TRỊ CARD
    # ========================================================

    def set_card_value(
        self,
        card,
        value
    ):

        label = card.findChild(
            QLabel,
            "value_label"
        )

        if label:

            label.setText(
                value
            )

    # ========================================================
    # THUỐC BÁN CHẠY
    # ========================================================

    def load_best_selling(
        self,
        cursor,
        time_condition
    ):

        self.best_selling_table.setRowCount(
            0
        )

        query = f"""
            SELECT
                m.name,
                SUM(d.quantity) AS total_quantity,
                SUM(
                    d.quantity * d.price
                ) AS total_revenue

            FROM invoice_details d

            INNER JOIN medicines m
                ON d.medicine_id = m.id

            INNER JOIN invoices i
                ON d.invoice_id = i.id

            WHERE i.payment_status = 'Đã thanh toán'

            {time_condition}

            GROUP BY
                m.id,
                m.name

            ORDER BY
                total_quantity DESC

            LIMIT 10
        """

        cursor.execute(
            query
        )

        rows = cursor.fetchall()

        for index, row in enumerate(
            rows,
            start=1
        ):

            medicine_name = row[0]

            quantity = row[1]

            revenue = row[2]

            row_position = (
                self.best_selling_table.rowCount()
            )

            self.best_selling_table.insertRow(
                row_position
            )

            self.set_table_item(
                self.best_selling_table,
                row_position,
                0,
                str(index)
            )

            self.set_table_item(
                self.best_selling_table,
                row_position,
                1,
                str(medicine_name)
            )

            self.set_table_item(
                self.best_selling_table,
                row_position,
                2,
                f"{quantity:,}"
            )

            self.set_table_item(
                self.best_selling_table,
                row_position,
                3,
                self.format_money(
                    revenue
                )
            )

    # ========================================================
    # TỒN KHO
    # ========================================================

    def load_inventory(
        self,
        cursor
    ):

        self.inventory_table.setRowCount(
            0
        )

        cursor.execute("""
            SELECT
                name,
                category,
                quantity,
                expiry_date

            FROM medicines

            ORDER BY
                quantity ASC,
                name ASC
        """)

        rows = cursor.fetchall()

        for index, row in enumerate(
            rows,
            start=1
        ):

            medicine_name = row[0]

            category = row[1]

            quantity = row[2]

            expiry_date = row[3]

            row_position = (
                self.inventory_table.rowCount()
            )

            self.inventory_table.insertRow(
                row_position
            )

            self.set_table_item(
                self.inventory_table,
                row_position,
                0,
                str(index)
            )

            self.set_table_item(
                self.inventory_table,
                row_position,
                1,
                str(medicine_name)
            )

            self.set_table_item(
                self.inventory_table,
                row_position,
                2,
                str(category)
                if category
                else ""
            )

            self.set_table_item(
                self.inventory_table,
                row_position,
                3,
                f"{quantity:,}"
            )

            self.set_table_item(
                self.inventory_table,
                row_position,
                4,
                str(expiry_date)
                if expiry_date
                else ""
            )

    # ========================================================
    # SET TABLE ITEM
    # ========================================================

    def set_table_item(
        self,
        table,
        row,
        column,
        text
    ):

        item = QTableWidgetItem(
            text
        )

        item.setTextAlignment(
            Qt.AlignCenter
        )

        table.setItem(
            row,
            column,
            item
        )

    # ========================================================
    # GIAO DIỆN ĐỒNG BỘ TOÀN HỆ THỐNG
    # ========================================================

    def apply_theme(self):

        self.setStyleSheet("""

            /* ==========================================
               TOÀN BỘ CỬA SỔ
               ========================================== */

            QWidget {
                font-family: "Segoe UI";
                color: #1F2937;
                background-color: #F5F7FA;
            }


            /* ==========================================
               TIÊU ĐỀ
               ========================================== */

            QLabel#pageTitle {
                background-color: transparent;
                color: #0F766E;
                font-size: 28px;
                font-weight: bold;
                padding: 2px 0px;
            }

            QLabel#pageSubtitle {
                background-color: transparent;
                color: #6B7280;
                font-size: 13px;
                padding-bottom: 5px;
            }


            /* ==========================================
               THANH CÔNG CỤ
               ========================================== */

            QLabel#toolbarLabel {
                background-color: transparent;
                color: #374151;
                font-size: 13px;
                font-weight: bold;
            }


            QComboBox {
                background-color: #FFFFFF;
                color: #1F2937;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 13px;
            }

            QComboBox:hover {
                border: 1px solid #0F766E;
            }

            QComboBox:focus {
                border: 1px solid #0F766E;
            }

            QComboBox::drop-down {
                border: none;
                width: 28px;
            }


            /* ==========================================
               NÚT LÀM MỚI
               ========================================== */

            QPushButton#refreshButton {
                background-color: #0F766E;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
            }

            QPushButton#refreshButton:hover {
                background-color: #115E59;
            }

            QPushButton#refreshButton:pressed {
                background-color: #134E4A;
            }


            /* ==========================================
               NÚT ĐÓNG
               ========================================== */

            QPushButton#closeButton {
                background-color: #E5E7EB;
                color: #374151;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
            }

            QPushButton#closeButton:hover {
                background-color: #D1D5DB;
                color: #1F2937;
            }


            /* ==========================================
               CARD THỐNG KÊ
               ========================================== */

            QFrame#statCard {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 14px;
            }

            QFrame#statCard:hover {
                border: 1px solid #99F6E4;
            }


            QLabel#cardIcon {
                background-color: transparent;
                font-size: 25px;
            }

            QLabel#cardTitle {
                background-color: transparent;
                color: #6B7280;
                font-size: 13px;
                font-weight: bold;
            }

            QLabel#value_label {
                background-color: transparent;
                color: #0F766E;
                font-size: 25px;
                font-weight: bold;
                padding-top: 5px;
            }


            /* ==========================================
               CARD NỘI DUNG
               ========================================== */

            QFrame#contentCard {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 14px;
            }


            QLabel#sectionTitle {
                background-color: transparent;
                color: #0F766E;
                font-size: 17px;
                font-weight: bold;
                padding-bottom: 5px;
            }


            /* ==========================================
               TRẠNG THÁI
               ========================================== */

            QLabel#statusLabel {
                background-color: transparent;
                color: #16A34A;
                font-size: 12px;
                padding: 3px 0px;
            }

        """)


# ============================================================
# CHẠY RIÊNG FILE NẾU CẦN
# ============================================================

if __name__ == "__main__":

    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(
        sys.argv
    )

    window = StatisticsWindow()

    window.show()

    sys.exit(
        app.exec()
    )