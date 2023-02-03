from getData.getAkshare import isTradeDay
import DBhandle


# --------------配置信息------------
class ScheduleConfig(object):
    # 列表类型，如有需要可以定义多个job
    JOBS = [
        {
            'id': 'daily_job1',
            'func': 'schedule:daily_job1',
            'trigger': 'cron',  # 指定任务触发器 cron
            'day_of_week': 'mon-fri',  # 每周1至周5早上6点执行
            'hour': 17,
            'minute': 30
        }
        ,
        {
            'id': 'weekly_job1',
            'func': 'schedule:weekly_job1',
            'trigger': 'cron',
            'day_of_week': 'sun',
            'hour': 6,
            'minute': 30
        }
        ,
        {
            'id': 'interval_job1',
            'func': 'schedule:interval_job1',
            'trigger': 'interval',  # 指定任务触发器 interval
            'minutes': 500
        }
    ]
    # 是否开启RESTful API
    SCHEDULER_API_ENABLED = True
    # 时区配置，cron任务必备
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'


# --------------定时任务------------
# 每个交易日执行一次，更新所有个股数据
def daily_job1():
    if isTradeDay():
        DBhandle.stockHandle.updateHistoryData()
    else:
        pass


# --------------定时任务------------
# 每周检查一次，更新股票列表和行业信息
def weekly_job1():
    pass


# --------------间隔任务------------
# 间隔几分钟执行一次，用于盯市
def interval_job1():
    pass