import select
import paramiko

def get_sql_log(host,port,user,password,cmd):
    # commond='cd crm-app/;./tailall.sh | grep %s'%key_words
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(host,port,user,password)
    transport=s.get_transport()
    channel = transport.open_session()
    channel.get_pty()
    channel.exec_command(cmd)
    # print 'command %s'%commond
   # print '%s' % (str(host))
   #  f=open(out_put_filename,'a+')

   # f.write(str(dir(s)))
    while not channel.exit_status_ready():
        try:
            rl,wl,xl=select.select([channel],[],[],1)
            #print rl
            if len(rl)>0:
                recv=channel.recv(1024)
                print(recv)
                #print recv
                #f.seek(2)
                # f.write(str(recv))
                # f.flush()

        except KeyboardInterrupt:
            # print("Caught control-C")
            channel.send("\x03")#发送 ctrl+c
            channel.close()
            s.close()
            exit(0)

get_sql_log(host='192.168.8.231',port=22,user='root',password='hd8832508',cmd='ping -c4 www.baidu.com')