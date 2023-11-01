from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # 初始化变量以防止未定义错误
    total_capital = stop_loss_percentage = stop_loss_amount = 0
    long_entry_price = long_stop_loss_price = long_position_size = 0
    short_entry_price = short_stop_loss_price = short_position_size = 0
    error = None
    long_results_shown = short_results_shown = False
    show_long_operation = show_short_operation = False  # 新增两个变量以控制显示

    if request.method == 'POST':
        try:
            # 获取表单数据
            total_capital = float(request.form.get('total_capital', 0))
            stop_loss_percentage = float(request.form.get('stop_loss_percentage', 0)) / 100  # 百分比转小数
            # 进行计算
            stop_loss_amount = total_capital * stop_loss_percentage

            # 检查是否显示做多或做空的输入字段
            if 'show_long' in request.form:
                show_long_operation = True
            elif 'show_short' in request.form:
                show_short_operation = True

            # 检查是否进行做多或做空的计算
            if 'long_calculate' in request.form:
                long_entry_price = float(request.form.get('long_entry_price', 0))
                long_stop_loss_price = float(request.form.get('long_stop_loss_price', 0))
                # 做多计算
                long_stop_loss_points = long_entry_price - long_stop_loss_price
                if long_stop_loss_points > 0:
                    long_position_size = (stop_loss_amount / long_stop_loss_points) * long_entry_price
                    long_results_shown = True
                else:
                    error = "做多停損價格應低於進場價格。"

            elif 'short_calculate' in request.form:
                short_entry_price = float(request.form.get('short_entry_price', 0))
                short_stop_loss_price = float(request.form.get('short_stop_loss_price', 0))
                # 做空计算
                short_stop_loss_points = short_stop_loss_price - short_entry_price
                if short_stop_loss_points > 0:
                    short_position_size = (stop_loss_amount / short_stop_loss_points) * short_entry_price
                    short_results_shown = True
                else:
                    error = "做空停損價格應高於進場價格。"

        except ValueError as e:
            error = "請輸入有效的數字。"

    # 将新增的变量传给模板
    return render_template('index.html',
                           total_capital=total_capital,
                           stop_loss_percentage=stop_loss_percentage * 100,  # 显示为百分比
                           stop_loss_amount=stop_loss_amount,
                           long_entry_price=long_entry_price,
                           long_stop_loss_price=long_stop_loss_price,
                           long_position_size=long_position_size,
                           short_entry_price=short_entry_price,
                           short_stop_loss_price=short_stop_loss_price,
                           short_position_size=short_position_size,
                           long_results_shown=long_results_shown,
                           short_results_shown=short_results_shown,
                           show_long_operation=show_long_operation,
                           show_short_operation=show_short_operation,
                           error=error)

if __name__ == '__main__':
    app.run(debug=True)
