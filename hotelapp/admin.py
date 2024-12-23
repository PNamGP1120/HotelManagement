from hotelapp import app, db
from flask_admin import Admin
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

admin.add_view(ModelView(TaiKhoan, db.session))
admin.add_view(ModelView(KhachHang, db.session))
admin.add_view(ModelView(TrangThaiPhong, db.session))
admin.add_view(ModelView(LoaiKhachHang, db.session))
admin.add_view(ModelView(TrangThaiTaiKhoan, db.session))
admin.add_view(ModelView(VaiTro, db.session))
admin.add_view(ModelView(LoaiPhong, db.session))
admin.add_view(ModelView(NhanVien, db.session))
admin.add_view(ModelView(Phong, db.session))
admin.add_view(ModelView(PhieuDatPhong, db.session))
admin.add_view(ModelView(ChiTietDatPhong, db.session))
admin.add_view(ModelView(PhieuThuePhong, db.session))
admin.add_view(ModelView(ChiTietThuePhong, db.session))
admin.add_view(ModelView(HoaDon, db.session))
admin.add_view(ModelView(LichSuTrangThaiPhong, db.session))

