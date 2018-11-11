from celery_tasks.main import app
from mall import settings
from django.core.mail import send_mail


@app.task(name='send_verify_mail')
def send_verify_mail(recv_email, verify_url):
    subject = '美多商城邮箱确认邮件'
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用美多商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (recv_email, verify_url, verify_url)
    from_email = settings.EMAIL_FROM
    recipient_list = [recv_email]
    send_mail(subject=subject,
              message='',
              from_email=from_email,
              html_message=html_message,
              recipient_list=recipient_list)
