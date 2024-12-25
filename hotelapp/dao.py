from sqlalchemy.exc import SQLAlchemyError

from hotelapp import app, db
from sqlalchemy import and_, exists, func, extract
from datetime import datetime
from hotelapp.models import TrangThaiPhong, LoaiKhachHang, TrangThaiTaiKhoan, VaiTro, LoaiPhong,NhanVien, KhachHang, Phong, PhieuDatPhong, ChiTietDatPhong, PhieuThuePhong, ChiTietThuePhong, HoaDon, TaiKhoan, LichSuTrangThaiPhong

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

def get_reservation_by_id(reservation_id=None):
    """
    Lấy thông tin phiếu đặt phòng dựa trên mã phiếu đặt.
    """
    query = PhieuDatPhong.query
    if reservation_id:
        query = query.filter(PhieuDatPhong.maPhieuDat == reservation_id).join(ChiTietDatPhong)

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
                phieu_dat = PhieuDatPhong(
                    maKhachHang=khach_hang.maKhachHang,
                    ngayDatPhong=datetime.now(),
                    ngayNhanPhong=booking_data["ngayNhanPhong"],
                    ngayTraPhong=booking_data["ngayTraPhong"]
                )
                db.session.add(phieu_dat)
                db.session.flush()
                flag = True
              # Lấy ID của phiếu đặt phòng

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


def doanh_thu_theo_thang(thang: int = None, nam: int = None):
    try:
        if thang is None or nam is None:
            today = datetime.today()
            thang = thang or today.month
            nam = nam or today.year

        doanh_thu = (
            db.session.query(
                Phong.maPhong.label("maPhong"),
                LoaiPhong.tenLoaiPhong.label("tenLoaiPhong"),
                func.coalesce(func.sum(HoaDon.tongCong + HoaDon.phuThu), 0).label("doanhThu")  # Sử dụng coalesce để thay 0 cho phòng không có doanh thu
            )
            .join(LoaiPhong, LoaiPhong.maLoaiPhong == Phong.maLoaiPhong)  # Liên kết đến bảng Loại Phòng
            .outerjoin(ChiTietThuePhong, ChiTietThuePhong.maPhong == Phong.maPhong)  # Sử dụng outerjoin
            .outerjoin(PhieuThuePhong, PhieuThuePhong.maPhieuThue == ChiTietThuePhong.maPhieuThue)  # Sử dụng outerjoin
            .outerjoin(HoaDon, HoaDon.maPhieuThue == PhieuThuePhong.maPhieuThue)  # Sử dụng outerjoin
            .filter(
                extract('month', HoaDon.ngayLapHoaDon) == thang,
                extract('year', HoaDon.ngayLapHoaDon) == nam
            )
            .group_by(Phong.maPhong, LoaiPhong.tenLoaiPhong)
            .order_by(Phong.maPhong)
            .all()
        )

        if not doanh_thu:
            return f"Không có dữ liệu doanh thu cho tháng {thang}, năm {nam}."

        return doanh_thu

    except SQLAlchemyError as e:
        db.session.rollback()  # Rollback nếu xảy ra lỗi
        return f"Đã xảy ra lỗi khi truy vấn dữ liệu: {str(e)}"

def tan_suat_theo_thang(thang: int = None, nam: int = None):
    try:
        if thang is None or nam is None:
            today = datetime.today()
            thang = thang or today.month
            nam = nam or today.year

        tan_suat = (
            db.session.query(
                LoaiPhong.tenLoaiPhong.label("tenLoaiPhong"),
                func.count(ChiTietThuePhong.maPhong).label("soLanSuDung")
            )
            .join(Phong, LoaiPhong.maLoaiPhong == Phong.maLoaiPhong)
            .join(ChiTietThuePhong, ChiTietThuePhong.maPhong == Phong.maPhong)
            .join(PhieuThuePhong, PhieuThuePhong.maPhieuThue == ChiTietThuePhong.maPhieuThue)
            .filter(
                extract('month', PhieuThuePhong.ngayNhanPhong) == thang,
                extract('year', PhieuThuePhong.ngayNhanPhong) == nam
            )
            .group_by(LoaiPhong.tenLoaiPhong)
            .order_by(func.count(ChiTietThuePhong.maPhong).desc())
            .all()
        )

        if not tan_suat:
            return f"Không có dữ liệu sử dụng phòng cho tháng {thang}, năm {nam}."

        return tan_suat
    except SQLAlchemyError as e:
        db.session.rollback()
        return f"Đã xảy ra lỗi khi truy vấn dữ liệu: {str(e)}"



# with app.app_context():
#     print(doanh_thu_theo_thang(thang=1))
#     print(tan_suat_theo_thang())
