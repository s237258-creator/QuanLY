import sqlite3
from pathlib import Path


# ==================================================
# ĐƯỜNG DẪN DATABASE
# ==================================================

# Lấy thư mục gốc của project
BASE_DIR = Path(__file__).resolve().parent.parent

# File database
DB_PATH = BASE_DIR / "pharmacy.db"


# ==================================================
# KẾT NỐI DATABASE
# ==================================================

def get_connection():
    """
    Tạo kết nối đến SQLite database.
    """
    connection = sqlite3.connect(DB_PATH, timeout=10)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


# ==================================================
# TẠO DATABASE
# ==================================================

def create_database():
    """
    Tạo các bảng cần thiết cho hệ thống quản lý nhà thuốc.
    """

    connection = get_connection()
    cursor = connection.cursor()

    # ==================================================
    # BẢNG TÀI KHOẢN
    # ==================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT,
            role TEXT DEFAULT 'admin'
        )
    """)

    # ==================================================
    # BẢNG THUỐC
    # ==================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            unit TEXT,
            price REAL DEFAULT 0,
            quantity INTEGER DEFAULT 0,
            expiry_date TEXT
        )
    """)
    # ==================================================
    # BẢNG KHÁCH HÀNG
    # ==================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            address TEXT,
            note TEXT
        )
    """)

    # ==================================================
    # BẢNG HÓA ĐƠN
    # ==================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            total REAL DEFAULT 0,
            payment_status TEXT DEFAULT 'Chưa thanh toán',
            created_at TEXT
        )
    """)

    # ==================================================
    # BẢNG LỊCH SỬ NHẬP THUỐC
    # ==================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_imports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_id INTEGER,
            quantity INTEGER NOT NULL,
            imported_at TEXT,
            FOREIGN KEY (medicine_id) REFERENCES medicines(id)
        )
    """)

    # ==================================================
    # BẢNG CHI TIẾT HÓA ĐƠN
    # ==================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoice_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER,
            medicine_id INTEGER,
            quantity INTEGER,
            price REAL,
            FOREIGN KEY (invoice_id) REFERENCES invoices(id),
            FOREIGN KEY (medicine_id) REFERENCES medicines(id)
        )
    """)

    # ==================================================
    # TẠO TÀI KHOẢN ADMIN MẶC ĐỊNH
    # ==================================================

    cursor.execute("""
        SELECT id
        FROM users
        WHERE username = ?
    """, ("admin",))

    admin = cursor.fetchone()

    if admin is None:

        cursor.execute("""
            INSERT INTO users
            (
                username,
                password,
                full_name,
                role
            )
            VALUES (?, ?, ?, ?)
        """, (
            "admin",
            "123456",
            "Quản trị viên",
            "admin"
        ))

    # ==================================================
    # LƯU THAY ĐỔI
    # ==================================================

    connection.commit()

    # Đóng kết nối
    connection.close()


# ==================================================
# CHẠY FILE TRỰC TIẾP
# ==================================================

if __name__ == "__main__":

    create_database()

    print("Database đã được tạo thành công!")