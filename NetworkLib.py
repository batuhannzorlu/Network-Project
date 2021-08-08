import paramiko
import time
import threading

class Switch:
  def __init__( self,IP, EnableSecret='-1',SshHname='admin',SshPsswd='admin'):
    self.IP = IP
    self.EnableSecret = EnableSecret
    self.SshHname = SshHname
    self.SshPsswd = SshPsswd

class Router:
  def __init__(self, IP, EnableSecret='-1',SshHname='admin',SshPsswd='admin'):
    self.IP = IP
    self.EnableSecret = EnableSecret
    self.SshHname = SshHname
    self.SshPsswd = SshPsswd

def ConnectViaSSH(device:Router):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh_client.connect(device.IP,'22',device.SshHname,device.SshPsswd,
                       look_for_keys=False, allow_agent=False)

    print('Connected Successfully!')
    return ssh_client

def ConnectViaTELNET(device:Switch):
    pass


def SendCommand(shell,Command):
    print('sent')
    shell.send(Command+'\n')
    time.sleep(1)
    return shell

def PrintOutput(shell):
    output = shell.recv(10000)
    output = output.decode('utf-8')
    print(output)

def RIPV2SUB24Conf(shell,device:Router,Subnet=24):

   # if (device.EnableSecret != '-1'):
    SendCommand(shell,device.EnableSecret)

    #SendCommand(shell,'show run | include (interface | ip address)')
    SendCommand(shell,'show ip int bri')

    output = shell.recv(10000)
    output = output.decode('utf-8')
    output_list = output.splitlines()

    SendCommand(shell, ' en')
    SendCommand(shell, 'admin')
    SendCommand(shell, 'conf terminal')
    SendCommand(shell, 'router rip')
    SendCommand(shell, 'version 2')
    for line in output_list:
        if( line.__contains__('up')):
              s = str(line)
              IntIp = s.split()
              if IntIp[1] != 'unassigned' :
                  SIntIp = IntIp[1].split('.')
                  IntIp[1] = SIntIp[0]+'.'+SIntIp[1]+'.'+SIntIp[2]+'.'+'0'
                  SendCommand(shell,'network'+' '+IntIp[1])
                  PrintOutput(shell)

    client.close()

#User must create the vlan and give it ip address.
def EtherChannel(interface_list,vlan_num,port_channel_num, mode):
    SendCommand(shell, ' en')
    SendCommand(shell, 'admin')
    SendCommand(shell, 'conf terminal')

    for interface in interface_list:
        SendCommand(shell,f'int {interface}')
        SendCommand(shell,'switchport mode access')
        SendCommand(shell,f'switchport access vlan {vlan_num}')
        SendCommand(shell,f'channel-group {port_channel_num} mode {mode}')

    SendCommand(shell,f'interface port-channel {port_channel_num}')
    SendCommand(shell,'switchport trunk encapsulation dot1q')
    SendCommand(shell,'switchport mode trunk')
    SendCommand(shell,f'switchport trunk allowed vlan {vlan_num}')
    PrintOutput(shell)

def DhcpConf(shell,device,network,SubnetMask,DefaultRouter,poolname):
    SendCommand(shell,'')

def BackUp():
    pass
def MultiThreading(DeviceList,TargetFunction):
    threads =list()
    for device in DeviceList:
        th=threading.Thread(target=TargetFunction,args=(device,))
        threads.append(th)

    for th in threads:
        th.start()

    for th in threads:
        th.join()

router2 = Router('10.1.1.3','admin')
client = ConnectViaSSH(router2)
shell = client.invoke_shell()
#interfaces=['e 1/0','e 1/1']
#EtherChannel(interfaces,12,1,'on')

#ripV2Conf(shell,router2)
#SendCommand(shell,'en')
#SendCommand(shell,'admin')
#SendCommand(shell,'sh run')
#PrintOutput(shell)
