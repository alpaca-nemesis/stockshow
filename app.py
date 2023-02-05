from markupsafe import escape
from flask import Flask
from flask import render_template
from flask_apscheduler import APScheduler
from DBhandle import stockView
import schedule

app = Flask(__name__, static_folder='static', template_folder='template')


# --------------页面配置------------
@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/kline/<stock_id>')
def hello(stock_id):
    columns, prices = stockView.viewStockPrice(stock=stock_id)
    print(type(prices))

    return render_template('showKline.html', stock_id=stock_id, prices=prices)


if __name__ == '__main__':
    app.config.from_object(schedule.ScheduleConfig())      # 为实例化的 flask 引入配置
    scheduler = APScheduler()                  # 实例化 APScheduler
    scheduler.init_app(app)                    # 把任务列表放入 flask
    scheduler.start()                          # 启动任务列表
    app.debug = True
    app.run()
