import time

def allen_return_time():
    # 取得 struct_time 格式的時間
    t = time.localtime()

    # 依指定格式輸出
    c_time = time.strftime("%m/%d/%Y, %H:%M:%S", t)
    return c_time