# ============================================================
# GIAO DIỆN CHUNG CHO PHẦN MỀM QUẢN LÝ NHÀ THUỐC
# ============================================================

def apply_theme(app):

    app.setStyleSheet("""

    /* ========================================================
       TOÀN BỘ ỨNG DỤNG
       ======================================================== */

    QWidget {
        font-family: "Segoe UI";
        font-size: 14px;
        color: #1F2937;
    }

    QMainWindow,
    QWidget {
        background-color: #F5F7FA;
    }


    /* ========================================================
       LABEL
       ======================================================== */

    QLabel {
        color: #1F2937;
    }


    /* ========================================================
       Ô NHẬP
       ======================================================== */

    QLineEdit {
        background-color: white;
        border: 1px solid #D1D5DB;
        border-radius: 8px;
        padding: 10px 12px;
        min-height: 20px;
    }

    QLineEdit:focus {
        border: 2px solid #14B8A6;
    }


    /* ========================================================
       COMBO BOX
       ======================================================== */

    QComboBox {
        background-color: white;
        border: 1px solid #D1D5DB;
        border-radius: 8px;
        padding: 9px 12px;
        min-height: 20px;
    }

    QComboBox:hover {
        border-color: #14B8A6;
    }

    QComboBox:focus {
        border: 2px solid #14B8A6;
    }


    /* ========================================================
       BUTTON
       ======================================================== */

    QPushButton {
        background-color: white;
        color: #374151;
        border: 1px solid #D1D5DB;
        border-radius: 8px;
        padding: 10px 18px;
        min-height: 20px;
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


    /* ========================================================
       BUTTON PRIMARY - MÀU XANH
       ======================================================== */

    QPushButton#primaryButton {
        background-color: #0F766E;
        color: white;
        border: none;
    }

    QPushButton#primaryButton:hover {
        background-color: #115E59;
    }


    /* ========================================================
       BUTTON SUCCESS
       ======================================================== */

    QPushButton#successButton {
        background-color: #10B981;
        color: white;
        border: none;
    }

    QPushButton#successButton:hover {
        background-color: #059669;
    }


    /* ========================================================
       BUTTON DANGER
       ======================================================== */

    QPushButton#dangerButton {
        background-color: #EF4444;
        color: white;
        border: none;
    }

    QPushButton#dangerButton:hover {
        background-color: #DC2626;
    }


    /* ========================================================
       TABLE
       ======================================================== */

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


    /* ========================================================
       HEADER CỦA TABLE
       ======================================================== */

    QHeaderView::section {
        background-color: #F0FDFA;
        color: #0F766E;
        font-weight: bold;
        border: none;
        border-bottom: 1px solid #D1D5DB;
        padding: 10px;
    }


    /* ========================================================
       GROUP BOX
       ======================================================== */

    QGroupBox {
        background-color: white;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        margin-top: 12px;
        padding: 15px;
        font-weight: bold;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 15px;
        padding: 0 5px;
        color: #0F766E;
    }


    /* ========================================================
       TEXT EDIT
       ======================================================== */

    QTextEdit {
        background-color: white;
        border: 1px solid #D1D5DB;
        border-radius: 8px;
        padding: 8px;
    }

    QTextEdit:focus {
        border: 2px solid #14B8A6;
    }


    /* ========================================================
       SPIN BOX
       ======================================================== */

    QSpinBox,
    QDoubleSpinBox {
        background-color: white;
        border: 1px solid #D1D5DB;
        border-radius: 8px;
        padding: 9px;
    }


    /* ========================================================
       THANH CUỘN
       ======================================================== */

    QScrollBar:vertical {
        background: #F3F4F6;
        width: 10px;
        margin: 0;
    }

    QScrollBar::handle:vertical {
        background: #CBD5E1;
        border-radius: 5px;
        min-height: 30px;
    }

    QScrollBar::handle:vertical:hover {
        background: #94A3B8;
    }

    QScrollBar:horizontal {
        background: #F3F4F6;
        height: 10px;
    }

    QScrollBar::handle:horizontal {
        background: #CBD5E1;
        border-radius: 5px;
    }

    """)