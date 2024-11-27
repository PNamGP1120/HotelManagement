from hotelapp import app


@app.route('/')
def index():
    return "10đ CNPM"


if __name__ == '__main__':
    app.run(debug=True)