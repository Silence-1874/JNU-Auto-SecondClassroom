import requests
import send_eamil
import time

# 发送邮件的内容
message = '''
          "{hdmc}"活动招募中!
          招募人数:{zmrs},现已报名了{bmrs}人
          活动地点:{hddd}
          活动时长:{hdsc}
          活动时间:{kssj}至{jssj}
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
    flag = False
    for active in data['data']['list']:
        if active['zmrs'] > active['bmrs'] and active['hdmc'].find('团日活动') == -1:  # 有些班级的团日活动长期占榜，排除之
            content = message.format(zmrs=active['zmrs'],
                                     bmrs=active['bmrs'],
                                     xs=active['xs'],
                                     hdsc=count_time(active['kssj'], active['jssj']),
                                     hdmc=active['hdmc'],
                                     kssj=active['kssj'],
                                     jssj=active['jssj'],
                                     hddd=active['hddd'],
                                     bmkssj=active['bmkssj'],
                                     bmjssj=active['bmjssj']
                                     )
            print(content)
            flag = True
            send_eamil.send(content)
    if not flag:
        print('本次查询无结果')


# 计算活动时长(应该的不会有跨日的活动吧……)
def count_time(start_time, end_time):
    hour = int(end_time[-5:-3]) - int(start_time[-5:-3])
    minute = int(end_time[-2:]) - int(start_time[-2:])
    if minute < 0:
        minute += 60
        # 本来想写 hour-- 结果居然报错了，才知道Python没有自增/自减运算符……
        hour -= 1
    return '{hour}小时{minute}分钟'.format(hour=hour, minute=minute)


if __name__ == '__main__':
    while True:
        print('开始查询(' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + ')')
        check()
        # 每隔3分钟检查一次
        time.sleep(3 * 60)
