
from flask import redirect
from flask_login import current_user, logout_user

from hotelapp import app, db
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from hotelapp.models import (TrangThaiPhong,
                             LoaiKhachHang,
                             TrangThaiTaiKhoan,
                             VaiTro,
                             LoaiPhong,
                             NhanVien,
                             KhachHang,
                             Phong,
                             PhieuDatPhong,
                             ChiTietDatPhong,
                             PhieuThuePhong,
                             ChiTietThuePhong,
                             HoaDon,
                             TaiKhoan)

admin = Admin(app=app, name=  "HOTEL ADMINISTRATORS", template_mode='bootstrap4',url='/admin')
class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.vaiTro == 1

admin.add_view(AuthenticatedView(TaiKhoan, db.session))
admin.add_view(AuthenticatedView(KhachHang, db.session))
admin.add_view(AuthenticatedView(TrangThaiPhong, db.session))
admin.add_view(AuthenticatedView(LoaiKhachHang, db.session))
admin.add_view(AuthenticatedView(TrangThaiTaiKhoan, db.session))
admin.add_view(AuthenticatedView(VaiTro, db.session))
admin.add_view(AuthenticatedView(LoaiPhong, db.session))
admin.add_view(AuthenticatedView(NhanVien, db.session))
admin.add_view(AuthenticatedView(Phong, db.session))
admin.add_view(AuthenticatedView(PhieuDatPhong, db.session))
admin.add_view(AuthenticatedView(ChiTietDatPhong, db.session))
admin.add_view(AuthenticatedView(PhieuThuePhong, db.session))
admin.add_view(AuthenticatedView(ChiTietThuePhong, db.session))
admin.add_view(AuthenticatedView(HoaDon, db.session))





class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

admin.add_view(LogoutView(name='Đăng xuất'))




# class SecureModelView(ModelView):
#     """
#     ModelView có thêm lớp bảo mật: chỉ cho phép admin truy cập.
#     # """
#     # def is_accessible(self):
#     #     return current_user.is_authenticated and current_user.role == 'admin'
#     #
#     # def inaccessible_callback(self, name, **kwargs):
#     #     return redirect(url_for('login'))
# class KhachHangView(SecureModelView):
#     column_list = ['maKhachHang', 'hoTen', 'cmnd', 'diaChi', 'loaiKhach.tenLoaiKhach']
#     column_searchable_list = ['hoTen', 'cmnd']
#     column_filters = ['maLoaiKhach']
#     column_labels = {
#         'maKhachHang': 'Mã Khách Hàng',
#         'hoTen': 'Họ Tên',
#         'cmnd': 'CMND',
#         'diaChi': 'Địa Chỉ',
#         'loaiKhach.tenLoaiKhach': 'Loại Khách'
#     }
#
#
#
# class PhieuDatPhongView(SecureModelView):
#     column_list = ['maPhieuDat', 'khachHang.hoTen', 'ngayDatPhong', 'ngayNhanPhong', 'ngayTraPhong', 'chiTietDatPhong.maChiTietPhieuDat']
#     column_searchable_list = ['ngayNhanPhong', 'ngayTraPhong']
#     column_filters = ['ngayDatPhong']
#     column_labels = {
#         'maPhieuDat': 'Mã Phiếu Đặt',
#         'khachHang.hoTen': 'Khách Hàng',
#         'ngayDatPhong': 'Ngày Đặt Phòng',
#         'ngayNhanPhong': 'Ngày Nhận Phòng',
#         'ngayTraPhong': 'Ngày Trả Phòng',
#         'chiTietDatPhong.maChiTietPhieuDat': 'Chi Tiết Đặt Phòng'
#     }
#     form_columns = ['maPhieuDat', 'khachHang', 'ngayDatPhong', 'ngayNhanPhong', 'ngayTraPhong', 'chiTietDatPhong']
#
# class PhongView(SecureModelView):
#     column_list = ['maPhong', 'maLoaiPhong', 'trangThaiPhong']
#     column_searchable_list = ['maLoaiPhong']
#     column_filters = ['trangThaiPhong']
#     column_labels = {
#         'maPhong': 'Mã Phòng',
#         'maLoaiPhong': 'Loại Phòng',
#         'trangThaiPhong': 'Trạng Thái Phòng'
#     }
# class LoaiPhongView(SecureModelView):
#     column_list = ['maLoaiPhong', 'tenLoaiPhong', 'giaPhong', 'moTa']
#     column_searchable_list = ['tenLoaiPhong']
#     column_labels = {
#         'maLoaiPhong': 'Mã Loại Phòng',
#         'tenLoaiPhong': 'Tên Loại Phòng',
#         'giaPhong': 'Giá Phòng',
#         'moTa': 'Mô Tả'
#     }
#
# class ChiTietDatPhongView(SecureModelView):
#     column_list = ['phieuDatPhong.maPhieuDat', 'phong.maPhong', 'khachHang.hoTen']
#     column_labels = {
#         'phieuDatPhong.maPhieuDat': 'Mã Phiếu Đặt',
#         'phong.maPhong': 'Phòng',
#         'khachHang.hoTen': 'Khách Hàng'
#     }
# # Thêm các bảng vào Flask-Admin
# admin.add_view(KhachHangView(KhachHang, db.session, name='Khách Hàng'))
# admin.add_view(PhieuDatPhongView(PhieuDatPhong, db.session, name='Phiếu Đặt Phòng'))
# admin.add_view(PhongView(Phong, db.session, name='Phòng'))
# admin.add_view(LoaiPhongView(LoaiPhong, db.session, name='Loại Phòng'))
# admin.add_view(ChiTietDatPhongView(ChiTietDatPhong, db.session, name='Chi Tiết Đặt Phòng'))

