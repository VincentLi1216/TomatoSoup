import paramiko
import SSH_KEY

def get(file, pc_path):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=SSH_KEY.hostname, username=SSH_KEY.username, password=SSH_KEY.password, port=SSH_KEY.port)
    sftp_client = ssh.open_sftp()

    #上傳檔案
    sftp_client.get(file, pc_path)

    sftp_client.close()
    ssh.close()

def put(file, server_path):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=SSH_KEY.hostname, username=SSH_KEY.username, password=SSH_KEY.password, port=SSH_KEY.port)
    sftp_client = ssh.open_sftp()

    #上傳檔案
    sftp_client.put(file, server_path)

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

# put("IMG_2918.JPG", "/home/ubuntu/static/IMG_2918.JPG")
# remove("/home/ubuntu/static/保螺.png")

