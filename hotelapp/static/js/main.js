
document.addEventListener("DOMContentLoaded", function () {
    const ngayNhanPhongInput = document.getElementById("ngay_nhan_phong");
    const ngayTraPhongInput = document.getElementById("ngay_tra_phong");

    // Định dạng ngày theo chuẩn yyyy-MM-dd
    const formatDate = (d) => d.toISOString().split("T")[0];

    // Lấy ngày hiện tại
    const today = new Date();
    const todayFormatted = formatDate(today);

    // Đặt giá trị min cho ngày nhận phòng (không cho phép chọn ngày trong quá khứ)
    ngayNhanPhongInput.min = todayFormatted;

    // Lắng nghe sự kiện thay đổi ngày nhận phòng
    ngayNhanPhongInput.addEventListener("change", function () {
        const ngayNhanPhong = this.value;

        if (ngayNhanPhong) {
            // Chuyển giá trị sang đối tượng Date
            const date = new Date(ngayNhanPhong);

            // Tính ngày tối đa (28 ngày sau ngày nhận phòng)
            const maxDate = new Date(date);
            maxDate.setDate(date.getDate() + 28);

            // Cập nhật thuộc tính min và max cho ngày trả phòng
            ngayTraPhongInput.min = formatDate(date);
            ngayTraPhongInput.max = formatDate(maxDate);

            // Bật lại input ngày trả phòng
            ngayTraPhongInput.disabled = false;
        } else {
            // Nếu không có giá trị, reset các thuộc tính
            ngayTraPhongInput.min = "";
            ngayTraPhongInput.max = "";
            ngayTraPhongInput.disabled = true;
        }
    });
});


//Add - Del Customers
document.addEventListener("DOMContentLoaded", function () {
    const maxGuestsPerRoom = 3;

    const roomContainers = document.querySelectorAll(".room-info");

    roomContainers.forEach((room, index) => {
        const addButton = room.querySelector(".add-customer");
        const removeButton = room.querySelector(".remove-customer");
        const customerContainer = room.querySelector(".customer-container");

        let roomGuestCount = customerContainer.querySelectorAll(".customer-info").length;

        const updateButtons = () => {
            // Hiển thị hoặc ẩn nút "Thêm Khách"
            if (roomGuestCount >= maxGuestsPerRoom) {
                addButton.style.display = "none";
            } else {
                addButton.style.display = "inline-block";
            }

            // Hiển thị hoặc ẩn nút "Giảm Khách"
            if (roomGuestCount <= 1) {
                removeButton.style.display = "none";
            } else {
                removeButton.style.display = "inline-block";
            }
        };

        const addGuest = () => {
    if (roomGuestCount < maxGuestsPerRoom) {
        roomGuestCount++;

        const newCustomer = document.createElement("div");
        newCustomer.classList.add("customer-info");
        newCustomer.innerHTML = `
            <div class="fw-bold">Khách hàng ${roomGuestCount}</div>
            <div class="mb-3 mt-3">
                <input style="width: 70%; height: 50px;" type="text" class="form-control" placeholder="Họ và Tên" name="hoTen_phong${index + 1}[]" required>
            </div>
            <div class="mb-3">
                <input style="width: 70%; height: 50px;" type="text" class="form-control" placeholder="CMND" name="cmnd_phong${index + 1}[]" required>
            </div>
            <div class="mb-3">
                <input style="width: 70%; height: 50px;" type="text" class="form-control" placeholder="Địa Chỉ" name="diaChi_phong${index + 1}[]" required>
            </div>
            <div class="d-flex">
                <div class="ps-3 flex-fill" style="font-size: 1rem; color: grey;">Loại Khách</div>
                <div class="form-check flex-fill">
                    <input type="radio" class="form-check-input" name="optradio_phong${index + 1}_${roomGuestCount}" value="noiDia" checked>
                    <label class="form-check-label">Nội Địa</label>
                </div>
                <div class="form-check flex-fill">
                    <input type="radio" class="form-check-input" name="optradio_phong${index + 1}_${roomGuestCount}" value="nuocNgoai">
                    <label class="form-check-label">Nước Ngoài</label>
                </div>
            </div>
        `;
        customerContainer.appendChild(newCustomer);
        updateButtons();
    }
    };

        const removeGuest = () => {
            if (roomGuestCount > 1) {
                customerContainer.lastElementChild.remove();
                roomGuestCount--;
                updateButtons();
            }
        };

        addButton.addEventListener("click", addGuest);
        removeButton.addEventListener("click", removeGuest);

        updateButtons();
    });
});

let container = document.getElementById('container');
let count = 50;
for(var i = 0; i<50; i++){
    let leftSnow = Math.floor(Math.random() * container.clientWidth);
    let topSnow = Math.floor(Math.random() * container.clientHeight);
    let widthSnow = Math.floor(Math.random() * 50);
    let timeSnow = Math.floor((Math.random() * 5) + 5);
    let blurSnow = Math.floor(Math.random() * 10);
    console.log(leftSnow);
    let div = document.createElement('div');
    div.classList.add('snow');
    div.style.left = leftSnow + 'px';
    div.style.top = topSnow + 'px';
    div.style.width = widthSnow + 'px';
    div.style.height = widthSnow + 'px';
    div.style.animationDuration = timeSnow + 's';
    div.style.filter = "blur(" + blurSnow + "px)";
    container.appendChild(div);
}





