from flask import Flask
from flask_apscheduler import APScheduler


# 实例化 APScheduler
scheduler = APScheduler()

@scheduler.task('interval', id='job_1', args=(1,2), seconds=5)
def job1(a, b):  # 运行的定时任务的函数
    print(str(a) + ' ' + str(b))


if __name__ == '__main__':
    app = Flask(__name__)

    scheduler.start() 

    app.debug=True
    app.run(host='0.0.0.0', port= 8000)  # 启动 flask