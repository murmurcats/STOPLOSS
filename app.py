from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # 初始化变量以防止未定义错误
    stop_loss_amount = long_stop_loss_points = long_position_size = 0
    short_stop_loss_points = short_position_size = 0
    error = None

    if request.method == 'POST':
        try:
            # 获取表单数据
            total_capital = float(request.form.get('total_capital', 0))
            stop_loss_percentage = float(request.form.get('stop_loss_percentage', 0)) / 100  # 百分比转小数
            long_entry_price = float(request.form.get('long_entry_price', 0))
            long_stop_loss_price = float(request.form.get('long_stop_loss_price', 0))
            short_entry_price = float(request.form.get('short_entry_price', 0))
            short_stop_loss_price = float(request.form.get('short_stop_loss_price', 0))

            # 进行计算
            stop_loss_amount = total_capital * stop_loss_percentage
            long_stop_loss_points = long_entry_price - long_stop_loss_price
            long_position_size = stop_loss_amount / long_stop_loss_points if long_stop_loss_points else 0
            short_stop_loss_points = short_entry_price - short_stop_loss_price
            short_position_size = stop_loss_amount / short_stop_loss_points if short_stop_loss_points else 0
        except ValueError as e:
            error = "请输入有效的数字。"

    # 不管是GET请求还是POST请求，都渲染同一个页面，但是POST请求会带有计算结果
    return render_template('index.html',
                           stop_loss_amount=stop_loss_amount,
                           long_stop_loss_points=long_stop_loss_points,
                           long_position_size=long_position_size,
                           short_stop_loss_points=short_stop_loss_points,
                           short_position_size=short_position_size,
                           error=error)

if __name__ == '__main__':
    app.run(debug=True)
