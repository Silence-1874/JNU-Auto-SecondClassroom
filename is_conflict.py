import datetime


# 检测活动开始时间是否与本人上课时间冲突
def is_conflict(d, h, m):
    if d == '周日' or d == '周六':
        return False
    elif d == '周五' or d == '周四' or d == '周三':
        if h < '15':
            return True
        elif h == '15' and m < '10':
            return True
        else:
            return False
    elif d == '周二' or d == '周一':
        if h < '17':
            return True
        elif h == '17' and m < '05':
            return True
        else:
            return False
    # 正常情况下到不了这句，安全起见，返回True
    return True