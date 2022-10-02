import paramiko
import SSH_KEY
import time

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
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=SSH_KEY.hostname, username=SSH_KEY.username, password=SSH_KEY.password, port=SSH_KEY.port)
    sftp_client = ssh.open_sftp()

    ##下載檔案
    sftp_client.get(file, pc_path, callback = trans_status)


    sftp_client.close()
    ssh.close()

def put(file, server_path):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=SSH_KEY.hostname, username=SSH_KEY.username, password=SSH_KEY.password, port=SSH_KEY.port)
    sftp_client = ssh.open_sftp()

    #上傳檔案
    sftp_client.put(file, server_path, callback = trans_status)

    sftp_client.close()
    ssh.close()

def remove(file):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=SSH_KEY.hostname, username=SSH_KEY.username, password=SSH_KEY.password, port=SSH_KEY.port)
    sftp_client = ssh.open_sftp()

    # 刪除檔案
    sftp_client.remove(file)

    sftp_client.close()
    ssh.close()


def mkdir(folder_name):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=SSH_KEY.hostname, username=SSH_KEY.username, password=SSH_KEY.password, port=SSH_KEY.port)
    sftp_client = ssh.open_sftp()

    # 製作資料夾
    ssh.exec_command("mkdir /home/ubuntu/static/" + folder_name)

    sftp_client.close()
    ssh.close()

def server_command(command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=SSH_KEY.hostname, username=SSH_KEY.username, password=SSH_KEY.password, port=SSH_KEY.port)
    sftp_client = ssh.open_sftp()

    # 伺服器執行指令
    ssh.exec_command(command)

    sftp_client.close()
    ssh.close()

if __name__ == "__main__":
    # put("/Users/lishande/Pictures/桌布/pexels-sanaan-mazhar-3075993.jpg", "/home/ubuntu/static/wallpaper.jpg")
    remove("/home/ubuntu/static/final_10-02-2022_23:50:53.jpg")
    # get("/home/ubuntu/static/wallpaper.jpg", "imgs/wallpaper.jpg")

