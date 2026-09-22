from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QSpinBox,
    QDoubleSpinBox,
    QInputDialog,
    QFrame,
    QGridLayout
)

from PySide6.QtCore import Qt

from database.database import get_connection

from datetime import datetime, date


class MedicineWindow(QWidget):

    def __init__(self):
        super().__init__()

        # ==================================================
        # CẤU HÌNH CỬA SỔ
        # ==================================================

        self.setWindowTitle(
            "Nhà thuốc Ý Như - Quản lý thuốc"
        )

        self.setMinimumSize(
            1150,
            700
        )

        # ==================================================
        # STYLE
        # ==================================================

        self.setStyleSheet("""

            QWidget {
                font-family: "Segoe UI";
            }

            /* ==============================================
               TIÊU ĐỀ
               ============================================== */

            QLabel#pageTitle {
                color: #0F766E;
                font-size: 27px;
                font-weight: bold;
            }

            QLabel#pageSubtitle {
                color: #6B7280;
                font-size: 13px;
            }

            /* ==============================================
               KHUNG
               ============================================== */

            QFrame#panel {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 14px;
            }

            QLabel#panelTitle {
                color: #111827;
                font-size: 17px;
                font-weight: bold;
            }

            QLabel#fieldLabel {
                color: #374151;
                font-size: 12px;
                font-weight: bold;
            }

            /* ==============================================
               Ô NHẬP
               ============================================== */

            QLineEdit,
            QSpinBox,
            QDoubleSpinBox {
                background-color: #F9FAFB;
                color: #1F2937;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 9px 10px;
                min-height: 22px;
            }

            QLineEdit:focus,
            QSpinBox:focus,
            QDoubleSpinBox:focus {
                background-color: white;
                border: 2px solid #14B8A6;
            }

            /* ==============================================
               BUTTON
               ============================================== */

            QPushButton {
                background-color: white;
                color: #374151;
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding: 9px 15px;
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

            QPushButton#successButton {
                background-color: #10B981;
                color: white;
                border: none;
            }

            QPushButton#successButton:hover {
                background-color: #059669;
            }

            QPushButton#dangerButton {
                background-color: #EF4444;
                color: white;
                border: none;
            }

            QPushButton#dangerButton:hover {
                background-color: #DC2626;
            }

            /* ==============================================
               BẢNG
               ============================================== */

            QTableWidget {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 10px;
                gridline-color: #E5E7EB;
                selection-background-color: #CCFBF1;
                selection-color: #134E4A;
                alternate-background-color: #F9FAFB;
            }

            QTableWidget::item {
                padding: 8px;
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
                padding: 11px;
            }

        """)

        # ==================================================
        # TIÊU ĐỀ TRANG
        # ==================================================

        title = QLabel(
            "💊  Quản lý thuốc"
        )

        title.setObjectName(
            "pageTitle"
        )

        subtitle = QLabel(
            "Quản lý thông tin, số lượng và hạn sử dụng thuốc tại Nhà thuốc Ý Như"
        )

        subtitle.setObjectName(
            "pageSubtitle"
        )

        # ==================================================
        # KHUNG TÌM KIẾM
        # ==================================================

        search_panel = QFrame()

        search_panel.setObjectName(
            "panel"
        )

        search_layout = QHBoxLayout()

        search_layout.setContentsMargins(
            18,
            15,
            18,
            15
        )

        search_label = QLabel(
            "🔎  Tìm kiếm:"
        )

        search_label.setStyleSheet("""
            font-weight: bold;
            color: #374151;
        """)

        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "Nhập tên thuốc cần tìm..."
        )

        self.search_input.setMinimumHeight(
            40
        )

        search_button = QPushButton(
            "🔎 Tìm kiếm"
        )

        search_button.setObjectName(
            "primaryButton"
        )

        search_button.setMinimumHeight(
            40
        )

        search_button.clicked.connect(
            self.search_medicine
        )

        show_all_button = QPushButton(
            "📋 Hiển thị tất cả"
        )

        show_all_button.setMinimumHeight(
            40
        )

        show_all_button.clicked.connect(
            self.load_medicines
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
            show_all_button
        )

        search_panel.setLayout(
            search_layout
        )

        # ==================================================
        # KHUNG THÔNG TIN THUỐC
        # ==================================================

        form_panel = QFrame()

        form_panel.setObjectName(
            "panel"
        )

        form_layout = QVBoxLayout()

        form_layout.setContentsMargins(
            18,
            15,
            18,
            18
        )

        form_title = QLabel(
            "📋  Thông tin thuốc"
        )

        form_title.setObjectName(
            "panelTitle"
        )

        form_layout.addWidget(
            form_title
        )

        # ==================================================
        # GRID FORM
        # ==================================================

        grid = QGridLayout()

        grid.setHorizontalSpacing(
            12
        )

        grid.setVerticalSpacing(
            7
        )

        # --------------------------------------------------
        # TÊN THUỐC
        # --------------------------------------------------

        name_label = QLabel(
            "Tên thuốc"
        )

        name_label.setObjectName(
            "fieldLabel"
        )

        self.name_input = QLineEdit()

        self.name_input.setPlaceholderText(
            "Ví dụ: Paracetamol 500mg"
        )

        # --------------------------------------------------
        # LOẠI THUỐC
        # --------------------------------------------------

        category_label = QLabel(
            "Loại thuốc"
        )

        category_label.setObjectName(
            "fieldLabel"
        )

        self.category_input = QLineEdit()

        self.category_input.setPlaceholderText(
            "Ví dụ: Thuốc giảm đau"
        )

        # --------------------------------------------------
        # ĐƠN VỊ
        # --------------------------------------------------

        unit_label = QLabel(
            "Đơn vị"
        )

        unit_label.setObjectName(
            "fieldLabel"
        )

        self.unit_input = QLineEdit()

        self.unit_input.setPlaceholderText(
            "Ví dụ: Hộp, viên..."
        )

        # --------------------------------------------------
        # GIÁ
        # --------------------------------------------------

        price_label = QLabel(
            "Giá bán"
        )

        price_label.setObjectName(
            "fieldLabel"
        )

        self.price_input = QDoubleSpinBox()

        self.price_input.setRange(
            0,
            100000000
        )

        self.price_input.setSuffix(
            " đ"
        )

        self.price_input.setDecimals(
            0
        )

        # --------------------------------------------------
        # SỐ LƯỢNG
        # --------------------------------------------------

        quantity_label = QLabel(
            "Số lượng"
        )

        quantity_label.setObjectName(
            "fieldLabel"
        )

        self.quantity_input = QSpinBox()

        self.quantity_input.setRange(
            0,
            1000000
        )

        # --------------------------------------------------
        # HẠN SỬ DỤNG
        # --------------------------------------------------

        expiry_label = QLabel(
            "Hạn sử dụng"
        )

        expiry_label.setObjectName(
            "fieldLabel"
        )

        self.expiry_input = QLineEdit()

        self.expiry_input.setPlaceholderText(
            "YYYY-MM-DD"
        )

        # ==================================================
        # ĐƯA FORM VÀO GRID
        # ==================================================

        grid.addWidget(
            name_label,
            0,
            0
        )

        grid.addWidget(
            category_label,
            0,
            1
        )

        grid.addWidget(
            unit_label,
            0,
            2
        )

        grid.addWidget(
            price_label,
            0,
            3
        )

        grid.addWidget(
            self.name_input,
            1,
            0
        )

        grid.addWidget(
            self.category_input,
            1,
            1
        )

        grid.addWidget(
            self.unit_input,
            1,
            2
        )

        grid.addWidget(
            self.price_input,
            1,
            3
        )

        grid.addWidget(
            quantity_label,
            2,
            0
        )

        grid.addWidget(
            expiry_label,
            2,
            1
        )

        grid.addWidget(
            self.quantity_input,
            3,
            0
        )

        grid.addWidget(
            self.expiry_input,
            3,
            1
        )

        form_layout.addLayout(
            grid
        )

        # ==================================================
        # BUTTON CHỨC NĂNG
        # ==================================================

        button_layout = QHBoxLayout()

        button_layout.setSpacing(
            10
        )

        add_button = QPushButton(
            "➕  Thêm thuốc"
        )

        add_button.setObjectName(
            "successButton"
        )

        add_button.setMinimumHeight(
            42
        )

        add_button.clicked.connect(
            self.add_medicine
        )

        edit_button = QPushButton(
            "✏️  Sửa thuốc"
        )

        edit_button.setObjectName(
            "primaryButton"
        )

        edit_button.setMinimumHeight(
            42
        )

        edit_button.clicked.connect(
            self.edit_medicine
        )

        delete_button = QPushButton(
            "🗑️  Xóa thuốc"
        )

        delete_button.setObjectName(
            "dangerButton"
        )

        delete_button.setMinimumHeight(
            42
        )

        delete_button.clicked.connect(
            self.delete_medicine
        )

        import_button = QPushButton(
            "📦  Nhập thuốc"
        )

        import_button.setMinimumHeight(
            42
        )

        import_button.clicked.connect(
            self.import_medicine
        )

        clear_button = QPushButton(
            "↩️  Làm trống"
        )

        clear_button.setMinimumHeight(
            42
        )

        clear_button.clicked.connect(
            self.clear_inputs
        )

        button_layout.addWidget(
            add_button
        )

        button_layout.addWidget(
            edit_button
        )

        button_layout.addWidget(
            delete_button
        )

        button_layout.addWidget(
            import_button
        )

        button_layout.addWidget(
            clear_button
        )

        button_layout.addStretch()

        form_layout.addSpacing(
            8
        )

        form_layout.addLayout(
            button_layout
        )

        form_panel.setLayout(
            form_layout
        )

        # ==================================================
        # TIÊU ĐỀ DANH SÁCH
        # ==================================================

        table_title = QLabel(
            "📦  Danh sách thuốc"
        )

        table_title.setObjectName(
            "panelTitle"
        )

        # ==================================================
        # BẢNG THUỐC
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
            "Số lượng",
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

        self.table.setMinimumHeight(
            260
        )

        self.table.itemSelectionChanged.connect(
            self.load_selected_medicine
        )

        # ==================================================
        # LAYOUT CHÍNH
        # ==================================================

        layout = QVBoxLayout()

        layout.setContentsMargins(
            25,
            22,
            25,
            22
        )

        layout.setSpacing(
            10
        )

        layout.addWidget(
            title
        )

        layout.addWidget(
            subtitle
        )

        layout.addSpacing(
            5
        )

        layout.addWidget(
            search_panel
        )

        layout.addWidget(
            form_panel
        )

        layout.addWidget(
            table_title
        )

        layout.addWidget(
            self.table
        )

        self.setLayout(
            layout
        )

        # ==================================================
        # TẢI DỮ LIỆU
        # ==================================================

        self.load_medicines()
    # ==================================================
    # THÊM THUỐC
    # ==================================================

    def add_medicine(self):

        name = self.name_input.text().strip()

        category = self.category_input.text().strip()

        unit = self.unit_input.text().strip()

        price = self.price_input.value()

        quantity = self.quantity_input.value()

        expiry_date = self.expiry_input.text().strip()

        if not name:

            QMessageBox.warning(
                self,
                "Thông báo",
                "Vui lòng nhập tên thuốc!"
            )

            return

        connection = get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO medicines
                (
                    name,
                    category,
                    unit,
                    price,
                    quantity,
                    expiry_date
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    category,
                    unit,
                    price,
                    quantity,
                    expiry_date
                )
            )

            connection.commit()

            connection.close()

            QMessageBox.information(
                self,
                "Thành công",
                "Đã thêm thuốc thành công!"
            )

            self.clear_inputs()

            self.load_medicines()

        except Exception as error:

            connection.rollback()

            connection.close()

            QMessageBox.critical(
                self,
                "Lỗi",
                f"Không thể thêm thuốc!\n\n{error}"
            )

    # ==================================================
    # CHỌN THUỐC
    # ==================================================

    def load_selected_medicine(self):

        selected_row = self.table.currentRow()

        if selected_row < 0:
            return

        self.name_input.setText(
            self.table.item(
                selected_row,
                1
            ).text()
        )

        self.category_input.setText(
            self.table.item(
                selected_row,
                2
            ).text()
        )

        self.unit_input.setText(
            self.table.item(
                selected_row,
                3
            ).text()
        )

        price_text = self.table.item(
            selected_row,
            4
        ).text()

        try:

            price_text = (
                price_text
                .replace(",", "")
                .replace(" đ", "")
                .strip()
            )

            self.price_input.setValue(
                float(price_text)
            )

        except ValueError:

            self.price_input.setValue(
                0
            )

        quantity_text = self.table.item(
            selected_row,
            5
        ).text()

        try:

            self.quantity_input.setValue(
                int(quantity_text)
            )

        except ValueError:

            self.quantity_input.setValue(
                0
            )

        self.expiry_input.setText(
            self.table.item(
                selected_row,
                6
            ).text()
        )

    # ==================================================
    # SỬA THUỐC
    # ==================================================

    def edit_medicine(self):

        selected_row = self.table.currentRow()

        if selected_row < 0:

            QMessageBox.warning(
                self,
                "Thông báo",
                "Vui lòng chọn thuốc cần sửa!"
            )

            return

        medicine_id = self.table.item(
            selected_row,
            0
        ).text()

        name = self.name_input.text().strip()

        category = self.category_input.text().strip()

        unit = self.unit_input.text().strip()

        price = self.price_input.value()

        quantity = self.quantity_input.value()

        expiry_date = self.expiry_input.text().strip()

        if not name:

            QMessageBox.warning(
                self,
                "Thông báo",
                "Vui lòng nhập tên thuốc!"
            )

            return

        connection = get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                UPDATE medicines
                SET
                    name = ?,
                    category = ?,
                    unit = ?,
                    price = ?,
                    quantity = ?,
                    expiry_date = ?
                WHERE id = ?
                """,
                (
                    name,
                    category,
                    unit,
                    price,
                    quantity,
                    expiry_date,
                    medicine_id
                )
            )

            connection.commit()

            connection.close()

            QMessageBox.information(
                self,
                "Thành công",
                "Đã sửa thuốc thành công!"
            )

            self.load_medicines()

        except Exception as error:

            connection.rollback()

            connection.close()

            QMessageBox.critical(
                self,
                "Lỗi",
                f"Không thể sửa thuốc!\n\n{error}"
            )

    # ==================================================
    # NHẬP THUỐC
    # ==================================================

    def import_medicine(self):

        selected_row = self.table.currentRow()

        if selected_row < 0:

            QMessageBox.warning(
                self,
                "Thông báo",
                "Vui lòng chọn thuốc cần nhập!"
            )

            return

        medicine_id = int(
            self.table.item(
                selected_row,
                0
            ).text()
        )

        medicine_name = self.table.item(
            selected_row,
            1
        ).text()

        current_quantity = int(
            self.table.item(
                selected_row,
                5
            ).text()
        )

        quantity, ok = QInputDialog.getInt(
            self,
            "📦 Nhập thuốc",
            f"Thuốc: {medicine_name}\n\n"
            f"Tồn kho hiện tại: {current_quantity}\n\n"
            f"Nhập thêm số lượng:",
            1,
            1,
            1000000,
            1
        )

        if not ok:
            return

        new_quantity = current_quantity + quantity

        answer = QMessageBox.question(
            self,
            "Xác nhận nhập thuốc",
            f"Thuốc: {medicine_name}\n"
            f"Tồn kho hiện tại: {current_quantity}\n"
            f"Nhập thêm: {quantity}\n"
            f"Tồn kho sau khi nhập: {new_quantity}\n\n"
            f"Bạn có chắc muốn nhập thuốc không?",
            QMessageBox.Yes |
            QMessageBox.No
        )

        if answer != QMessageBox.Yes:
            return

        connection = get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                UPDATE medicines
                SET quantity = quantity + ?
                WHERE id = ?
                """,
                (
                    quantity,
                    medicine_id
                )
            )

            imported_at = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            cursor.execute(
                """
                INSERT INTO stock_imports
                (
                    medicine_id,
                    quantity,
                    imported_at
                )
                VALUES (?, ?, ?)
                """,
                (
                    medicine_id,
                    quantity,
                    imported_at
                )
            )

            connection.commit()

            connection.close()

            QMessageBox.information(
                self,
                "Nhập thuốc thành công",
                f"Đã nhập thêm {quantity} {medicine_name}!\n\n"
                f"Tồn kho hiện tại: {new_quantity}"
            )

            self.load_medicines()

        except Exception as error:

            connection.rollback()

            connection.close()

            QMessageBox.critical(
                self,
                "Lỗi nhập thuốc",
                f"Không thể nhập thuốc!\n\n{error}"
            )

    # ==================================================
    # XÓA THUỐC
    # ==================================================

    def delete_medicine(self):

        selected_row = self.table.currentRow()

        if selected_row < 0:

            QMessageBox.warning(
                self,
                "Thông báo",
                "Vui lòng chọn thuốc cần xóa!"
            )

            return

        medicine_id = self.table.item(
            selected_row,
            0
        ).text()

        medicine_name = self.table.item(
            selected_row,
            1
        ).text()

        answer = QMessageBox.question(
            self,
            "Xác nhận",
            f"Bạn có chắc muốn xóa thuốc "
            f"'{medicine_name}' không?",
            QMessageBox.Yes |
            QMessageBox.No
        )

        if answer != QMessageBox.Yes:
            return

        connection = get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                DELETE FROM medicines
                WHERE id = ?
                """,
                (
                    medicine_id,
                )
            )

            connection.commit()

            connection.close()

            QMessageBox.information(
                self,
                "Thành công",
                "Đã xóa thuốc thành công!"
            )

            self.clear_inputs()

            self.load_medicines()

        except Exception as error:

            connection.rollback()

            connection.close()

            QMessageBox.critical(
                self,
                "Lỗi",
                f"Không thể xóa thuốc!\n\n{error}"
            )

    # ==================================================
    # TÌM KIẾM
    # ==================================================

    def search_medicine(self):

        keyword = self.search_input.text().strip()

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
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
            ORDER BY id DESC
            """,
            (
                f"%{keyword}%",
            )
        )

        medicines = cursor.fetchall()

        connection.close()

        self.table.setRowCount(
            len(medicines)
        )

        for row, medicine in enumerate(
            medicines
        ):

            for column, value in enumerate(
                medicine
            ):

                if value is None:
                    value = ""

                if column == 4:

                    try:

                        value = f"{float(value):,.0f}"

                    except (
                        ValueError,
                        TypeError
                    ):

                        value = "0"

                item = QTableWidgetItem(
                    str(value)
                )

                self.table.setItem(
                    row,
                    column,
                    item
                )

        self.align_table()

    # ==================================================
    # XÓA FORM
    # ==================================================

    def clear_inputs(self):

        self.name_input.clear()

        self.category_input.clear()

        self.unit_input.clear()

        self.price_input.setValue(
            0
        )

        self.quantity_input.setValue(
            0
        )

        self.expiry_input.clear()

        self.table.clearSelection()

    # ==================================================
    # HIỂN THỊ DANH SÁCH
    # ==================================================

    def load_medicines(self):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                name,
                category,
                unit,
                price,
                quantity,
                expiry_date
            FROM medicines
            ORDER BY id DESC
            """
        )

        medicines = cursor.fetchall()

        connection.close()

        self.table.setRowCount(
            len(medicines)
        )

        for row, medicine in enumerate(
            medicines
        ):

            for column, value in enumerate(
                medicine
            ):

                if value is None:
                    value = ""

                if column == 4:

                    try:

                        value = f"{float(value):,.0f}"

                    except (
                        ValueError,
                        TypeError
                    ):

                        value = "0"

                item = QTableWidgetItem(
                    str(value)
                )

                self.table.setItem(
                    row,
                    column,
                    item
                )

        self.align_table()

    # ==================================================
    # CĂN CHỈNH BẢNG
    # ==================================================

    def align_table(self):

        for row in range(
            self.table.rowCount()
        ):

            for column in [
                0,
                4,
                5,
                6
            ]:

                item = self.table.item(
                    row,
                    column
                )

                if item:

                    item.setTextAlignment(
                        Qt.AlignCenter
                    )

        self.table.resizeColumnsToContents()

        # Đặt độ rộng hợp lý
        self.table.setColumnWidth(
            1,
            260
        )

        self.table.setColumnWidth(
            2,
            170
        )

    # ==================================================
    # KIỂM TRA CẢNH BÁO
    # ==================================================

    def check_warnings(self):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                name,
                quantity,
                expiry_date
            FROM medicines
            """
        )

        medicines = cursor.fetchall()

        connection.close()

        warnings = []

        today = date.today()

        for medicine in medicines:

            name = medicine[0]

            quantity = medicine[1]

            expiry_date = medicine[2]

            # ------------------------------------------------
            # TỒN KHO
            # ------------------------------------------------

            if quantity == 0:

                warnings.append(
                    f"🔴 {name}: ĐÃ HẾT HÀNG"
                )

            elif quantity <= 10:

                warnings.append(
                    f"🟡 {name}: Sắp hết hàng "
                    f"(còn {quantity})"
                )

            # ------------------------------------------------
            # HẠN SỬ DỤNG
            # ------------------------------------------------

            if expiry_date:

                try:

                    expiry = datetime.strptime(
                        expiry_date,
                        "%Y-%m-%d"
                    ).date()

                    days_left = (
                        expiry - today
                    ).days

                    if days_left < 0:

                        warnings.append(
                            f"🔴 {name}: ĐÃ HẾT HẠN"
                        )

                    elif days_left <= 30:

                        warnings.append(
                            f"🟠 {name}: Sắp hết hạn "
                            f"({days_left} ngày)"
                        )

                except ValueError:

                    pass

        # ==================================================
        # HIỂN THỊ CẢNH BÁO
        # ==================================================

        if warnings:

            QMessageBox.warning(
                self,
                "🔔 Cảnh báo thuốc",
                "\n".join(warnings)
            )