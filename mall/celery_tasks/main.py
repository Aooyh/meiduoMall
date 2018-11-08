from celery import Celery
import os

# 为celery使用django文件进行配置
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mall.settings'

# 创建celery对象
# main参数设置脚本名, 一般为celery文件夹名
app = Celery('celery_tasks')

# 配置文件加载celery配置
app.config_from_object('celery_tasks.config')

# 自动检测任务
app.autodiscover_tasks(['celery_tasks.sms'])
