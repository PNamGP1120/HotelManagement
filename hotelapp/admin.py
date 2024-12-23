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
                             TaiKhoan,
                             LichSuTrangThaiPhong)

admin = Admin(app=app, name=  "HOTEL ADMINISTRATORS", template_mode='bootstrap4')
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
admin.add_view(AuthenticatedView(LichSuTrangThaiPhong, db.session))




class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

admin.add_view(LogoutView(name='Đăng xuất'))