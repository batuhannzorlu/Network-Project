import paramiko
import time
# creating an ssh client object
ssh_client = paramiko.SSHClient()
# print(type(ssh_client))

ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print('Connecting to 10.1.1.10')

router1 = {'hostname':'10.1.1.3' , 'port' : '22','username': 'admin','password':'admin'}
ssh_client.connect(**router1,
                   look_for_keys=False, allow_agent=False)
shell = ssh_client.invoke_shell()
shell.send('en\n')
time.sleep(1)
shell.send('show run \n')
time.sleep(1)
output = shell.recv(10000)
output = output.decode('utf-8')
print(output)

# checking if the connection is active
print(ssh_client.get_transport().is_active())

# sending commands
# ...

print('Closing connection')
ssh_client.close()