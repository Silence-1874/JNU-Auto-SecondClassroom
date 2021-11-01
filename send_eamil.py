import yagmail

send_username = 'silence1874@foxmail.com'
receiver_1 = 'silence1874@foxmail.com'
authorization = '(邮箱授权码)'

subject = '第二课堂活动提醒'
content = '测试内容'

yag = yagmail.SMTP(user=send_username, password=authorization, host='smtp.qq.com')
yag.send(to=receiver_1, subject=subject, contents=content)
