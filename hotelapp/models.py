from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship, backref
from wtforms.validators import email

from hotelapp import db, app
from flask_login import UserMixin

class TrangThaiPhong(db.Model):
    __tablename__ = 'TrangThaiPhong'
    maTrangThai = db.Column(db.Integer, primary_key=True)
    tenTrangThai = db.Column(db.String(100), nullable=False)

    phong = relationship('Phong', backref=backref('trangThai', lazy=True))

class LoaiKhachHang(db.Model):
    __tablename__ = 'LoaiKhachHang'
    maLoaiKhach = db.Column(db.Integer, primary_key=True)
    tenLoaiKhach = db.Column(db.String(100), nullable=False)

    khachHang = relationship('KhachHang', backref=backref('loaiKhach', lazy=True))

class TrangThaiTaiKhoan(db.Model):
    __tablename__ = 'TrangThaiTaiKhoan'
    maTrangThai = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tenTrangThai = db.Column(db.String(100), nullable=False)
    taiKhoan = db.relationship('TaiKhoan', backref=backref('trangThaiTaiKhoan', lazy=True))


class VaiTro(db.Model):
    __tablename__ = 'VaiTro'
    maVaiTro = db.Column(db.Integer, primary_key=True)
    tenVaiTro = db.Column(db.String(100), nullable=False)

    taiKhoan = relationship('TaiKhoan', backref=backref('vaiTroTaiKhoan', lazy=True))

class LoaiPhong(db.Model):
    __tablename__ = 'LoaiPhong'
    maLoaiPhong = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tenLoaiPhong = db.Column(db.String(100), nullable=False)
    giaPhong = db.Column(db.Integer, nullable=False)
    moTa = db.Column(db.String(200), nullable=False)
    hinhAnh = db.Column(db.String(200))

    phong = relationship('Phong', backref=backref('loaiPhong', lazy=True))

class NhanVien(db.Model):
    __tablename__ = 'NhanVien'
    maNhanVien = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hoTen = db.Column(db.String(100), nullable=False)
    cmnd = db.Column(db.String(20), unique=True, nullable=False)
    diaChi = db.Column(db.String(255))
    maTaiKhoan = db.Column(db.Integer, db.ForeignKey('TaiKhoan.maTaiKhoan'), nullable = True)
    phieuThuePhong = relationship('PhieuThuePhong', backref=backref('nhanVien', lazy=True))

class KhachHang(db.Model):
    __tablename__ = 'KhachHang'
    maKhachHang = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hoTen = db.Column(db.String(100), nullable=False)
    cmnd = db.Column(db.String(20), unique=True, nullable=False)
    diaChi = db.Column(db.String(255))
    maLoaiKhach = db.Column(db.Integer, db.ForeignKey('LoaiKhachHang.maLoaiKhach'), nullable=False)
    maTaiKhoan = db.Column(db.Integer, db.ForeignKey('TaiKhoan.maTaiKhoan'), nullable=True)
    phieuDatPhong = relationship('PhieuDatPhong', backref=backref('khachHang', lazy=True))
    chiTietDatPhong = relationship('ChiTietDatPhong', backref=backref('khachHang', lazy=True))
    chiTietThuePhong = relationship('ChiTietThuePhong', backref=backref('khachHang', lazy=True))

class Phong(db.Model):
    __tablename__ = 'Phong'
    maPhong = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trangThaiPhong = db.Column(db.Integer, db.ForeignKey('TrangThaiPhong.maTrangThai'), nullable=False)
    maLoaiPhong = db.Column(db.Integer, db.ForeignKey('LoaiPhong.maLoaiPhong'), nullable=False)
    chiTietDatPhong = relationship('ChiTietDatPhong', backref=backref('phong', lazy=True))
    chiTietThuePhong = relationship('ChiTietThuePhong', backref=backref('phong', lazy=True))


class PhieuDatPhong(db.Model):
    __tablename__ = 'PhieuDatPhong'
    maPhieuDat = db.Column(db.Integer, primary_key=True, autoincrement=True)
    maKhachHang = db.Column(db.Integer, db.ForeignKey('KhachHang.maKhachHang'), nullable=False)
    ngayDatPhong = db.Column(db.Date, nullable=False)
    ngayNhanPhong = db.Column(db.Date, nullable=False)
    ngayTraPhong = db.Column(db.Date, nullable=False)
    chiTietDatPhong = relationship('ChiTietDatPhong', backref=backref('phieuDatPhong', lazy=True))
    phieuThuePhong = relationship('PhieuThuePhong', backref=backref('phieuDatPhong', lazy=True))

class ChiTietDatPhong(db.Model):
    __tablename__ = 'ChiTietDatPhong'
    maChiTietPhieuDat = db.Column(db.Integer, primary_key=True, autoincrement=True)
    maPhieuDat = db.Column(db.Integer, db.ForeignKey('PhieuDatPhong.maPhieuDat'), nullable=False)
    maPhong = db.Column(db.Integer, db.ForeignKey('Phong.maPhong'), nullable=False)
    maKhachHang = db.Column(db.Integer, db.ForeignKey('KhachHang.maKhachHang'), nullable=False)

class PhieuThuePhong(db.Model):
    __tablename__ = 'PhieuThuePhong'
    maPhieuThue = db.Column(db.Integer, primary_key=True, autoincrement=True)
    maPhieuDat = db.Column(db.Integer, db.ForeignKey('PhieuDatPhong.maPhieuDat'))
    maKhachHang = db.Column(db.Integer, db.ForeignKey('KhachHang.maKhachHang'), nullable=False)
    ngayNhanPhong = db.Column(db.Date, nullable=False)
    ngayTraPhong = db.Column(db.Date, nullable=False)
    maNhanVien = db.Column(db.Integer, db.ForeignKey('NhanVien.maNhanVien'), nullable=False)
    chiTietThuePhong = relationship('ChiTietThuePhong', backref=backref('phieuThuePhong', lazy=True))
    hoaDon = relationship('HoaDon', backref=backref('phieuThuePhong', lazy=True))

class ChiTietThuePhong(db.Model):
    __tablename__ = 'ChiTietThuePhong'
    maChiTietPhieuThue = db.Column(db.Integer, primary_key=True, autoincrement=True)
    maPhieuThue = db.Column(db.Integer, db.ForeignKey('PhieuThuePhong.maPhieuThue'), nullable=False)
    maPhong = db.Column(db.Integer, db.ForeignKey('Phong.maPhong'), nullable=False)
    maKhachHang = db.Column(db.Integer, db.ForeignKey('KhachHang.maKhachHang'), nullable=False)

class HoaDon(db.Model):
    __tablename__ = 'HoaDon'
    maHoaDon = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ngayLapHoaDon = db.Column(db.Date)
    phuThu = db.Column(db.Numeric(10, 2), nullable=False)
    tongCong = db.Column(db.Numeric(10, 2), nullable=False)
    maPhieuThue = db.Column(db.Integer, db.ForeignKey('PhieuThuePhong.maPhieuThue'), nullable=False)

class TaiKhoan(db.Model, UserMixin):
    __tablename__ = 'TaiKhoan'
    maTaiKhoan = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tenDangNhap = db.Column(db.String(100), unique=True, nullable=False)
    matKhau = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    trangThai = db.Column(db.Integer, db.ForeignKey('TrangThaiTaiKhoan.maTrangThai'), nullable=False)
    vaiTro = db.Column(db.Integer, db.ForeignKey('VaiTro.maVaiTro'), nullable=False)
    khachHang = relationship("KhachHang", backref=backref("taiKhoan", lazy="joined"), uselist=False)
    nhanVien = relationship("NhanVien", backref=backref("taiKhoan", lazy="joined"), uselist=False)

    def get_id(self):
        return str(self.maTaiKhoan)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        import hashlib

        trang_thai_phong = [
            TrangThaiPhong(maTrangThai=1, tenTrangThai="Trống"),
            TrangThaiPhong(maTrangThai=2, tenTrangThai="Đang sử dụng"),
            TrangThaiPhong(maTrangThai=3, tenTrangThai="Đang bảo trì"),
        ]

        loai_khach_hang = [
            LoaiKhachHang(maLoaiKhach=1, tenLoaiKhach="Nội Địa"),
            LoaiKhachHang(maLoaiKhach=2, tenLoaiKhach="Nước Ngoài"),
        ]

        trang_thai_tai_khoan = [
            TrangThaiTaiKhoan(maTrangThai=1, tenTrangThai="Hoạt động"),
            TrangThaiTaiKhoan(maTrangThai=2, tenTrangThai="Đã khóa"),
        ]

        vai_tro = [
            VaiTro(maVaiTro=1, tenVaiTro="Admin"),
            VaiTro(maVaiTro=2, tenVaiTro="NhanVien"),
            VaiTro(maVaiTro=3, tenVaiTro="KhachHang"),
        ]

        loai_phong = [
            LoaiPhong(maLoaiPhong=1,tenLoaiPhong="Standard", giaPhong=500000, moTa="Phòng đơn giản, gia đình, không ban công, không sofa", hinhAnh="assets/room1.png"),
            LoaiPhong(maLoaiPhong=2,tenLoaiPhong="Delux", giaPhong=1000000, moTa="Phòng sang trọng, cặp đôi, không ban công, sofa êm đẹp", hinhAnh="assets/room2.png"),
            LoaiPhong(maLoaiPhong=3, tenLoaiPhong="VIP", giaPhong=2000000, moTa="Phòng cao cấp, ban công thoáng mát view thành phố, sofa êm ái đẹp",hinhAnh="assets/room3.png"),
        ]

        # Thêm dữ liệu mẫu vào bảng chính
        nhan_vien = [
            NhanVien(maNhanVien=1, hoTen="Nguyễn Văn A", cmnd="012345678901", diaChi="Hà Nội", maTaiKhoan=2),
            NhanVien(maNhanVien=2, hoTen="Trần Thị B", cmnd="987654321098", diaChi="Hồ Chí Minh", maTaiKhoan=3),
        ]

        khach_hang = [
            KhachHang(maKhachHang=1, hoTen="Lê Văn C", cmnd="123456789012", diaChi="Đà Nẵng", maLoaiKhach=1, maTaiKhoan=4),
            KhachHang(maKhachHang=2, hoTen="Phạm Thị D", cmnd="210987654321", diaChi="Huế", maLoaiKhach=2, maTaiKhoan=5),
            KhachHang(maKhachHang=3, hoTen="Trần Văn E", cmnd="140936674321", diaChi="Phú Yên", maLoaiKhach=1),
            KhachHang(maKhachHang=4, hoTen="Nguyễn Tấn L", cmnd="760987654321", diaChi="Sài Gòn", maLoaiKhach=2),

        ]

        phong = [
            Phong(maPhong=1, trangThaiPhong=1, maLoaiPhong=1),
            Phong(maPhong=2, trangThaiPhong=2, maLoaiPhong=1),
            Phong(maPhong=3, trangThaiPhong=3, maLoaiPhong=3),
            Phong(maPhong=4, trangThaiPhong=1, maLoaiPhong=2),
            Phong(maPhong=5, trangThaiPhong=1, maLoaiPhong=2),
            Phong(maPhong=6, trangThaiPhong=1, maLoaiPhong=3),
            Phong(maPhong=7, trangThaiPhong=1, maLoaiPhong=1),
        ]

        phieu_dat_phong = [
            PhieuDatPhong(maPhieuDat=1, maKhachHang=1, ngayDatPhong="2024-12-01", ngayNhanPhong="2024-12-05",
                          ngayTraPhong="2024-12-10"),
        ]

        chi_tiet_dat_phong = [
            ChiTietDatPhong(maPhieuDat=1, maPhong=1, maKhachHang=1),
        ]

        phieu_thue_phong = [
            PhieuThuePhong(maPhieuThue=1, maPhieuDat=1, maKhachHang= 1, ngayNhanPhong="2024-12-05", ngayTraPhong="2024-12-10",
                           maNhanVien=1),
        ]

        chi_tiet_thue_phong = [
            ChiTietThuePhong(maChiTietPhieuThue=1, maPhieuThue=1, maPhong=1, maKhachHang=1),
        ]

        hoa_don = [
            HoaDon(maHoaDon=1, ngayLapHoaDon="2024-12-11", phuThu=50000, tongCong=550000, maPhieuThue=1),
        ]

        tai_khoan = [
            TaiKhoan(maTaiKhoan=1, tenDangNhap="admin", matKhau="hashed_password", email="admin@gmail.com", trangThai=1, vaiTro=1),
            TaiKhoan(maTaiKhoan=2, tenDangNhap="nhanvien1", matKhau="123", email="nhanvien1@gmail.com", trangThai=1, vaiTro=2),
            TaiKhoan(maTaiKhoan=3, tenDangNhap="nhanvien2", matKhau="123", email="nhanvien2@gmail.com",trangThai=1, vaiTro=2),
            TaiKhoan(maTaiKhoan=4, tenDangNhap="khachhang1", matKhau="123", email="khachhang1@gmail.com", trangThai=1,vaiTro=3),
            TaiKhoan(maTaiKhoan=5, tenDangNhap="khachhang2", matKhau="123", email="khachhang2@gmail.com", trangThai=1,vaiTro=3),
        ]


        # Lưu tất cả vào database
        db.session.add_all(trang_thai_phong)
        db.session.add_all(loai_khach_hang)
        db.session.add_all(trang_thai_tai_khoan)
        db.session.add_all(vai_tro)
        db.session.add_all(tai_khoan)
        db.session.add_all(loai_phong)
        db.session.commit()
        db.session.add_all(nhan_vien)
        db.session.add_all(khach_hang)
        db.session.add_all(phong)
        db.session.add_all(phieu_dat_phong)
        db.session.commit()
        db.session.add_all(chi_tiet_dat_phong)
        db.session.commit()
        db.session.add_all(phieu_thue_phong)
        db.session.commit()
        db.session.add_all(chi_tiet_thue_phong)
        db.session.commit()
        db.session.add_all(hoa_don)
        db.session.commit()
