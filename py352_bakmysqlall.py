import pymysql
import time
import os
import logging
import string
import configparser
from threading import Thread
from paramiko import SSHClient, AutoAddPolicy
from pymysql.cursors import DictCursor

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s [%(threadName)s] %(message)s')

_sql_baklist = "select concat(mr.host,'|',mr.port,'|',ma.username,'|',ma.password,'|',concat(install_dir,'/mysql57/mysql',mr.port,'.cnf'),'|','root','|',AES_DECRYPT(unhex(default_os_passwd),'Tf$%hj'),'|',mp.sets_name )  from mysql_replication  mr , mysql_pools mp ,db_servers_mysql ma where mr.tags=mp.sets_name and concat(ma.host,'|',ma.port)=concat(mr.host,'|',mr.port) and mr.is_master!=1 and concat(mr.host,'|',mr.port) not in (select concat(localhost,'|',dbport) from mysql_backup_conf);"
_inser_sql = 'insert into mysql_backup_conf(user, password, localhost, dbport, dbcfg, sets_name) values("{user}", "{password}", "{host}", "{port}", "{cnf}", "{set_name}")'
_exec_bak_list = "select concat(my.user,'|',my.password,'|',my.localhost,'|',my.dbport,'|',my.dbcfg,'|',my.bakpath,my.dbport,'|',my.rsync,'|',my.keeplocalbak,'|','root','|',AES_DECRYPT(unhex(default_os_passwd),'Tf$%hj')) from mysql_backup_conf my,mysql_pools mp where  my.sets_name=mp.sets_name;"
_bak_shpath = "/soft/backup_cycle.sh"


def _run_cmd(user, host, password, commands, copy_file=False, backpath=None):
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    try:
        client.connect(username=user, hostname=host, password=password)
        for index, cmd in enumerate(commands):
            logging.info('run cmd => {}'.format(cmd))
            if copy_file and index == 1:
                _copy_file(client, _bak_shpath, backpath)
            _, stdout_, _ = client.exec_command(cmd)
            logging.info('run finished => {}'.format(stdout_.read()))
    except Exception as e:
        logging.error('Handle Exception {}'.format(str(e)))
    finally:
        client.close()


def _copy_file(client, file, rm_path):
    sftp = client.open_sftp()
    sftp.put(file, os.path.join(rm_path, os.path.join(rm_path, file.split('/')[-1])))


class BackupClient(object):
    def __init__(self, *args, **kwargs):
        self._conn = pymysql.connect(*args, **kwargs)

    def _execute(self, sql):
        with self._conn as cur:
            cur.execute(sql)
            return cur.fetchall()

    def _add_backup_list(self):
        result = self._execute(_sql_baklist)
        for item in result:
            ip, port, user, passwd, cnf, osuser, ospwd, set_names = \
                [val for val in item.values()][0].split('|')
            self._execute(
                _inser_sql.format(user=user, password=passwd, port=port, host=ip, cnf=cnf, set_name=set_names))

    def _run_backup(self, user, host, password, commands, copy_file=False, backpath=None, dbport=None):
        Thread(target=_run_cmd, args=(user, host, password, commands, copy_file, backpath),
               name='{}@{}:{} backup threading'.format(user, host, dbport)).start()

    def _backup_all_db(self):
        result = self._execute(_exec_bak_list)
        for item in result:
            user, pwd, host, port, cfg, back_path, rsync, keep_local, osuser, ospwd = \
                [val for val in item.values()][0].split('|')
            cmds = []
            cmds.append('mkdir -p {} > /dev/null 2>&1'.format(back_path))
            cmds.append(
                'sh {backpath}/backup_cycle.sh {cfg} {user} {password} {backpath} {keep_local} {rsync} {host}'.format(
                    backpath=back_path, cfg=cfg, user=user, password=pwd, keep_local=keep_local, rsync=rsync, host=host
                ))
            self._run_backup(osuser, host, ospwd, cmds, True, back_path, port)
            time.sleep(1)

    def run_backup(self):
        self._add_backup_list()
        self._backup_all_db()

if __name__ == '__main__':
    def get_config(group,config_name):
        config = configparser.ConfigParser()
        config.readfp(open('/usr/local/lepus/etc/config.ini','r'))
        config_value=config.get(group,config_name).strip(' ').strip('\'').strip('\"')
        return config_value
    monitor_host = get_config('monitor_server','host')
    monitor_port = get_config('monitor_server','port')
    monitor_user = get_config('monitor_server','user')
    monitor_passwd = get_config('monitor_server','passwd')
    monitor_dbname = get_config('monitor_server','dbname')

    BackupClient(host=monitor_host, port=int(monitor_port), user=monitor_user, password=monitor_passwd,
                 database=monitor_dbname, cursorclass=DictCursor).run_backup()
