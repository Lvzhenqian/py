import pymysql,paramiko
from contextlib import contextmanager
import threading


class Mysql:
    def __init__(self, **kwargs):
        self.config = kwargs

    def SQL(self, sql):
        @contextmanager
        def mysql():
            conn = pymysql.connect(**self.config)
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            try:
                yield cursor
            finally:
                conn.commit()
                cursor.close()
                conn.close()

        with mysql() as cursor:
            stat = cursor.execute(sql)
            return {'stat': stat, 'data': cursor.fetchall()}

class Cond:
    def __init__(self):
        self._data = None
        self.event = threading.Event()
        self.cond = threading.Condition()
    def producer(self,mysql:Mysql()):
        sql = "select concat(my.user,'|',my.password,'|',my.localhost,'|',my.dbport,'|',my.dbcfg,'|',my.bakpath,my.dbport,'|',my.rsync,'|',my.keeplocalbak,'|','root','|',AES_DECRYPT(unhex(default_os_passwd),'Tf$%hj')) from mysql_backup_conf my,mysql_pools mp where  my.app_name=mp.sets_name;"
        lst = mysql.SQL(sql)
        with self.cond:
            self.cond.notifyAll()

    def consumer(self,ssh):
        while not self.event.is_set():
            with self.cond:
                self.cond.wait()
                ssh.Cmd('sh $mybakpath2/backup_cycle.sh $mycfg2 $myuser2 $mypwd2 $mybakpath2 $mykeeplocal2 $myrsync2 ${myhost2}')

def Add_mysql_baklist(barrier:threading.Barrier,mysql:Mysql()):
    try:
        sql = "select concat(my.user,'|',my.password,'|',my.localhost,'|',my.dbport,'|',my.dbcfg,'|',my.bakpath,my.dbport,'|',my.rsync,'|',my.keeplocalbak,'|','root','|',AES_DECRYPT(unhex(default_os_passwd),'Tf$%hj')) from mysql_backup_conf my,mysql_pools mp where  my.app_name=mp.sets_name"
        worker_id = barrier.wait()
        lst = mysql.SQL(sql)
        ## {'data': [{'id': 1, 'name': 'aming'},{'id': 12, 'name': 'aaa'},{'id': 3, 'name': 'lv'}],'stat': 3}
        ###work
        sql2 = "insert into mysql_backup_conf(user,password,localhost,dbport,dbcfg,app_name) values('{}','{}','{}','{}','{}','{}')".format('$user1','$passwd1','$host1','$port1','$cnf1','$set_names1')
    except threading.BrokenBarrierError:
        return

class SSH:
    def __init__(self,host,port,user,passwd):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.con = ssh.connect(host,port,user,passwd)
    def Cmd(self,cmd):
        stdin,stdout,stderr = self.con.exec_command(cmd)
        return stdout.readlines()

if __name__ == '__main__':

    config = {
        'host': '192.168.19.20',
        'port': 3306,
        'user': 'root',
        'password': 'hd8832508',
        'db': 'hd',
        'charset': 'utf8'
    }
    mysql = Mysql(**config)
    Thread_n = 20
    barrier = threading.Barrier(Thread_n)
    for x in range(Thread_n):
        threading.Thread(target=Add_mysql_baklist, name='worker-{}'.format(x), args=(barrier,)).start()
    c = Cond()
    p = threading.Thread(target=c.producer,args=(mysql,),name='producer')
    hostlist = []
    hostlist.append(SSH('127.0.0.1',22,'root','1234'))
    for i in hostlist:
        threading.Thread(target=c.consumer,args=(i,),name='consumer')