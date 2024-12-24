from flask import render_template
import math
from hotelapp.admin import *
from datetime import datetime
from flask import render_template, request, redirect, jsonify, session, url_for, flash
import dao
from flask_login import login_user, logout_user
from hotelapp import app, login, db
from hotelapp.dao import load_room_type, load_room, get_rooms_by_type, get_available_room_types_by_date, \
    get_rooms_by_type_and_date, get_reservation_by_id, add_booking, get_rent_info_by_reservation
from hotelapp.models import ChiTietThuePhong, PhieuThuePhong


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/room_option', methods=['GET'])
def room_option():
    """
    Xử lý tìm kiếm phòng theo các điều kiện khác nhau.
    """
    # Lấy tham số từ request
    loai_phong = request.args.get('loai_phong')
    ngay_nhan_phong = request.args.get('ngay_nhan_phong')
    ngay_tra_phong = request.args.get('ngay_tra_phong')

    # Kiểm tra từng trường hợp
    if loai_phong and not ngay_nhan_phong and not ngay_tra_phong:
        # Tìm kiếm theo loại phòng
        danh_sach_loai_phong = get_rooms_by_type(loai_phong)
    elif ngay_nhan_phong and ngay_tra_phong and not loai_phong:
        # Tìm kiếm theo ngày nhận và ngày trả
        danh_sach_loai_phong = get_available_room_types_by_date(ngay_nhan_phong, ngay_tra_phong)
    elif loai_phong and ngay_nhan_phong and ngay_tra_phong:
        # Tìm kiếm theo cả loại phòng và ngày
        danh_sach_loai_phong = get_rooms_by_type_and_date(loai_phong, ngay_nhan_phong, ngay_tra_phong)
    else:
        # Trả về tất cả các loại phòng
        danh_sach_loai_phong = load_room_type()

    return render_template('room_option.html', danh_sach_loai_phong=danh_sach_loai_phong)



@app.route('/booking', methods=['GET'])
def booking():
    """
    Xử lý dữ liệu đặt phòng và hiển thị trang booking.
    """
    ma_loai_phong = request.args.get('maLoaiPhong')
    so_luong_phong = request.args.get('soLuongPhong', type=int)
    ngay_nhan_phong = request.args.get('ngayNhanPhong')
    ngay_tra_phong = request.args.get('ngayTraPhong')

    # Kiểm tra các giá trị truyền vào
    if not ma_loai_phong:
        return "Mã loại phòng không được để trống!", 400
    if so_luong_phong is None or so_luong_phong < 1:
        return "Số lượng phòng phải lớn hơn 0!", 400

    # Lấy thông tin chi tiết loại phòng từ cơ sở dữ liệu
    loai_phong = load_room_type(ma_loai_phong)

    # Render template với thông tin đặt phòng
    return render_template(
        'booking.html',
        loai_phong=loai_phong,
        so_luong_phong=so_luong_phong,
        ngay_nhan_phong=ngay_nhan_phong,
        ngay_tra_phong=ngay_tra_phong
    )


@app.route('/add_booking', methods=['POST'])
def add_booking_route():
    try:
        # Lấy dữ liệu từ form
        ngay_nhan_phong = request.form.get("ngayNhanPhong")
        ngay_tra_phong = request.form.get("ngayTraPhong")
        so_luong_phong = request.form.get("soLuongPhong")

        if not so_luong_phong:
            return jsonify({"message": "Số lượng phòng không được để trống!"}), 400

        so_luong_phong = int(so_luong_phong)  # Chuyển đổi sang số nguyên

        # Lưu thông tin khách hàng và chi tiết từng phòng
        room_details = []
        for room_number in range(1, so_luong_phong + 1):
            maPhong = request.form.get(f"maPhong_phong{room_number}")
            if not maPhong:
                return jsonify({"message": f"Mã phòng cho phòng {room_number} không được để trống!"}), 400

            hoTen = request.form.getlist(f"hoTen_phong{room_number}[]")
            cmnd = request.form.getlist(f"cmnd_phong{room_number}[]")
            diaChi = request.form.getlist(f"diaChi_phong{room_number}[]")
            loaiKhach = []  # Khởi tạo một danh sách rỗng

            for idx, name in enumerate(hoTen):
                # Lấy giá trị từ form và thêm vào danh sách loaiKhach
                loaiKhach.append(request.form.get(f"optradio_phong{room_number}_{idx + 1}"))

            # In log để kiểm tra dữ liệu
            print(f"Room {room_number}:")
            print(f"hoTen: {hoTen}")
            print(f"cmnd: {cmnd}")
            print(f"diaChi: {diaChi}")
            print(f"loaiKhach: {loaiKhach}")
            print(request.form)

            # Kiểm tra danh sách có đồng bộ
            if not (len(hoTen) == len(cmnd) == len(diaChi) ):
                return jsonify({"message": f"Thông tin khách hàng cho phòng {room_number} không đồng bộ!"}), 400

            for idx, name in enumerate(hoTen):
                room_details.append({
                    "maPhong": int(maPhong),
                    "hoTen": hoTen[idx],
                    "cmnd": cmnd[idx],
                    "diaChi": diaChi[idx],
                    "loaiKhach": loaiKhach[idx]
                })

        # Gọi hàm thêm booking từ DAO
        booking_data = {
            "ngayNhanPhong": datetime.strptime(ngay_nhan_phong, '%Y-%m-%d'),
            "ngayTraPhong": datetime.strptime(ngay_tra_phong, '%Y-%m-%d')
        }

        maPhieuDat = add_booking(room_details, booking_data)

        return jsonify({"message": "Đặt phòng thành công!", "maPhieuDat": maPhieuDat}), 200
    except ValueError as ve:
        return jsonify({"message": "Giá trị nhập vào không hợp lệ!", "error": str(ve)}), 400
    except Exception as ex:
        db.session.rollback()
        return jsonify({"message": "Có lỗi xảy ra!", "error": str(ex)}), 400

@app.route("/login", methods=['get', 'post'])
def login_process():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        u = dao.auth_user(username=username, password=password)
        if u:
            login_user(u)
            return redirect('/')

    return render_template('login.html')

@app.route("/register", methods=['get', 'post'])
def register_process():
    err_msg = None
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password.__eq__(confirm):
            data = request.form.copy()
            del data['confirm']

            avatar = request.files.get('avatar')
            dao.add_user(avatar=avatar, **data)
            return redirect('/login')
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('register.html', err_msg=err_msg)



@app.route("/logout")
def logout_process():
    logout_user()
    return redirect('/login')


@login.user_loader
def get_user_by_id(user_id):
    return dao.get_user_by_id(user_id)

@app.route("/rentonline", methods=['GET', 'POST'])
def rent_online_process():
    if request.method == 'POST':
        reservation_id = request.form.get('reservationId', '').strip()
        if not reservation_id:
            flash("Vui lòng nhập mã phiếu đặt!", "warning")
            return redirect(url_for('rent_online'))

        reservations = get_reservation_by_id(reservation_id)
        formatted_reservations = [
            {
                'maPhieuDat': r.maPhieuDat,
                'maPhong': r.maPhong,
                'ngayNhanPhong': r.ngayNhanPhong.strftime('%d/%m/%Y') if r.ngayNhanPhong else None,
                'ngayTraPhong': r.ngayTraPhong.strftime('%d/%m/%Y') if r.ngayTraPhong else None,
            }
            for r in reservations
        ]
        return render_template('rentonline.html', reservations=formatted_reservations, reservation_id=reservation_id)

    elif request.args.get('reservation_id'):
        reservation_id = request.args.get('reservation_id')
        rent_info = get_rent_info_by_reservation(reservation_id)
        if not rent_info:
            flash("Không tìm thấy thông tin phiếu thuê!", "danger")
            return redirect(url_for('rent_online'))
        return render_template('rentonline.html', rent_info=rent_info)

    return render_template('rentonline.html', reservations=[], reservation_id=None)


@app.route("/search_reservation", methods=['POST'])
def search_reservation():
    data = request.json
    reservation_id = data.get('reservationId', '').strip()

    if not reservation_id:
        return jsonify({'error': 'Mã phiếu đặt không được để trống!'}), 400

    reservations = get_reservation_by_id(reservation_id)
    if not reservations:
        return jsonify({'error': 'Không tìm thấy phiếu đặt phù hợp!'}), 404

    formatted_reservation = {
        'reservation_id': reservations[0].maPhieuDat,
        'room': reservations[0].maPhong,
        'checkin_date': reservations[0].ngayNhanPhong.strftime('%d/%m/%Y') if reservations[0].ngayNhanPhong else None,
        'checkout_date': reservations[0].ngayTraPhong.strftime('%d/%m/%Y') if reservations[0].ngayTraPhong else None,
    }
    return jsonify(formatted_reservation)

@app.route("/save_rent", methods=['POST'])
def save_rent():
    reservation_id = request.form.get('reservation_id')

    if not reservation_id:
        flash("Không tìm thấy mã phiếu đặt!", "danger")
        return redirect(url_for('rent_online_process'))

    # Lấy thông tin chi tiết từ phiếu đặt
    reservations = get_reservation_by_id(reservation_id)
    rent_info = get_rent_info_by_reservation(reservation_id)

    if not reservations or not rent_info:
        flash("Không tìm thấy thông tin phiếu đặt!", "danger")
        return redirect(url_for('rent_online_process'))

    # Tạo phiếu thuê phòng mới
    try:
        new_rent = PhieuThuePhong(
            maPhieuDat=rent_info['maPhieuDat'],
            ngayNhanPhong=rent_info['ngayNhanPhong'],
            ngayTraPhong=rent_info['ngayTraPhong'],
            maNhanVien=1  # Giả sử nhân viên có mã 1
        )
        db.session.add(new_rent)
        db.session.flush()
        if not new_rent.maPhieuThue:
            raise Exception("Không thể tạo mã phiếu thuê.")

        # Lưu các chi tiết thuê phòng
        for khach in rent_info['khach_hang']:
            rent_detail = ChiTietThuePhong(
                maPhieuThue=new_rent.maPhieuThue,
                maPhong=rent_info['maPhong'],
                maKhachHang=khach['maKhachHang']  # Gán mã khách hàng
            )
            db.session.add(rent_detail)

        db.session.commit()
        flash("Lưu và xuất phiếu thuê thành công!", "success")
    except Exception as e:
        db.session.rollback()
        print(f"Error while saving rent: {str(e)}")  # Log lỗi chi tiết
        flash(f"Có lỗi xảy ra khi lưu phiếu thuê: {str(e)}", "danger")

    return redirect(url_for('rent_online_process'))

@app.route("/rentoffline")
def rent_offline_process():
    return render_template('rentoffline.html')

if __name__ == '__main__':

    app.run(port=5001, debug=True)