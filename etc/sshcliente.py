import paramiko

if __name__ == "__main__":
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect('0.0.0.0', username='', password='')

    stdin, stdout, stderr = ssh.exec_command('ls -al\n')

    print stdout.readlines()

    ssh.close()



