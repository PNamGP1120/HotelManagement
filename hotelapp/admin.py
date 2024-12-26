from flask import redirect, request, flash
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

admin.add_view(AuthenticatedView(TaiKhoan, db.session, category='Quản lý tài khoản'))
admin.add_view(AuthenticatedView(KhachHang, db.session, category='Quản lý khách hàng'))
admin.add_view(AuthenticatedView(TrangThaiPhong, db.session, category='Quản lý phòng'))
admin.add_view(AuthenticatedView(LoaiKhachHang, db.session, category='Quản lý khách hàng'))
admin.add_view(AuthenticatedView(TrangThaiTaiKhoan, db.session, category='Quản lý tài khoản'))
admin.add_view(AuthenticatedView(VaiTro, db.session, category='Quản lý tài khoản'))
admin.add_view(AuthenticatedView(LoaiPhong, db.session, category='Quản lý phòng'))
admin.add_view(AuthenticatedView(NhanVien, db.session, category='Quản lý nhân sự'))
admin.add_view(AuthenticatedView(Phong, db.session, category='Quản lý phòng'))
admin.add_view(AuthenticatedView(PhieuDatPhong, db.session, category='Quản lý đặt phòng'))
admin.add_view(AuthenticatedView(ChiTietDatPhong, db.session, category='Quản lý đặt phòng'))
admin.add_view(AuthenticatedView(PhieuThuePhong, db.session, category='Quản lý thuê phòng'))
admin.add_view(AuthenticatedView(ChiTietThuePhong, db.session, category='Quản lý thuê phòng'))
admin.add_view(AuthenticatedView(HoaDon, db.session, category='Quản lý hóa đơn'))
admin.add_view(AuthenticatedView(LichSuTrangThaiPhong, db.session, category='Quản lý phòng'))




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
        # stats = hotelapp.dao.get_room_statistics(selected_month, selected_year)
        if f"Không có dữ liệu doanh thu cho tháng {selected_month}, năm {selected_year}." == stats:
            stats = ''
        total = 0
        print(stats)
        try:
            total = sum([s[2] for s in stats if s[2]])  # Tính tổng doanh thu
        except Exception as e:
            total = 0


        return self.render('admin/stats.html', stats = stats)


    def is_accessible(self):
        return current_user.is_authenticated and current_user.vaiTro == 1

admin.add_view(StatsView(name = "Doanh thu",category='Thống kê' ))
admin.add_view(LogoutView(name='Đăng xuất'))

class RegisterAdminView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        if request.method == 'POST':
            password = request.form.get('password')
            confirm = request.form.get('confirm')

            if password.__eq__(confirm):
                name = request.form.get('name')
                username = request.form.get('username')
                cccd = request.form.get('CCCD')
                loaiKhachHang = request.form.get('loaiKhachHang')
                diaChi = request.form.get('diaChi')
                print(name)
                hotelapp.dao.add_user(fullName=name, username=username, cccd=cccd, loaiKhachHang=loaiKhachHang, diaChi=diaChi,
                             password=password, vaiTro=1)
                return redirect('/admin')
            else:
                err_msg = 'Mật khẩu KHÔNG khớp!'

        return self.render('admin/register.html')

admin.add_view(RegisterAdminView(name ='Đăng ký', endpoint='register-admin'))


class TanSuatView(BaseView):
    @expose('/')
    def index(self):
        selected_month = request.args.get('months')
        selected_year = request.args.get('years')
        stats = hotelapp.dao.doanh_thu_theo_thang(thang=selected_month, nam = selected_year)
        stats = hotelapp.dao.tan_suat_theo_thang(selected_month, selected_year)
        if f"Không có dữ liệu doanh thu cho tháng {selected_month}, năm {selected_year}." == stats:
            stats = ''
        # total = 0
        # print(stats)
        # try:
        #     total = sum([s[2] for s in stats if s[2]])  # Tính tổng doanh thu
        # except Exception as e:
        #     total = 0


        return self.render('admin/tanSuat.html', stats = stats)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.vaiTro == 1
admin.add_view(TanSuatView(name = "Tần suất",category='Thống kê' ))

class QuyDinhView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        rules = hotelapp.dao.load_rules()
        if request.method == 'POST':
            try:
                rules['dat_phong_khach_san']['thoi_gian_nhan_phong_toi_da'] = int(request.form['thoi_gian_nhan_phong_toi_da'])
                rules['suc_chua_phong']['so_khach_toi_da'] = int(request.form['so_khach_toi_da'])
                rules['gia_phong']['so_khach_co_ban'] = int(request.form['so_khach_co_ban'])
                rules['gia_phong']['phu_phi_khach_them'] = float(request.form['phu_phi_khach_them'])
                rules['gia_phong']['he_so_khach_nuoc_ngoai'] = float(request.form['he_so_khach_nuoc_ngoai'])
                hotelapp.dao.save_rules(rules)
                flash('Quy định đã được cập nhật thành công!', 'success')
            except Exception as e:
                flash(f"Đã xảy ra lỗi: {str(e)}", 'danger')
        return self.render('admin/rules.html', rules = rules)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.vaiTro == 1

admin.add_view(QuyDinhView(name = "Quy định", endpoint='update-rules' ))


