from flask import render_template
import math
from datetime import datetime

from pyexpat.errors import messages
from sqlalchemy import func

from hotelapp.admin import *

from flask import render_template, request, redirect, jsonify, session, flash, url_for
from flask_login import login_user, logout_user

from hotelapp import app, login, db, dao
from hotelapp.dao import load_room_type, load_room, get_rooms_by_type, get_available_room_types_by_date, get_rooms_by_type_and_date, get_reservation_by_id, add_booking, get_rent_info_by_reservation, add_rent, check_room_availability
from hotelapp.models import ChiTietThuePhong, PhieuThuePhong, LoaiKhachHang, KhachHang



@app.route('/')
def index():
    loaiPhong = load_room_type()
    return render_template('index.html', loaiPhong = loaiPhong)

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
    booking_data = session.get('booking_data', {})
    print(booking_data)
    # Kiểm tra các giá trị truyền vào
    if not ma_loai_phong:
        return "Mã loại phòng không được để trống!", 400
    if so_luong_phong is None or so_luong_phong < 1:
        return "Số lượng phòng phải lớn hơn 0!", 400

    # Lấy thông tin chi tiết loại phòng từ cơ sở dữ liệu
    loai_phong = load_room_type(ma_loai_phong)
    if ngay_nhan_phong:
        available_rooms = check_room_availability(ngay_nhan_phong, ngay_tra_phong, so_luong_phong, ma_loai_phong)
        if len(available_rooms) < so_luong_phong:
            danh_sach_loai_phong = load_room_type()
            messages = "Không còn đủ phòng trống trong khoảng thời gian bạn chọn!"
            return render_template('room_option.html', danh_sach_loai_phong=danh_sach_loai_phong, error_messages=messages)

    # Render template với thông tin đặt phòng
    return render_template(
        'booking.html',
        ma_loai_phong = ma_loai_phong,
        loai_phong= loai_phong,
        so_luong_phong=so_luong_phong,
        ngay_nhan_phong=ngay_nhan_phong,
        ngay_tra_phong=ngay_tra_phong,
        booking_data=booking_data
    )


@app.route('/booking_details', methods=['POST'])
def add_booking_route():
    try:
        # Lấy dữ liệu từ form
        ngay_nhan_phong = datetime.strptime(request.form.get("ngayNhanPhong"), '%Y-%m-%d').date()
        ngay_tra_phong = datetime.strptime(request.form.get("ngayTraPhong"), '%Y-%m-%d').date()
        so_luong_phong = request.form.get("soLuongPhong")
        ma_loai_phong = request.form.get("maLoaiPhong")

        if not so_luong_phong:
            return jsonify({"message": "Số lượng phòng không được để trống!"}), 400
        so_luong_phong = int(so_luong_phong)  # Chuyển đổi sang số nguyên

        loai_phong = load_room_type(ma_loai_phong)
        # Lấy danh sách phòng trống
        available_rooms = check_room_availability(ngay_nhan_phong, ngay_tra_phong, so_luong_phong, ma_loai_phong)
        if len(available_rooms) < so_luong_phong:
            # Lưu các thông tin đã nhập vào session
            session['booking_data'] = {
                'customer_data': request.form.to_dict(flat=False)  # Lưu toàn bộ thông tin khách hàng
            }
            print(session['booking_data'])
            flash("Không còn đủ phòng trống trong khoảng thời gian bạn chọn!", "warning")
            return redirect(request.referrer or url_for('booking_route'))

        # Lưu thông tin khách hàng và chi tiết từng phòng
        room_details = []
        for idx, maPhong in enumerate(available_rooms, start=1):
            hoTen = request.form.getlist(f"hoTen_phong{idx}[]")
            cmnd = request.form.getlist(f"cmnd_phong{idx}[]")
            diaChi = request.form.getlist(f"diaChi_phong{idx}[]")
            loaiKhach = [request.form.get(f"optradio_phong{idx}_{i + 1}") for i in range(len(hoTen))]

            # Kiểm tra danh sách có đồng bộ
            if not (len(hoTen) == len(cmnd) == len(diaChi)):
                return jsonify({"message": f"Thông tin khách hàng cho phòng {idx} không đồng bộ!"}), 400
            so_luong_khach = 0
            for i in range(len(hoTen)):
                so_luong_khach += 1
                room_details.append({
                    "maPhong": maPhong,
                    "hoTen": hoTen[i],
                    "cmnd": cmnd[i],
                    "diaChi": diaChi[i],
                    "loaiKhach": loaiKhach[i]
                })

        # Gọi hàm thêm booking từ DAO
        booking_data = {
            "ngayNhanPhong": ngay_nhan_phong,
            "ngayTraPhong": ngay_tra_phong
        }

        maPhieuDat = add_booking(room_details, booking_data)

        return render_template('booking_details.html',
                                maPhieuDat = maPhieuDat,
                                ma_loai_phong = ma_loai_phong,
                                loai_phong= loai_phong,
                                so_luong_khach = so_luong_khach,
                                so_luong_phong=so_luong_phong,
                                ngay_nhan_phong=ngay_nhan_phong,
                                ngay_tra_phong=ngay_tra_phong)
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

@app.route('/admin-login', methods = ['POST'])
def login_admin():
    username = request.form.get('username')
    password = request.form.get('password')

    u = dao.auth_user(username=username, password=password, role = 1)
    if u:
        login_user(u)
        return redirect('/admin')


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
    return dao.get_user_by_id(int(user_id))

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

    try:
        # Lấy thông tin chi tiết từ phiếu đặt
        rent_info = get_rent_info_by_reservation(reservation_id)
        if not rent_info:
            flash("Không tìm thấy thông tin phiếu đặt!", "danger")
            return redirect(url_for('rent_online_process'))

        # Tạo phiếu thuê phòng mới
        new_rent = PhieuThuePhong(
            maPhieuDat=rent_info['maPhieuDat'],
            ngayNhanPhong=rent_info['ngayNhanPhong'],
            ngayTraPhong=rent_info['ngayTraPhong'],
            maNhanVien=1  # Giả sử nhân viên có mã 1
        )
        db.session.add(new_rent)
        db.session.flush()

        for khach in rent_info['khach_hang']:
            rent_detail = ChiTietThuePhong(
                maPhieuThue=new_rent.maPhieuThue,
                maPhong=rent_info['maPhong'],
                maKhachHang=khach['maKhachHang']
            )
            db.session.add(rent_detail)

        db.session.commit()

        # Chuyển hướng sang trang receipt với mã phiếu thuê
        return redirect(url_for('receipt_process', maPhieuThue=new_rent.maPhieuThue))

    except Exception as e:
        db.session.rollback()
        print(f"Error while saving rent: {str(e)}")
        flash(f"Có lỗi xảy ra khi lưu phiếu thuê: {str(e)}", "danger")

    return redirect(url_for('rent_online_process'))

@app.route("/rentoffline")
def rentoffline():
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
        'rentoffline.html',
        loai_phong=loai_phong,
        so_luong_phong=so_luong_phong,
        ngay_nhan_phong=ngay_nhan_phong,
        ngay_tra_phong=ngay_tra_phong
    )

@app.route('/add_rent', methods=['POST'])
def add_rent_route():
    try:
        # Lấy dữ liệu từ form
        ngay_nhan_phong = datetime.strptime(request.form.get("ngayNhanPhong"), '%Y-%m-%d').date()
        ngay_tra_phong = datetime.strptime(request.form.get("ngayTraPhong"), '%Y-%m-%d').date()
        so_luong_phong = request.form.get("soLuongPhong")
        ma_loai_phong = request.form.get("maLoaiPhong")

        if not so_luong_phong:
            return jsonify({"message": "Số lượng phòng không được để trống!"}), 400
        so_luong_phong = int(so_luong_phong)  # Chuyển đổi sang số nguyên

        loai_phong = load_room_type(ma_loai_phong)
        # Lấy danh sách phòng trống
        available_rooms = check_room_availability(ngay_nhan_phong, ngay_tra_phong, so_luong_phong, ma_loai_phong)
        if len(available_rooms) < so_luong_phong:
            messages = "Không còn đủ phòng trống trong khoảng thời gian bạn chọn!"
            flash(messages, "warning")  # Gửi thông báo đến trang /booking
            return redirect(request.referrer or url_for('rentoffline'))  # Quay lại URL trước hoặc mặc định về /booking

        # Lưu thông tin khách hàng và chi tiết từng phòng
        room_details = []
        for idx, maPhong in enumerate(available_rooms, start=1):
            hoTen = request.form.getlist(f"hoTen_phong{idx}[]")
            cmnd = request.form.getlist(f"cmnd_phong{idx}[]")
            diaChi = request.form.getlist(f"diaChi_phong{idx}[]")
            loaiKhach = [request.form.get(f"optradio_phong{idx}_{i + 1}") for i in range(len(hoTen))]

            # Kiểm tra danh sách có đồng bộ
            if not (len(hoTen) == len(cmnd) == len(diaChi)):
                return jsonify({"message": f"Thông tin khách hàng cho phòng {idx} không đồng bộ!"}), 400
            so_luong_khach = 0
            for i in range(len(hoTen)):
                so_luong_khach += 1
                room_details.append({
                    "maPhong": maPhong,
                    "hoTen": hoTen[i],
                    "cmnd": cmnd[i],
                    "diaChi": diaChi[i],
                    "loaiKhach": loaiKhach[i]
                })

        # Gọi hàm thêm booking từ DAO
        booking_data = {
            "ngayNhanPhong": ngay_nhan_phong,
            "ngayTraPhong": ngay_tra_phong
        }

        maPhieuThue = add_rent(room_details, booking_data)
        return jsonify({"message": "Thuê Phòng Thành Công"}), 400
        # return render_template('booking_details.html',
        #                        maPhieuDat=maPhieuDat,
        #                        ma_loai_phong=ma_loai_phong,
        #                        loai_phong=loai_phong,
        #                        so_luong_khach=so_luong_khach,
        #                        so_luong_phong=so_luong_phong,
        #                        ngay_nhan_phong=ngay_nhan_phong,
        #                        ngay_tra_phong=ngay_tra_phong)
    except ValueError as ve:
        return jsonify({"message": "Giá trị nhập vào không hợp lệ!", "error": str(ve)}), 400
    except Exception as ex:
        db.session.rollback()
        return jsonify({"message": "Có lỗi xảy ra!", "error": str(ex)}), 400


@app.route("/receipt", methods=['GET'])
def receipt_process():
    maPhieuThue = request.args.get('maPhieuThue')
    if not maPhieuThue:
        flash("Không tìm thấy mã phiếu thuê!", "danger")
        return redirect(url_for('rent_online_process'))

    # Truy vấn thông tin phiếu thuê và các chi tiết liên quan
    rent = PhieuThuePhong.query.filter_by(maPhieuThue=maPhieuThue).first()
    if not rent:
        flash("Không tìm thấy thông tin phiếu thuê!", "danger")
        return redirect(url_for('rent_online_process'))

    rent_details = ChiTietThuePhong.query.filter_by(maPhieuThue=maPhieuThue).join(
        KhachHang, ChiTietThuePhong.maKhachHang == KhachHang.maKhachHang
    ).join(LoaiKhachHang, KhachHang.maLoaiKhach == LoaiKhachHang.maLoaiKhach
    ).with_entities(
        ChiTietThuePhong.maPhong,
        KhachHang.hoTen,
        KhachHang.cmnd,
        KhachHang.diaChi,
        LoaiKhachHang.tenLoaiKhach
    ).all()

    # Chuẩn bị dữ liệu để render
    rent_info = {
        'maPhieuThue': rent.maPhieuThue,
        'maPhieuDat': rent.maPhieuDat,
        'ngayNhanPhong': rent.ngayNhanPhong.strftime('%d/%m/%Y'),
        'ngayTraPhong': rent.ngayTraPhong.strftime('%d/%m/%Y'),
        'khach_hang': [
            {
                'hoTen': detail.hoTen,
                'cmnd': detail.cmnd,
                'diaChi': detail.diaChi,
                'tenLoaiKhach': detail.tenLoaiKhach
            } for detail in rent_details
        ]
    }
    return render_template('receipt.html', rent_info=rent_details)

if __name__ == '__main__':

    app.run(port=5001, debug=True)