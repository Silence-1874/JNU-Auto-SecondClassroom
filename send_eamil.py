import yagmail


def send(content):
    send_username = 'silence1874@foxmail.com'
    receiver_1 = 'silence1874@foxmail.com'
    authorization = ''

    subject = '第二课堂活动提醒'

    yag = yagmail.SMTP(user=send_username, password=authorization, host='smtp.qq.com')
    yag.send(to=receiver_1, subject=subject, contents=content)
