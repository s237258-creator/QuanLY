import sqlite3
from pathlib import Path

# Đường dẫn chính xác đến pharmacy.db
DATABASE = Path(__file__).resolve().parent / "pharmacy.db"

print("Database:")
print(DATABASE)

if not DATABASE.exists():
    print("❌ Không tìm thấy pharmacy.db")
    exit()

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

# Lấy danh sách bảng
cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name
""")

tables = cursor.fetchall()

print("\n==============================")
print("      DANH SÁCH BẢNG")
print("==============================")

for table in tables:
    table_name = table[0]
    print(f"\n📌 BẢNG: {table_name}")

    cursor.execute(f"SELECT * FROM [{table_name}]")
    rows = cursor.fetchall()

    if not rows:
        print("   Chưa có dữ liệu.")
    else:
        for row in rows:
            print("  ", row)

connection.close()

print("\n==============================")
print("✅ KIỂM TRA DATABASE XONG")
print("==============================")