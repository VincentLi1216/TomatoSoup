import paramiko
import SSH_KEY



ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=SSH_KEY.hostname, username=SSH_KEY.username, password=SSH_KEY.password, port=SSH_KEY.port)
sftp_client=ssh.open_sftp()
print(dir(sftp_client))


#取得檔案
# sftp_client.get("/home/ubuntu/static/IMG_5317.JPG", "orig_10-01-2022_09:37:04.jpg")

#上傳檔案
# sftp_client.put("/Users/lishande/Desktop/123.png", "/home/ubuntu/static/123.png")

#刪除檔案
sftp_client.remove("/home/ubuntu/static/123.png")

sftp_client.close()
ssh.close()
