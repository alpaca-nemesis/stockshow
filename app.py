from markupsafe import escape
from flask import Flask
from flask import render_template
from flask_apscheduler import APScheduler
from getData.getAkshare import isTradeDay
import DBhandle

app = Flask(__name__, static_folder='statics', template_folder='templates')


# --------------配置信息------------
class ScheduleConfig(object):
    # 列表类型，如有需要可以定义多个job
    JOBS = [
        {
            'id': 'daily_job1',
            'func': '__main__:daily_job1',
            'args': (1, 2),
            'trigger': 'cron',  # 指定任务触发器 cron
            'day_of_week': 'mon-fri',  # 每周1至周5早上6点执行
            'hour': 6,
            'minute': 00
        }
        ,
        {
            'id': 'weekly_job1',
            'func': '__main__:weekly_job1',
            'trigger': 'cron',
            'day_of_week': 'sun',
            'hour': 6,
            'minute': 30
        }
        ,
        {
            'id': 'job1',
            'func': '__main__:job1',
            'trigger': 'interval',  # 指定任务触发器 interval
            'minutes': 5
        }
    ]
    # 是否开启RESTful API
    SCHEDULER_API_ENABLED = True
    # 时区配置，cron任务必备
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'


# --------------页面配置------------
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/show/<stock_id>')
def hello(stock_id):
    return render_template('show.html', stock=stock_id)


# --------------定时任务------------
# 每个交易日执行一次，更新所有个股数据
def daily_job1():
    if isTradeDay():
        DBhandle.stockHandle.updateHistoryData()
    else:
        pass


# 每周检查一次，更新股票列表和行业信息
def weekly_job1():
    if isTradeDay():
        DBhandle.stockHandle.updateHistoryData()
    else:
        pass


if __name__ == '__main__':
    app.config.from_object(ScheduleConfig())      # 为实例化的 flask 引入配置
    scheduler = APScheduler()                  # 实例化 APScheduler
    scheduler.init_app(app)                    # 把任务列表放入 flask
    scheduler.start()                          # 启动任务列表
    # app.debug = True
    app.run()
