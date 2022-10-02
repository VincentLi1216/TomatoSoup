import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname="114.32.43.46", username="ubuntu", password="pi", port=22)
sftp_client=ssh.open_sftp()
print(dir(sftp_client))

sftp_client.get("/home/ubuntu/static/IMG_5317.JPG", "orig_10-01-2022_09:37:04.jpg")

sftp_client.close()
ssh.close()
