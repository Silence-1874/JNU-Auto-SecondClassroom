import requests
import send_eamil

# 发送邮件的内容
message = '''
          # 招募人数:{zmrs},#现已报名了{bmrs},学时:{xs}
          # 活动名:{hdmc},活动时间：{kssj}至{jssj},地点:{hddd}
          # 报名时间:{bmkssj}至{bmjssj}
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

    for active in data['data']['list']:
        if active['zmrs'] > active['bmrs']:
            message.format()

if __name__ == '__main__':
    check()