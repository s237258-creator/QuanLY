# App Quản Lý Nhà Thuốc Ý Như

Ứng dụng desktop quản lý nhà thuốc xây dựng bằng **Python + PySide6 + SQLite**.

## Chức năng

- Đăng nhập / đăng ký tài khoản
- Dashboard tổng quan
- Quản lý thuốc: thêm, sửa, xóa, tìm kiếm, cảnh báo tồn kho/hạn dùng
- Quản lý khách hàng
- Quản lý kho và cảnh báo thuốc
- Nhập thuốc và lịch sử nhập
- Bán thuốc, giỏ hàng, thanh toán, tự động trừ tồn kho
- Quản lý hóa đơn, xem chi tiết, xuất PDF, xóa hóa đơn và hoàn lại tồn kho
- Thống kê doanh thu, bán chạy và tồn kho
- Cài đặt giao diện và ngôn ngữ

## Cài đặt trên Windows

Mở Terminal tại thư mục `App_QuanLy`:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Chạy ứng dụng:

```powershell
.\.venv\Scripts\python.exe main.py
```

Nếu PowerShell chặn kích hoạt `.venv`, không cần activate; dùng trực tiếp lệnh trên.

## Tài khoản mặc định

- Tài khoản: `admin`
- Mật khẩu: `123456`

Nên đổi mật khẩu trước khi sử dụng thực tế.

## Database

Database SQLite nằm tại `pharmacy.db`. Khi chạy `main.py`, hệ thống tự tạo các bảng còn thiếu.
