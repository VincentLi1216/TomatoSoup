import paramiko
import SSH_KEY
import time
from util_warning import *



def trans_status(now, total):
    start_time = time.time()
    file_size = total/1000000
    progress = now/total
    bar_width = 50
    bar = "["

    for i in range(int(now*bar_width / total)):
        bar += "█"

    for j in range(bar_width-int(now*bar_width / total)):
            bar += " "

    bar += "]" + str(int(progress*100)) + "%"

    print(bar)

    if now == total:
        duration = time.time() - start_time
        print("Total Size:", round(file_size,2), "MB in", round(duration*100000, 2), "secs")



def get(file, pc_path):

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=SSH_KEY.hostname, username=SSH_KEY.username, password=SSH_KEY.password, port=SSH_KEY.port)
        sftp_client = ssh.open_sftp()

        ##下載檔案
        sftp_client.get(file, pc_path, callback=trans_status)

        sftp_client.close()
        ssh.close()
    except:
        warning("Can NOT get the file from the server!")


def put(file, server_path):


    try:
        # 嘗試新增新資料夾
        t = time.localtime()
        date = str(time.strftime("%m-%d-%Y", t))
        mkdir(date)

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=SSH_KEY.hostname, username=SSH_KEY.username, password=SSH_KEY.password, port=SSH_KEY.port)
        sftp_client = ssh.open_sftp()

        # 上傳檔案
        sftp_client.put(file, server_path, callback=trans_status)

        sftp_client.close()
        ssh.close()
    except:
        warning("Can NOT put the file to the server!")


def remove(file):

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=SSH_KEY.hostname, username=SSH_KEY.username, password=SSH_KEY.password, port=SSH_KEY.port)
        sftp_client = ssh.open_sftp()

        # 刪除檔案
        sftp_client.remove(file)

        sftp_client.close()
        ssh.close()
    except:
        warning("Can NOT remove the file from the server!")


def mkdir(folder_name):

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=SSH_KEY.hostname, username=SSH_KEY.username, password=SSH_KEY.password, port=SSH_KEY.port)
        sftp_client = ssh.open_sftp()

        # 製作資料夾
        ssh.exec_command("mkdir /home/ubuntu/static/" + folder_name)

        sftp_client.close()
        ssh.close()
    except:
        warning("Can NOT mkdir from the server!")

def server_command(command):


    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=SSH_KEY.hostname, username=SSH_KEY.username, password=SSH_KEY.password, port=SSH_KEY.port)
        sftp_client = ssh.open_sftp()

        # 伺服器執行指令
        ssh.exec_command(command)

        sftp_client.close()
        ssh.close()
    except:
        warning("Can NOT execute the command from the server!")

if __name__ == "__main__":
    # put("imgs/10-04-2022/final_10-04-2022_15:59:34.jpg", "/home/ubuntu/static/10-04-2022/final_10-04-2022_15:59:34.jpg")
    # remove("/home/ubuntu/static/final_10-02-2022_23:50:53.jpg")
    # get("/home/ubuntu/static/wallpaper.jpg", "imgs/wallpaper.jpg")
    server_command("rm -r /home/ubuntu/static/10-04-2022")

