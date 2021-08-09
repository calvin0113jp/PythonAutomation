# For ssh auto login
# pip install pexpect

from pexpect import popen_spawn
import pexpect
import time
import sys


host = '10.90.90.90'
user = 'user'
password = 'user'
count = 10


def main_process():
    for count1 in range(1,count):
        try:
            cmd_ssh_login = "plink -batch -ssh %s -l %s -pw %s" %(host,user,password)
            login_process = popen_spawn.PopenSpawn(cmd_ssh_login,logfile=sys.stdout.buffer)
            login_process.expect("#",timeout=10)
            time.sleep(1.5)
            login_process.sendline('logout')
            time.sleep(1.5)
            login_process.expect(pexpect.EOF)
            print ('Running for %s times = Passed' %(count1))
        except:
            print ('Running for %s = Failed , unable to login or other issue' %(count1))


if __name__ == '__main__':
    main_process()


