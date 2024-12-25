from flask import redirect, request
from flask_login import current_user, logout_user

import hotelapp.dao
from hotelapp import app, db
from flask_admin import Admin, BaseView, expose, AdminIndexView
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


class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', msg = "Hello")

admin = Admin(app=app, name=  "HOTEL ADMINISTRATORS", template_mode='bootstrap4', index_view=MyAdminIndex())
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

class StatsView(BaseView):
    @expose('/')
    def index(self):
        selected_month = request.args.get('months')
        selected_year = request.args.get('years')
        stats = hotelapp.dao.doanh_thu_theo_thang(thang=selected_month, nam = selected_year)
        if f"Không có dữ liệu doanh thu cho tháng {selected_month}, năm {selected_year}." == stats:
            stats = ''
        total = 0
        print(stats)
        try:
            total = sum([s[2] for s in stats if s[2]])  # Tính tổng doanh thu
        except Exception as e:
            total = 0
        return self.render('admin/stats.html', stats = stats, total = total)


    def is_accessible(self):
        return current_user.is_authenticated and current_user.vaiTro == 1

admin.add_view(StatsView(name = "Stats"))
admin.add_view(LogoutView(name='Đăng xuất'))

