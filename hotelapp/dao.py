from hotelapp.models import TaiKhoan, Phong, LoaiPhong, ChiTietDatPhong, PhieuDatPhong, TrangThaiPhong
from hotelapp import app, db
from sqlalchemy import and_, exists
from datetime import datetime
import hashlib
import cloudinary.uploader

# def get_user_by_id(user_id):
#     return User.query.get(user_id)
#
def auth_user(username, password, role=None):
    password= '1'
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    username = 'user1'

    u = TaiKhoan.query.filter(TaiKhoan.tenDangNhap.__eq__(username), TaiKhoan.matKhau.__eq__(password))
    u = TaiKhoan.query.filter(TaiKhoan.tenDangNhap.__eq__(username),
                          TaiKhoan.matKhau.__eq__(password))

    if role:
        u = u.filter(TaiKhoan.vaiTro.__eq__(role))

    return u.first()
# with app.app_context():
#     print(auth_user('pnam', '0212'))


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
    Lấy danh sách loại phòng dựa trên loại phòng cụ thể.
    """
    return db.session.query(
        LoaiPhong.maLoaiPhong,
        LoaiPhong.tenLoaiPhong,
        LoaiPhong.hinhAnh,
        LoaiPhong.giaPhong,
        exists().where(Phong.maLoaiPhong == LoaiPhong.maLoaiPhong).where(Phong.trangThaiPhong == 1).label('coPhongTrong')
    ).filter(LoaiPhong.tenLoaiPhong == loai_phong).all()


# Tra cứu theo ngày nhận, trả
def get_available_room_types_by_date(ngay_nhan_phong, ngay_tra_phong):
    """
    Lấy danh sách các loại phòng và kiểm tra trạng thái trống trong khoảng thời gian.
    """
    ngay_nhan = datetime.strptime(ngay_nhan_phong, '%Y-%m-%d')
    ngay_tra = datetime.strptime(ngay_tra_phong, '%Y-%m-%d')

    subquery = db.session.query(ChiTietDatPhong.maPhong).join(PhieuDatPhong).filter(
        and_(
            PhieuDatPhong.ngayNhanPhong < ngay_tra,
            PhieuDatPhong.ngayTraPhong > ngay_nhan
        )
    )

    return db.session.query(
        LoaiPhong.maLoaiPhong,
        LoaiPhong.tenLoaiPhong,
        LoaiPhong.hinhAnh,
        LoaiPhong.giaPhong,
        exists().where(
            Phong.maLoaiPhong == LoaiPhong.maLoaiPhong
        ).where(Phong.trangThaiPhong == 1).where(~Phong.maPhong.in_(subquery)).label('coPhongTrong')
    ).all()


#Tra cứu theo cả loại phòng và ngaày nhận, trả
def get_rooms_by_type_and_date(loai_phong, ngay_nhan_phong, ngay_tra_phong):
    """
    Lấy danh sách loại phòng dựa trên loại phòng và kiểm tra trạng thái trống trong khoảng thời gian.
    """
    ngay_nhan = datetime.strptime(ngay_nhan_phong, '%Y-%m-%d')
    ngay_tra = datetime.strptime(ngay_tra_phong, '%Y-%m-%d')

    subquery = db.session.query(ChiTietDatPhong.maPhong).join(PhieuDatPhong).filter(
        and_(
            PhieuDatPhong.ngayNhanPhong < ngay_tra,
            PhieuDatPhong.ngayTraPhong > ngay_nhan
        )
    )

    return db.session.query(
        LoaiPhong.maLoaiPhong,
        LoaiPhong.tenLoaiPhong,
        LoaiPhong.hinhAnh,
        LoaiPhong.giaPhong,
        exists().where(
            Phong.maLoaiPhong == LoaiPhong.maLoaiPhong
        ).where(Phong.trangThaiPhong == 1).where(~Phong.maPhong.in_(subquery)).label('coPhongTrong')
    ).filter(LoaiPhong.tenLoaiPhong == loai_phong).all()


#Lấy tất cả các loại phòng
def get_all_room_types():
    """
    Lấy danh sách tất cả các loại phòng và trạng thái có phòng trống hay không.
    """
    return db.session.query(
        LoaiPhong.maLoaiPhong,
        LoaiPhong.tenLoaiPhong,
        LoaiPhong.hinhAnh,
        LoaiPhong.giaPhong,
        exists().where(Phong.maLoaiPhong == LoaiPhong.maLoaiPhong).where(Phong.trangThaiPhong == 1).label('coPhongTrong')
    ).all()