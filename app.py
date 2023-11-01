from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    stop_loss_amount = None
    if request.method == 'POST':
        try:
            # 从表单获取数据
            total_capital = float(request.form['total_capital'])
            stop_loss_percentage = float(request.form['stop_loss_percentage']) / 100  # 转换为小数
            # 计算每笔交易的停损金额
            stop_loss_amount = total_capital * stop_loss_percentage
        except ValueError:
            # 如果输入不是数字，则给出错误信息
            stop_loss_amount = "请输入有效的数字。"

    return render_template('index.html', stop_loss_amount=stop_loss_amount)

@app.route('/long_position', methods=['GET', 'POST'])
def long_position():
    error = None
    long_position_size = long_stop_loss_points = None
    total_capital = request.args.get('total_capital', type=float)
    stop_loss_percentage = request.args.get('stop_loss_percentage', type=float) / 100
    stop_loss_amount = request.args.get('stop_loss_amount', type=float)

    if request.method == 'POST':
        try:
            long_entry_price = float(request.form['long_entry_price'])
            long_stop_loss_price = float(request.form['long_stop_loss_price'])
            long_stop_loss_points = long_entry_price - long_stop_loss_price
            if long_stop_loss_points > 0:
                long_position_size = (stop_loss_amount / long_stop_loss_points) * long_entry_price
            else:
                error = "停損價格需要小於進場價格。"
        except ValueError:
            error = "请输入有效的数字。"

    return render_template('long_position.html',
                           long_stop_loss_points=long_stop_loss_points,
                           long_position_size=long_position_size,
                           error=error)

@app.route('/short_position', methods=['GET', 'POST'])
def short_position():
    error = None
    short_position_size = short_stop_loss_points = None
    total_capital = request.args.get('total_capital', type=float)
    stop_loss_percentage = request.args.get('stop_loss_percentage', type=float) / 100
    stop_loss_amount = request.args.get('stop_loss_amount', type=float)

    if request.method == 'POST':
        try:
            short_entry_price = float(request.form['short_entry_price'])
            short_stop_loss_price = float(request.form['short_stop_loss_price'])
            short_stop_loss_points = short_stop_loss_price - short_entry_price
            if short_stop_loss_points > 0:
                short_position_size = (stop_loss_amount / short_stop_loss_points) * short_entry_price
            else:
                error = "停損價格需要大於進場價格。"
        except ValueError:
            error = "请输入有效的数字。"

    return render_template('short_position.html',
                           short_stop_loss_points=short_stop_loss_points,
                           short_position_size=short_position_size,
                           error=error)

if __name__ == '__main__':
    app.run(debug=True)
