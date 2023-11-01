from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 从表单获取数据
        total_capital = request.form['total_capital']
        stop_loss_percentage = request.form['stop_loss_percentage']
        stop_loss_amount = request.form['stop_loss_amount']
        
        # 根据用户的选择重定向到对应的页面
        if 'long' in request.form:
            return redirect(url_for('long_position', 
                                    total_capital=total_capital, 
                                    stop_loss_percentage=stop_loss_percentage, 
                                    stop_loss_amount=stop_loss_amount))
        elif 'short' in request.form:
            return redirect(url_for('short_position', 
                                    total_capital=total_capital, 
                                    stop_loss_percentage=stop_loss_percentage, 
                                    stop_loss_amount=stop_loss_amount))
    
    # GET请求时显示表单
    return render_template('index.html')

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
