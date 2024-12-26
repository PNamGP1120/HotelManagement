from hotelapp import app, db
from sqlalchemy import and_, exists
from datetime import datetime
from hotelapp.models import TrangThaiPhong, LoaiKhachHang, TrangThaiTaiKhoan, VaiTro, LoaiPhong,NhanVien, KhachHang, Phong, PhieuDatPhong, ChiTietDatPhong, PhieuThuePhong, ChiTietThuePhong, HoaDon, TaiKhoan

from hotelapp import db, app
import hashlib
import cloudinary.uploader

def get_user_by_id(user_id):
    return TaiKhoan.query.get(user_id)
with app.app_context():
    print(get_user_by_id(1))
def auth_user(username, password, role=None):
    # password= '1'
    # password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    # username = 'user1'

    u = TaiKhoan.query.filter(TaiKhoan.tenDangNhap.__eq__(username), TaiKhoan.matKhau.__eq__(password))


    if role:
        u = u.filter(TaiKhoan.vaiTro.__eq__(role))

    return u.first()
# with app.app_context():
#     print(auth_user('admin', 'hashed_password'))


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


# with app.app_context():
#     print(load_room_type())

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
        # Biến lưu phiếu đặt phòng
        phieu_dat = None

        for customer in room_details:
            # Lưu khách hàng
            khach_hang = KhachHang(
                hoTen=customer["hoTen"],
                cmnd=customer["cmnd"],
                diaChi=customer["diaChi"],
                maLoaiKhach=1 if customer["loaiKhach"] == "noiDia" else 2
            )
            db.session.add(khach_hang)
            db.session.flush()  # Đảm bảo ID của khách hàng có sẵn

            # Tạo phiếu đặt phòng nếu chưa tạo
            if phieu_dat is None:
                phieu_dat = PhieuDatPhong(
                    maKhachHang=khach_hang.maKhachHang,
                    ngayDatPhong=datetime.now(),
                    ngayNhanPhong=booking_data["ngayNhanPhong"],
                    ngayTraPhong=booking_data["ngayTraPhong"]
                )
                db.session.add(phieu_dat)
                db.session.flush()  # Đảm bảo ID của phiếu đặt có sẵn

            # Lưu chi tiết đặt phòng
            chi_tiet = ChiTietDatPhong(
                maPhieuDat=phieu_dat.maPhieuDat,
                maPhong=customer["maPhong"],
                maKhachHang=khach_hang.maKhachHang
            )
            db.session.add(chi_tiet)

        # Lưu thay đổi
        db.session.commit()

        # Trả về mã phiếu đặt
        return phieu_dat.maPhieuDat
    except Exception as ex:
        db.session.rollback()
        print(f"Lỗi khi lưu phiếu đặt: {ex}")
        raise ex

def add_rent(room_details, booking_data):
    try:
        # Lưu khách hàng
        flag = False
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
            if not flag:
                phieu_thue = PhieuThuePhong(
                    ngayNhanPhong=booking_data["ngayNhanPhong"],
                    ngayTraPhong=booking_data["ngayTraPhong"],
                    maNhanVien = 1
                )
                db.session.add(phieu_thue)
                db.session.flush()
                flag = True
              # Lấy ID của phiếu đặt phòng

            # Lưu chi tiết đặt phòng
            chi_tiet = ChiTietThuePhong(
                maPhieuThue=phieu_thue.maPhieuThue,
                maPhong=customer["maPhong"],
                maKhachHang=khach_hang.maKhachHang
            )
            db.session.add(chi_tiet)

        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        raise ex

def check_room_availability(ngay_nhan_phong, ngay_tra_phong, so_luong_phong, loai_phong_id):
    """
    Kiểm tra và trả về danh sách phòng trống cho một loại phòng cụ thể.
    """
    # Danh sách các phòng đã được đặt trong khoảng thời gian yêu cầu
    booked_rooms = db.session.query(ChiTietDatPhong.maPhong).join(PhieuDatPhong).filter(
        and_(
            PhieuDatPhong.ngayNhanPhong < ngay_tra_phong,
            PhieuDatPhong.ngayTraPhong > ngay_nhan_phong
        )
    ).all()
    booked_room_ids = [room[0] for room in booked_rooms]

    # Lấy danh sách phòng trống
    available_rooms = db.session.query(Phong.maPhong).filter(
        Phong.maLoaiPhong == loai_phong_id,
        Phong.trangThaiPhong.is_(True),
        ~Phong.maPhong.in_(booked_room_ids)
    ).order_by(Phong.maPhong).limit(so_luong_phong).all()

    return [room[0] for room in available_rooms]  # Trả về danh sách mã phòng trống



