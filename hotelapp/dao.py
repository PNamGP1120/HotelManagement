
from idlelib.query import Query
from hotelapp import app, db
from sqlalchemy import and_, exists
from datetime import datetime
from hotelapp.models import (
    TrangThaiPhong, LoaiKhachHang, TrangThaiTaiKhoan, VaiTro, LoaiPhong,
    NhanVien, KhachHang, Phong, PhieuDatPhong, ChiTietDatPhong,
    PhieuThuePhong, ChiTietThuePhong, HoaDon, TaiKhoan, LichSuTrangThaiPhong
)
from hotelapp import db, app
import hashlib
import cloudinary.uploader

# def get_user_by_id(user_id):
#     return User.query.get(user_id)
#
# def auth_user(username, password, role=None):
#     password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
#
#     u = User.query.filter(User.username.__eq__(username),
#                           User.password.__eq__(password))
#
#     if role:
#         u = u.filter(User.user_role.__eq__(role))
#
#     return u.first()
#
#
# def add_user(name, username, password,CCCD='1', avatar=None):
#     password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
#
#     u = User(name=name, username=username, password=password, CCCD = CCCD)
#     if avatar:
#         res = cloudinary.uploader.upload(avatar)
#         u.avatar = res.get('secure_url')
#
#     db.session.add(u)
#     db.session.commit()

def get_reservation_by_id(reservation_id):
    if not reservation_id:
        return []
    return ChiTietDatPhong.query.join(
        PhieuDatPhong, ChiTietDatPhong.maPhieuDat == PhieuDatPhong.maPhieuDat
    ).filter(PhieuDatPhong.maPhieuDat == reservation_id).with_entities(
        PhieuDatPhong.maPhieuDat,
        ChiTietDatPhong.maPhong,
        PhieuDatPhong.ngayNhanPhong,
        PhieuDatPhong.ngayTraPhong
    ).all()

def get_rent_info_by_reservation(reservation_id):
    rent_data = PhieuDatPhong.query.join(
        ChiTietDatPhong, PhieuDatPhong.maPhieuDat == ChiTietDatPhong.maPhieuDat
    ).join(
        KhachHang, ChiTietDatPhong.maKhachHang == KhachHang.maKhachHang
    ).join(
        LoaiKhachHang, KhachHang.maLoaiKhach == LoaiKhachHang.maLoaiKhach
    ).filter(PhieuDatPhong.maPhieuDat == reservation_id).with_entities(
        PhieuDatPhong.maPhieuDat,
        PhieuDatPhong.ngayNhanPhong,
        PhieuDatPhong.ngayTraPhong,
        ChiTietDatPhong.maPhong,
        KhachHang.maKhachHang,
        KhachHang.hoTen,
        KhachHang.cmnd,
        KhachHang.diaChi,
        LoaiKhachHang.tenLoaiKhach
    ).all()

    if not rent_data:
        return None

    result = {
        'maPhieuDat': rent_data[0].maPhieuDat,
        'ngayNhanPhong': rent_data[0].ngayNhanPhong,
        'ngayTraPhong': rent_data[0].ngayTraPhong,
        'maPhong': rent_data[0].maPhong,
        'khach_hang': [
            {
                'hoTen': r.hoTen,
                'cmnd': r.cmnd,
                'diaChi': r.diaChi,
                'tenLoaiKhach': r.tenLoaiKhach,
                'maKhachHang': r.maKhachHang,
            } for r in rent_data
        ]
    }

    return result

def load_room():
    return Phong.query.get()

def load_room_type(id=None):
    query = LoaiPhong.query
    if id:
        query = query.filter(LoaiPhong.maLoaiPhong == id)
    return query.all()


# Tra cứu theo loại phòng

def get_rooms_by_type(loai_phong):
    """
    Lấy danh sách loại phòng dựa trên tên loại phòng cụ thể.
    """
    return LoaiPhong.query.filter(LoaiPhong.tenLoaiPhong.__eq__(loai_phong)).all()


def get_available_room_types_by_date(ngay_nhan_phong, ngay_tra_phong):
    """
    Lấy danh sách các loại phòng có sẵn trong khoảng thời gian cụ thể.
    """
    ngay_nhan = datetime.strptime(ngay_nhan_phong, '%Y-%m-%d')
    ngay_tra = datetime.strptime(ngay_tra_phong, '%Y-%m-%d')

    subquery = db.session.query(ChiTietDatPhong.maPhong).join(PhieuDatPhong).filter(
        and_(
            PhieuDatPhong.ngayNhanPhong < ngay_tra,
            PhieuDatPhong.ngayTraPhong > ngay_nhan
        )
    )

    return LoaiPhong.query.filter(
        LoaiPhong.phong.any(
            and_(
                Phong.trangThaiPhong.is_(True),
                ~Phong.maPhong.in_(subquery)
            )
        )
    ).all()


def get_rooms_by_type_and_date(loai_phong, ngay_nhan_phong, ngay_tra_phong):
    """
    Lấy danh sách loại phòng dựa trên tên loại phòng và kiểm tra trạng thái trống trong khoảng thời gian.
    """
    ngay_nhan = datetime.strptime(ngay_nhan_phong, '%Y-%m-%d')
    ngay_tra = datetime.strptime(ngay_tra_phong, '%Y-%m-%d')

    subquery = db.session.query(ChiTietDatPhong.maPhong).join(PhieuDatPhong).filter(
        and_(
            PhieuDatPhong.ngayNhanPhong < ngay_tra,
            PhieuDatPhong.ngayTraPhong > ngay_nhan
        )
    )

    return LoaiPhong.query.filter(
        LoaiPhong.tenLoaiPhong.__eq__(loai_phong),
        LoaiPhong.phong.any(
            and_(
                Phong.trangThaiPhong.is_(True),
                ~Phong.maPhong.in_(subquery)
            )
        )
    ).all()


def add_booking(room_details, booking_data):
    try:
        # Lưu khách hàng
        for customer in room_details:
            khach_hang = KhachHang(
                hoTen=customer["hoTen"],
                cmnd=customer["cmnd"],
                diaChi=customer["diaChi"],
                maLoaiKhach=1 if customer["loaiKhach"] == "noiDia" else 2
            )
            db.session.add(khach_hang)
            db.session.flush()  # Đảm bảo ID của khách hàng có sẵn sau khi thêm

            # Lưu phiếu đặt phòng
            phieu_dat = PhieuDatPhong(
                maKhachHang=khach_hang.maKhachHang,
                ngayDatPhong=datetime.now(),
                ngayNhanPhong=booking_data["ngayNhanPhong"],
                ngayTraPhong=booking_data["ngayTraPhong"]
            )
            db.session.add(phieu_dat)
            db.session.flush()  # Lấy ID của phiếu đặt phòng

            # Lưu chi tiết đặt phòng
            chi_tiet = ChiTietDatPhong(
                maPhieuDat=phieu_dat.maPhieuDat,
                maPhong=customer["maPhong"],
                maKhachHang=khach_hang.maKhachHang
            )
            db.session.add(chi_tiet)

        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        raise ex

