import time

def allen_return_time():
    sec = time.time()
    t = time.localtime(sec)  # 轉成 UTC+8 時區，取得 struct_time 格式的時間

    # 依指定格式輸出
    c_time = time.strftime("%m-%d-%Y_%H-%M-%S", t)
    return c_time