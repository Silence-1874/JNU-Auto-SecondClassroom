import requests
import time
import datetime
import send_eamil
import is_conflict

# 发送邮件的内容
message = '''
          [{hdmc}]活动招募中!
          招募人数:{zmrs},现已报名了{bmrs}人
          活动地点:{hddd}
          活动时长:{hdsc},学时:{xs}
          活动时间:({weekday}){kssj}至{jssj}
          报名时间:{bmkssj}至{bmjssj}
          '''

# 请求头
Headers = {
    'Authorization': '',
    'Cookie': '',
    'Referer': 'http://dekt.jiangnan.edu.cn/admin/index.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'
}

# 请求参数
Qurey_String_Parameters = {
    'hdmc': '',  # 原请求就是空的，保持为空
    'orgId': '',  # 原请求就是空的，保持为空
    'size': '10',  # 每页显示的条目数，保持10即可
    'page': '1',  # 页码，一般也不会一下多十几个活动吧……
    'userId': '',  # 自己的学号
    'xyId': '12200',  # 不知道是啥，不过好像保持不变就行了
    'grade': '2020',  # 填自己的年级就行
    'type': '2'  # 活动类型，2表示“招募中”(经过试验， 参数对应如下：1-预热中 2-招募中 3-进行中 4-已结束 5-全部活动)
}


# 核心代码
def check():
    session = requests.session()
    # 请求活动列表
    response = session.request(method='get',
                               url='http://dekt.jiangnan.edu.cn/biz/activity/student/list',
                               params=Qurey_String_Parameters,
                               headers=Headers)
    # 解析列表
    response.encoding = response.apparent_encoding
    # 转换成json格式
    data = response.json()
    # 判断是否找到可报名的活动，便于之后决定是否发送邮件
    flag = False
    # 邮件内容
    content = ''
    for active in data['data']['list']:
        if active['zmrs'] > active['bmrs'] and active['hdmc'].find('团日活动') == -1:  # 有些班级的团日活动长期占榜，排除之
            flag = True
            wd = get_weekday(active['kssj'])
            # 活动时间跟本人无冲突
            if not is_conflict.is_conflict(wd, active['kssj'][-5:-3], active['kssj'][-2:]):
                # 自动报名
                response = session.post('http://dekt.jiangnan.edu.cn/biz/activity/signup', json={'id': active['id']}, headers=Headers)
                print(response.text)
                if response.text.find('成功') != -1:
                    send_eamil.send('(报名成功)' + active['hdmc'])

            content += message.format(hdmc=active['hdmc'],
                                      zmrs=active['zmrs'],
                                      bmrs=active['bmrs'],
                                      hddd=active['hddd'],
                                      hdsc=count_time(active['kssj'], active['jssj']),
                                      xs=active['xs'],
                                      weekday=wd,
                                      kssj=active['kssj'],
                                      jssj=active['jssj'],
                                      bmkssj=active['bmkssj'],
                                      bmjssj=active['bmjssj']
                                      )
    if flag:
        print(content)
        # 发送提醒邮件
        send_eamil.send(content)
    else:
        print('本次查询无结果')


# 计算活动时长(应该不会有跨日的活动吧……)
def count_time(start_time, end_time):
    hour = int(end_time[-5:-3]) - int(start_time[-5:-3])
    minute = int(end_time[-2:]) - int(start_time[-2:])
    if minute < 0:
        minute += 60
        # 本来想写 hour-- 结果居然报错了，才知道Python没有自增/自减运算符……
        hour -= 1
    return '{hour}小时{minute}分钟'.format(hour=hour, minute=minute)


# 计算活动开始日是星期几，便于检查时间是否冲突
def get_weekday(dt):
    map = {'Mon': '周一', 'Tue': '周二', 'Wed': '周三', 'Thu': '周四', 'Fri': '周五', 'Sat': '周六', 'Sun': '周日'}
    dt = dt[0:10]
    year, month, day = (int(x) for x in dt.split('-'))
    return map[datetime.date(year, month, day).strftime("%a")]


if __name__ == '__main__':
    while True:
        print('开始查询(' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + ')')
        check()
        # 每隔1分钟检查一次
        time.sleep(1 * 60)
