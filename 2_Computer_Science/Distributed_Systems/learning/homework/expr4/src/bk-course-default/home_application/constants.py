
import os

# JOB执行作业的业务ID
JOB_BK_BIZ_ID = 3

# 作业执行结果查询的最大轮询次数
MAX_ATTEMPTS = 10

# 调用作业执行结果api的轮询间隔
JOB_RESULT_ATTEMPTS_INTERVAL = 0.2

# JOB作业平台HOST
BK_JOB_HOST = os.getenv("BKPAAS_JOB_URL")

# JOB 平台的状态码
WAITING_CODE = 2
SUCCESS_CODE = 3

# 默认HTTP状态码
WEB_SUCCESS_CODE = 0

# 作业方案ID
SEARCH_FILE_PLAN_ID = 1000451   # 将这里的方案ID更改为你自己在JOB平台上新建的方案ID
BACKUP_FILE_PLAN_ID = 1000452
