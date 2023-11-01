from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    stop_loss_amount = None

    if request.method == 'POST':
        try:
            total_capital = float(request.form['total_capital'])
            stop_loss_percentage = float(request.form['stop_loss_percentage']) / 100
            stop_loss_amount = total_capital * stop_loss_percentage

            if 'long' in request.form:
                return redirect(url_for('long_position', total_capital=total_capital, stop_loss_amount=stop_loss_amount))
            elif 'short' in request.form:
                return redirect(url_for('short_position', total_capital=total_capital, stop_loss_amount=stop_loss_amount))

        except ValueError:
            error = "请输入有效的数字。"

    return render_template('index.html', stop_loss_amount=stop_loss_amount, error=error)

@app.route('/long_position', methods=['GET', 'POST'])
def long_position():
    error = None
    long_position_size = long_stop_loss_points = None
    total_capital = request.args.get('total_capital', type=float)
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
