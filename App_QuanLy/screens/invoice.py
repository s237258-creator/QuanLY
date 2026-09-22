from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QFrame,
    QHeaderView,
    QLineEdit,
    QDialog,
    QDialogButtonBox
)

from PySide6.QtCore import Qt

from database.database import get_connection

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class InvoiceWindow(QWidget):

    def __init__(self):
        super().__init__()

        # ==================================================
        # CẤU HÌNH CỬA SỔ
        # ==================================================

        self.setWindowTitle(
            "Hóa đơn - Nhà thuốc Ý Như"
        )

        self.setMinimumSize(
            1100,
            700
        )

        # ==================================================
        # FONT PDF
        # ==================================================

        self.font_normal = "Helvetica"
        self.font_bold = "Helvetica-Bold"

        self.register_pdf_fonts()

        # ==================================================
        # TẠO GIAO DIỆN
        # ==================================================

        self.create_ui()

        # ==================================================
        # TẢI DỮ LIỆU
        # ==================================================

        self.load_invoices()

    # ==================================================
    # ĐĂNG KÝ FONT PDF
    # ==================================================

    def register_pdf_fonts(self):

        try:

            pdfmetrics.registerFont(
                TTFont(
                    "Arial",
                    "C:/Windows/Fonts/arial.ttf"
                )
            )

            pdfmetrics.registerFont(
                TTFont(
                    "Arial-Bold",
                    "C:/Windows/Fonts/arialbd.ttf"
                )
            )

            self.font_normal = "Arial"
            self.font_bold = "Arial-Bold"

        except Exception:

            self.font_normal = "Helvetica"
            self.font_bold = "Helvetica-Bold"

    # ==================================================
    # TẠO GIAO DIỆN
    # ==================================================

    def create_ui(self):

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            25,
            20,
            25,
            20
        )

        main_layout.setSpacing(
            15
        )

        # ==================================================
        # HEADER
        # ==================================================

        header_layout = QHBoxLayout()

        # Icon

        icon = QLabel("🧾")

        icon.setFixedSize(
            55,
            55
        )

        icon.setAlignment(
            Qt.AlignCenter
        )

        icon.setStyleSheet("""
            QLabel {
                background-color: #E6FFFA;
                border-radius: 14px;
                font-size: 28px;
            }
        """)

        # Tiêu đề

        title_layout = QVBoxLayout()

        title_layout.setSpacing(
            2
        )

        title = QLabel(
            "Quản lý hóa đơn"
        )

        title.setStyleSheet("""
            QLabel {
                font-size: 25px;
                font-weight: 700;
                color: #134E4A;
            }
        """)

        subtitle = QLabel(
            "Theo dõi, xem chi tiết và xuất hóa đơn tại Nhà thuốc Ý Như"
        )

        subtitle.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #64748B;
            }
        """)

        title_layout.addWidget(
            title
        )

        title_layout.addWidget(
            subtitle
        )

        header_layout.addWidget(
            icon
        )

        header_layout.addSpacing(
            12
        )

        header_layout.addLayout(
            title_layout
        )

        header_layout.addStretch()

        # Số lượng hóa đơn

        self.invoice_count = QLabel(
            "0 hóa đơn"
        )

        self.invoice_count.setStyleSheet("""
            QLabel {
                background-color: #ECFDF5;
                color: #047857;
                border: 1px solid #A7F3D0;
                border-radius: 15px;
                padding: 7px 14px;
                font-size: 12px;
                font-weight: 600;
            }
        """)

        header_layout.addWidget(
            self.invoice_count
        )

        main_layout.addLayout(
            header_layout
        )

        # ==================================================
        # KHUNG TÌM KIẾM
        # ==================================================

        search_frame = QFrame()

        search_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
        """)

        search_layout = QHBoxLayout(
            search_frame
        )

        search_layout.setContentsMargins(
            12,
            10,
            12,
            10
        )

        search_label = QLabel(
            "🔎 Tìm kiếm:"
        )

        search_label.setStyleSheet("""
            QLabel {
                color: #334155;
                font-size: 13px;
                font-weight: 600;
            }
        """)

        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "Nhập mã hóa đơn hoặc tên khách hàng..."
        )

        self.search_input.setMinimumHeight(
            40
        )

        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #F8FAFC;
                border: 1px solid #CBD5E1;
                border-radius: 8px;
                padding: 8px 12px;
                color: #334155;
                font-size: 13px;
            }

            QLineEdit:focus {
                border: 1px solid #0F766E;
                background-color: white;
            }
        """)

        self.search_input.textChanged.connect(
            self.search_invoices
        )

        search_layout.addWidget(
            search_label
        )

        search_layout.addWidget(
            self.search_input,
            1
        )

        main_layout.addWidget(
            search_frame
        )

        # ==================================================
        # BẢNG HÓA ĐƠN
        # ==================================================

        table_frame = QFrame()

        table_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
        """)

        table_layout = QVBoxLayout(
            table_frame
        )

        table_layout.setContentsMargins(
            8,
            8,
            8,
            8
        )

        self.table = QTableWidget()

        self.table.setColumnCount(
            5
        )

        self.table.setHorizontalHeaderLabels([
            "Mã hóa đơn",
            "Khách hàng",
            "Tổng tiền",
            "Trạng thái",
            "Ngày tạo"
        ])

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.table.setSelectionMode(
            QTableWidget.SingleSelection
        )

        self.table.setAlternatingRowColors(
            True
        )

        self.table.setShowGrid(
            False
        )

        self.table.verticalHeader().setVisible(
            False
        )

        self.table.setStyleSheet("""
            QTableWidget {
                border: none;
                background-color: white;
                alternate-background-color: #F8FAFC;
                color: #334155;
                font-size: 13px;
            }

            QTableWidget::item {
                padding: 9px;
                border-bottom: 1px solid #F1F5F9;
            }

            QTableWidget::item:selected {
                background-color: #CCFBF1;
                color: #134E4A;
            }

            QHeaderView::section {
                background-color: #F0FDFA;
                color: #134E4A;
                border: none;
                border-bottom: 1px solid #99F6E4;
                padding: 12px 8px;
                font-size: 13px;
                font-weight: 700;
            }
        """)

        # ==================================================
        # CỘT
        # ==================================================

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.Stretch
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.ResizeToContents
        )

        header.setSectionResizeMode(
            4,
            QHeaderView.ResizeToContents
        )

        table_layout.addWidget(
            self.table
        )

        main_layout.addWidget(
            table_frame,
            1
        )

        # ==================================================
        # KHU VỰC NÚT
        # ==================================================

        button_layout = QHBoxLayout()

        button_layout.setSpacing(
            10
        )

        # ==================================================
        # XEM CHI TIẾT
        # ==================================================

        view_button = QPushButton(
            "👁  Xem chi tiết"
        )

        view_button.setMinimumHeight(
            44
        )

        view_button.setMinimumWidth(
            145
        )

        view_button.setStyleSheet("""
            QPushButton {
                background-color: #0F766E;
                color: white;
                border: none;
                border-radius: 9px;
                padding: 10px 18px;
                font-size: 13px;
                font-weight: 700;
            }

            QPushButton:hover {
                background-color: #115E59;
            }

            QPushButton:pressed {
                background-color: #134E4A;
            }
        """)

        view_button.clicked.connect(
            self.view_invoice
        )

        # ==================================================
        # XUẤT PDF
        # ==================================================

        pdf_button = QPushButton(
            "📄  Xuất PDF"
        )

        pdf_button.setMinimumHeight(
            44
        )

        pdf_button.setMinimumWidth(
            140
        )

        pdf_button.setStyleSheet("""
            QPushButton {
                background-color: #EFF6FF;
                color: #1D4ED8;
                border: 1px solid #BFDBFE;
                border-radius: 9px;
                padding: 10px 18px;
                font-size: 13px;
                font-weight: 700;
            }

            QPushButton:hover {
                background-color: #DBEAFE;
            }
        """)

        pdf_button.clicked.connect(
            self.export_pdf
        )

        # ==================================================
        # XÓA
        # ==================================================

        delete_button = QPushButton(
            "🗑  Xóa hóa đơn"
        )

        delete_button.setMinimumHeight(
            44
        )

        delete_button.setMinimumWidth(
            145
        )

        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #FEF2F2;
                color: #DC2626;
                border: 1px solid #FECACA;
                border-radius: 9px;
                padding: 10px 18px;
                font-size: 13px;
                font-weight: 700;
            }

            QPushButton:hover {
                background-color: #FEE2E2;
            }
        """)

        delete_button.clicked.connect(
            self.delete_invoice
        )

        # ==================================================
        # LÀM MỚI
        # ==================================================

        refresh_button = QPushButton(
            "🔄  Làm mới"
        )

        refresh_button.setMinimumHeight(
            44
        )

        refresh_button.setMinimumWidth(
            125
        )

        refresh_button.setStyleSheet("""
            QPushButton {
                background-color: #F1F5F9;
                color: #334155;
                border: 1px solid #CBD5E1;
                border-radius: 9px;
                padding: 10px 18px;
                font-size: 13px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #E2E8F0;
            }
        """)

        refresh_button.clicked.connect(
            self.refresh_data
        )

        button_layout.addWidget(
            view_button
        )

        button_layout.addWidget(
            pdf_button
        )

        button_layout.addWidget(
            delete_button
        )

        button_layout.addWidget(
            refresh_button
        )

        button_layout.addStretch()

        main_layout.addLayout(
            button_layout
        )

        # ==================================================
        # FOOTER
        # ==================================================

        footer = QLabel(
            "💚 Nhà thuốc Ý Như • Quản lý hóa đơn"
        )

        footer.setAlignment(
            Qt.AlignRight
        )

        footer.setStyleSheet("""
            QLabel {
                color: #94A3B8;
                font-size: 11px;
                padding-top: 2px;
            }
        """)

        main_layout.addWidget(
            footer
        )

        self.setLayout(
            main_layout
        )

    # ==================================================
    # TẢI DANH SÁCH HÓA ĐƠN
    # ==================================================

    def load_invoices(self):

        connection = get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute("""
                SELECT
                    id,
                    customer_name,
                    total,
                    payment_status,
                    created_at
                FROM invoices
                ORDER BY id DESC
            """)

            invoices = cursor.fetchall()

            self.display_invoices(
                invoices
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Lỗi",
                "Không thể tải danh sách hóa đơn!\n\n"
                f"{error}"
            )

        finally:

            connection.close()

    # ==================================================
    # HIỂN THỊ HÓA ĐƠN
    # ==================================================

    def display_invoices(
        self,
        invoices
    ):

        self.table.setRowCount(
            len(invoices)
        )

        for row, invoice in enumerate(
            invoices
        ):

            invoice_id = invoice[0]

            customer_name = (
                invoice[1]
                if invoice[1]
                else "Khách lẻ"
            )

            total = (
                invoice[2]
                if invoice[2] is not None
                else 0
            )

            payment_status = (
                invoice[3]
                if invoice[3]
                else "Đã thanh toán"
            )

            created_at = (
                invoice[4]
                if invoice[4]
                else ""
            )

            # ==================================================
            # MÃ HÓA ĐƠN
            # ==================================================

            item = QTableWidgetItem(
                f"HD-{invoice_id:04d}"
            )

            item.setTextAlignment(
                Qt.AlignCenter
            )

            self.table.setItem(
                row,
                0,
                item
            )

            # ==================================================
            # KHÁCH HÀNG
            # ==================================================

            customer_item = QTableWidgetItem(
                str(customer_name)
            )

            self.table.setItem(
                row,
                1,
                customer_item
            )

            # ==================================================
            # TỔNG TIỀN
            # ==================================================

            total_item = QTableWidgetItem(
                f"{float(total):,.0f} đ"
            )

            total_item.setTextAlignment(
                Qt.AlignRight |
                Qt.AlignVCenter
            )

            self.table.setItem(
                row,
                2,
                total_item
            )

            # ==================================================
            # TRẠNG THÁI
            # ==================================================

            status_item = QTableWidgetItem(
                str(payment_status)
            )

            status_item.setTextAlignment(
                Qt.AlignCenter
            )

            self.table.setItem(
                row,
                3,
                status_item
            )

            # ==================================================
            # NGÀY TẠO
            # ==================================================

            date_item = QTableWidgetItem(
                str(created_at)
            )

            date_item.setTextAlignment(
                Qt.AlignCenter
            )

            self.table.setItem(
                row,
                4,
                date_item
            )

        self.invoice_count.setText(
            f"{len(invoices)} hóa đơn"
        )

    # ==================================================
    # TÌM KIẾM
    # ==================================================

    def search_invoices(
        self,
        keyword
    ):

        keyword = keyword.strip()

        if not keyword:

            self.load_invoices()

            return

        connection = get_connection()

        cursor = connection.cursor()

        try:

            # Nếu nhập HD-0001 thì lấy phần số

            search_keyword = keyword

            if keyword.upper().startswith(
                "HD-"
            ):

                search_keyword = (
                    keyword[3:]
                )

            cursor.execute("""
                SELECT
                    id,
                    customer_name,
                    total,
                    payment_status,
                    created_at
                FROM invoices
                WHERE
                    CAST(id AS TEXT) LIKE ?
                    OR customer_name LIKE ?
                ORDER BY id DESC
            """, (
                f"%{search_keyword}%",
                f"%{keyword}%"
            ))

            invoices = cursor.fetchall()

            self.display_invoices(
                invoices
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Lỗi",
                "Không thể tìm kiếm hóa đơn!\n\n"
                f"{error}"
            )

        finally:

            connection.close()

    # ==================================================
    # LẤY ID HÓA ĐƠN ĐANG CHỌN
    # ==================================================

    def get_selected_invoice_id(self):

        selected_row = (
            self.table.currentRow()
        )

        if selected_row < 0:

            QMessageBox.warning(
                self,
                "Thông báo",
                "Vui lòng chọn một hóa đơn!"
            )

            return None

        item = self.table.item(
            selected_row,
            0
        )

        if item is None:

            return None

        invoice_text = item.text()

        try:

            # HD-0001 -> 1

            if invoice_text.upper().startswith(
                "HD-"
            ):

                invoice_id = int(
                    invoice_text[3:]
                )

            else:

                invoice_id = int(
                    invoice_text
                )

            return invoice_id

        except ValueError:

            QMessageBox.warning(
                self,
                "Lỗi",
                "Không xác định được mã hóa đơn!"
            )

            return None

    # ==================================================
    # XEM CHI TIẾT
    # ==================================================

    def view_invoice(self):

        invoice_id = (
            self.get_selected_invoice_id()
        )

        if invoice_id is None:
            return

        connection = get_connection()

        cursor = connection.cursor()

        try:

            # ==================================================
            # THÔNG TIN HÓA ĐƠN
            # ==================================================

            cursor.execute("""
                SELECT
                    customer_name,
                    total,
                    payment_status,
                    created_at
                FROM invoices
                WHERE id = ?
            """, (
                invoice_id,
            ))

            invoice = cursor.fetchone()

            if invoice is None:

                QMessageBox.warning(
                    self,
                    "Thông báo",
                    "Không tìm thấy hóa đơn!"
                )

                return

            customer_name = (
                invoice[0]
                if invoice[0]
                else "Khách lẻ"
            )

            total = (
                invoice[1]
                if invoice[1] is not None
                else 0
            )

            payment_status = (
                invoice[2]
                if invoice[2]
                else "Đã thanh toán"
            )

            created_at = (
                invoice[3]
                if invoice[3]
                else ""
            )

            # ==================================================
            # CHI TIẾT THUỐC
            # ==================================================

            cursor.execute("""
                SELECT
                    medicines.name,
                    invoice_details.quantity,
                    invoice_details.price
                FROM invoice_details
                LEFT JOIN medicines
                    ON medicines.id =
                       invoice_details.medicine_id
                WHERE invoice_details.invoice_id = ?
            """, (
                invoice_id,
            ))

            details = cursor.fetchall()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Lỗi",
                "Không thể lấy chi tiết hóa đơn!\n\n"
                f"{error}"
            )

            return

        finally:

            connection.close()

        # ==================================================
        # DIALOG CHI TIẾT
        # ==================================================

        dialog = QDialog(
            self
        )

        dialog.setWindowTitle(
            f"Chi tiết hóa đơn HD-{invoice_id:04d}"
        )

        dialog.setMinimumSize(
            650,
            500
        )

        dialog.setStyleSheet("""
            QDialog {
                background-color: #F5F7FA;
            }

            QLabel {
                color: #334155;
            }

            QTableWidget {
                background-color: white;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
            }

            QHeaderView::section {
                background-color: #F0FDFA;
                color: #134E4A;
                padding: 10px;
                font-weight: 700;
                border: none;
            }

            QPushButton {
                background-color: #0F766E;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 18px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #115E59;
            }
        """)

        dialog_layout = QVBoxLayout()

        dialog_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        # ==================================================
        # TIÊU ĐỀ
        # ==================================================

        dialog_title = QLabel(
            f"🧾 HÓA ĐƠN HD-{invoice_id:04d}"
        )

        dialog_title.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: 700;
                color: #134E4A;
            }
        """)

        dialog_layout.addWidget(
            dialog_title
        )

        # ==================================================
        # THÔNG TIN
        # ==================================================

        info_frame = QFrame()

        info_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E2E8F0;
                border-radius: 10px;
            }
        """)

        info_layout = QVBoxLayout(
            info_frame
        )

        info_layout.addWidget(
            QLabel(
                f"👤 Khách hàng: {customer_name}"
            )
        )

        info_layout.addWidget(
            QLabel(
                f"📅 Ngày tạo: {created_at}"
            )
        )

        info_layout.addWidget(
            QLabel(
                f"💳 Trạng thái: {payment_status}"
            )
        )

        dialog_layout.addWidget(
            info_frame
        )

        # ==================================================
        # BẢNG CHI TIẾT
        # ==================================================

        detail_table = QTableWidget()

        detail_table.setColumnCount(
            4
        )

        detail_table.setHorizontalHeaderLabels([
            "Tên thuốc",
            "Số lượng",
            "Đơn giá",
            "Thành tiền"
        ])

        detail_table.setRowCount(
            len(details)
        )

        detail_table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        detail_table.setSelectionMode(
            QTableWidget.NoSelection
        )

        detail_table.verticalHeader().setVisible(
            False
        )

        detail_table.setShowGrid(
            False
        )

        for row, detail in enumerate(
            details
        ):

            medicine_name = (
                detail[0]
                if detail[0]
                else "Thuốc đã xóa"
            )

            quantity = (
                detail[1]
                if detail[1] is not None
                else 0
            )

            price = (
                detail[2]
                if detail[2] is not None
                else 0
            )

            subtotal = (
                quantity * price
            )

            detail_table.setItem(
                row,
                0,
                QTableWidgetItem(
                    str(medicine_name)
                )
            )

            quantity_item = QTableWidgetItem(
                str(quantity)
            )

            quantity_item.setTextAlignment(
                Qt.AlignCenter
            )

            detail_table.setItem(
                row,
                1,
                quantity_item
            )

            price_item = QTableWidgetItem(
                f"{float(price):,.0f} đ"
            )

            price_item.setTextAlignment(
                Qt.AlignRight |
                Qt.AlignVCenter
            )

            detail_table.setItem(
                row,
                2,
                price_item
            )

            subtotal_item = QTableWidgetItem(
                f"{float(subtotal):,.0f} đ"
            )

            subtotal_item.setTextAlignment(
                Qt.AlignRight |
                Qt.AlignVCenter
            )

            detail_table.setItem(
                row,
                3,
                subtotal_item
            )

        detail_header = (
            detail_table.horizontalHeader()
        )

        detail_header.setSectionResizeMode(
            0,
            QHeaderView.Stretch
        )

        detail_header.setSectionResizeMode(
            1,
            QHeaderView.ResizeToContents
        )

        detail_header.setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents
        )

        detail_header.setSectionResizeMode(
            3,
            QHeaderView.ResizeToContents
        )

        dialog_layout.addWidget(
            detail_table,
            1
        )

        # ==================================================
        # TỔNG TIỀN
        # ==================================================

        total_label = QLabel(
            f"TỔNG TIỀN: {float(total):,.0f} đ"
        )

        total_label.setAlignment(
            Qt.AlignRight
        )

        total_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 700;
                color: #0F766E;
                padding: 10px;
            }
        """)

        dialog_layout.addWidget(
            total_label
        )

        # ==================================================
        # NÚT ĐÓNG
        # ==================================================

        buttons = QDialogButtonBox(
            QDialogButtonBox.Close
        )

        buttons.rejected.connect(
            dialog.reject
        )

        buttons.accepted.connect(
            dialog.accept
        )

        dialog_layout.addWidget(
            buttons
        )

        dialog.setLayout(
            dialog_layout
        )

        dialog.exec()

    # ==================================================
    # XUẤT PDF
    # ==================================================

    def export_pdf(self):

        invoice_id = (
            self.get_selected_invoice_id()
        )

        if invoice_id is None:
            return

        connection = get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute("""
                SELECT
                    customer_name,
                    total,
                    payment_status,
                    created_at
                FROM invoices
                WHERE id = ?
            """, (
                invoice_id,
            ))

            invoice = cursor.fetchone()

            if invoice is None:

                QMessageBox.warning(
                    self,
                    "Thông báo",
                    "Không tìm thấy hóa đơn!"
                )

                return

            customer_name = (
                invoice[0]
                if invoice[0]
                else "Khách lẻ"
            )

            total = (
                invoice[1]
                if invoice[1] is not None
                else 0
            )

            payment_status = (
                invoice[2]
                if invoice[2]
                else "Đã thanh toán"
            )

            created_at = (
                invoice[3]
                if invoice[3]
                else ""
            )

            cursor.execute("""
                SELECT
                    medicines.name,
                    invoice_details.quantity,
                    invoice_details.price
                FROM invoice_details
                LEFT JOIN medicines
                    ON medicines.id =
                       invoice_details.medicine_id
                WHERE invoice_details.invoice_id = ?
            """, (
                invoice_id,
            ))

            details = cursor.fetchall()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Lỗi",
                "Không thể lấy dữ liệu hóa đơn!\n\n"
                f"{error}"
            )

            return

        finally:

            connection.close()

        # ==================================================
        # CHỌN FILE
        # ==================================================

        from PySide6.QtWidgets import QFileDialog

        default_name = (
            f"HoaDon_{invoice_id}.pdf"
        )

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Lưu hóa đơn PDF",
            default_name,
            "PDF Files (*.pdf)"
        )

        if not file_path:
            return

        # ==================================================
        # TẠO PDF
        # ==================================================

        try:

            pdf = canvas.Canvas(
                file_path,
                pagesize=A4
            )

            width, height = A4

            # ==================================================
            # HEADER
            # ==================================================

            pdf.setFont(
                self.font_bold,
                20
            )

            pdf.drawCentredString(
                width / 2,
                height - 55,
                "NHA THUOC Y NHU"
            )

            pdf.setFont(
                self.font_normal,
                11
            )

            pdf.drawCentredString(
                width / 2,
                height - 75,
                "HOA DON BAN THUOC"
            )

            # ==================================================
            # THÔNG TIN HÓA ĐƠN
            # ==================================================

            y = height - 115

            pdf.setFont(
                self.font_normal,
                10
            )

            pdf.drawString(
                50,
                y,
                f"Ma hoa don: HD-{invoice_id:04d}"
            )

            y -= 20

            pdf.drawString(
                50,
                y,
                f"Khach hang: {customer_name}"
            )

            y -= 20

            pdf.drawString(
                50,
                y,
                f"Ngay tao: {created_at}"
            )

            y -= 20

            pdf.drawString(
                50,
                y,
                f"Trang thai: {payment_status}"
            )

            y -= 35

            # ==================================================
            # ĐƯỜNG KẺ
            # ==================================================

            pdf.line(
                50,
                y,
                width - 50,
                y
            )

            y -= 20

            # ==================================================
            # TIÊU ĐỀ BẢNG
            # ==================================================

            pdf.setFont(
                self.font_bold,
                10
            )

            pdf.drawString(
                50,
                y,
                "Thuoc"
            )

            pdf.drawString(
                310,
                y,
                "SL"
            )

            pdf.drawString(
                360,
                y,
                "Don gia"
            )

            pdf.drawString(
                465,
                y,
                "Thanh tien"
            )

            y -= 20

            pdf.setFont(
                self.font_normal,
                10
            )

            # ==================================================
            # DANH SÁCH THUỐC
            # ==================================================

            for detail in details:

                medicine_name = (
                    detail[0]
                    if detail[0]
                    else "Thuoc da xoa"
                )

                quantity = (
                    detail[1]
                    if detail[1] is not None
                    else 0
                )

                price = (
                    detail[2]
                    if detail[2] is not None
                    else 0
                )

                subtotal = (
                    quantity * price
                )

                if len(
                    medicine_name
                ) > 38:

                    medicine_name = (
                        medicine_name[:35]
                        + "..."
                    )

                pdf.drawString(
                    50,
                    y,
                    str(medicine_name)
                )

                pdf.drawString(
                    310,
                    y,
                    str(quantity)
                )

                pdf.drawRightString(
                    440,
                    y,
                    f"{float(price):,.0f} d"
                )

                pdf.drawRightString(
                    545,
                    y,
                    f"{float(subtotal):,.0f} d"
                )

                y -= 20

                # ==================================================
                # SANG TRANG
                # ==================================================

                if y < 90:

                    pdf.showPage()

                    pdf.setFont(
                        self.font_normal,
                        10
                    )

                    y = height - 50

            # ==================================================
            # TỔNG TIỀN
            # ==================================================

            y -= 15

            pdf.line(
                350,
                y + 15,
                545,
                y + 15
            )

            pdf.setFont(
                self.font_bold,
                13
            )

            pdf.drawString(
                350,
                y - 5,
                "TONG TIEN:"
            )

            pdf.drawRightString(
                545,
                y - 5,
                f"{float(total):,.0f} d"
            )

            # ==================================================
            # LỜI CẢM ƠN
            # ==================================================

            y -= 55

            pdf.setFont(
                self.font_normal,
                11
            )

            pdf.drawCentredString(
                width / 2,
                y,
                "Cam on quy khach!"
            )

            y -= 18

            pdf.drawCentredString(
                width / 2,
                y,
                "Hen gap lai quy khach."
            )

            # ==================================================
            # LƯU PDF
            # ==================================================

            pdf.save()

            QMessageBox.information(
                self,
                "Xuất PDF thành công",
                "Đã xuất hóa đơn PDF thành công!\n\n"
                f"File:\n{file_path}"
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Lỗi xuất PDF",
                "Không thể xuất hóa đơn PDF!\n\n"
                f"{error}"
            )

    # ==================================================
    # XÓA HÓA ĐƠN
    # ==================================================

    def delete_invoice(self):

        invoice_id = (
            self.get_selected_invoice_id()
        )

        if invoice_id is None:
            return

        # ==================================================
        # XÁC NHẬN
        # ==================================================

        answer = QMessageBox.question(
            self,
            "Xác nhận xóa",
            f"Bạn có chắc muốn xóa hóa đơn "
            f"HD-{invoice_id:04d} không?\n\n"
            "Chi tiết hóa đơn cũng sẽ bị xóa.",
            QMessageBox.Yes |
            QMessageBox.No,
            QMessageBox.No
        )

        if answer != QMessageBox.Yes:
            return

        connection = get_connection()

        cursor = connection.cursor()

        try:

            # ==================================================
            # HOÀN LẠI TỒN KHO TRƯỚC KHI XÓA HÓA ĐƠN
            # ==================================================
            # Hóa đơn đã bán làm giảm tồn kho, vì vậy khi xóa
            # hóa đơn phải trả lại số lượng để dữ liệu không lệch.
            cursor.execute("""
                SELECT medicine_id, quantity
                FROM invoice_details
                WHERE invoice_id = ?
            """, (invoice_id,))

            details_to_restore = cursor.fetchall()

            for medicine_id, quantity in details_to_restore:
                if medicine_id is not None and quantity:
                    cursor.execute("""
                        UPDATE medicines
                        SET quantity = quantity + ?
                        WHERE id = ?
                    """, (quantity, medicine_id))

            # ==================================================
            # XÓA CHI TIẾT
            # ==================================================

            cursor.execute("""
                DELETE FROM invoice_details
                WHERE invoice_id = ?
            """, (
                invoice_id,
            ))

            # ==================================================
            # XÓA HÓA ĐƠN
            # ==================================================

            cursor.execute("""
                DELETE FROM invoices
                WHERE id = ?
            """, (
                invoice_id,
            ))

            connection.commit()

            QMessageBox.information(
                self,
                "Thành công",
                f"Đã xóa hóa đơn HD-{invoice_id:04d}!"
            )

            # ==================================================
            # TẢI LẠI
            # ==================================================

            self.load_invoices()

        except Exception as error:

            connection.rollback()

            QMessageBox.critical(
                self,
                "Lỗi",
                "Không thể xóa hóa đơn!\n\n"
                f"{error}"
            )

        finally:

            connection.close()

    # ==================================================
    # LÀM MỚI
    # ==================================================

    def refresh_data(self):

        self.search_input.clear()

        self.load_invoices()


# ==================================================
# CHẠY THỬ FILE
# ==================================================

if __name__ == "__main__":

    import sys

    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    window = InvoiceWindow()

    window.show()

    sys.exit(
        app.exec()
    )