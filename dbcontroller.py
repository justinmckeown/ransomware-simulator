import logging
import traceback
import pymysql
import typing
import time_utility 
from config import *
from sshtunnel import SSHTunnelForwarder
from datamodels

logger = logging.getLogger()

class SshConnectionManager:
    def __init__(self):
        self.ssh_connection = self.get_ssh_tunnel()
        self.open_tunnel()
    
    def open_tunnel(self):
        logger.debug(f'Opening ssh tunnel to: {server_ip}')
        self.ssh_connection.start()
        logger.debug(f'remote local_bind_port: {self.ssh_connection.local_bind_port}')
    
    def close_tunnel(self):
        logger.debug(f'Closing ssh tunnel to: {server_ip}')
        self.ssh_connection.stop()
    
    def get_ssh_tunnel(self) -> SSHTunnelForwarder:
        try:
            return SSHTunnelForwarder(server_ip, ssh_username=ssh_user, ssh_pkey=ssh_key_path, remote_bind_address=(bind_address, remote_port))
        except Exception as e:
            logger.error(e)


class DBManager:
    def __init__(self, remote_mode: bool,tunnel: typing.Union[SSHTunnelForwarder, None] = None ) -> None:
        self.remote_mode = remote_mode
        self.server = tunnel
        self.CONNECTION = self._get_db_connection()
        self.CURSOR = self.CONNECTION.cursor()
    
    def get_clients(self):
        sql = "select * from client;"
        clients = []
        try:
            self.CURSOR.execute(sql)
        except Exception as e:
            logger.error(f'DBManager: {str(e)}')
        else:
            row = self.CURSOR.fetchone()
            while row is not None:
                clients.append(row)
                row = self.CURSOR.fetchone()
        finally:
            return [Client(x) for x in clients]
    

    def get_email_list(self, client_id:int = 0):
        if client_id < 1:
            sql = "SELECT * FROM email WHERE active ='true';"
        else:
            sql = f"SELECT * FROM email WHERE active ='true' and client_id = {client_id};"

        emails = []
        try:
            self.CURSOR.execute(sql)
        except Exception as e:
            logger.error(f'DBManager: {str(e)}')
        else:
            row = self.CURSOR.fetchone()
            while row is not None:
                emails.append(row)
                row = self.CURSOR.fetchone()
        finally:
            #self.CONNECTION.close()
            return [EmailAddress(x) for x in emails]
    
    def get_breach(self, breach_name: str) -> typing.Union[Breach, None]:
        sql = f"SELECT * from breach WHERE name = '{breach_name}';"
        try:
            self.CURSOR.execute(sql)
        except Exception as e:
            logger.error(f'DBManager.get_breach(): {e.args}')
        else:
            row = self.CURSOR.fetchone()
        finally:
            return Breach(row) if row is not None else None
    

    def get_breach_description(self, breach_name) -> str:
        sql = f"SELECT description from breach_description WHERE breach_name = '{breach_name}';"
        try:
            self.CURSOR.execute(sql)
        except Exception as e:
            logger.error(f'DBManager.get_breach_description(): {e.args}')
        else:
            row = self.CURSOR.fetchone()
            logger.debug(f'DbManager.get_breach_description() ROW CONTENT: {row}')
        finally:
            return row[0] 



    def insert_breach_email_record(self, e_id: int, b_name: str, e_adrs: str, e_client_name: str, rprt:str = 'false'):
        logger.debug(f'DB.manager.insert_breach_email_records called')
        success = False
        sql = "INSERT INTO breachemail (id_email, breach_name, email_address, client_name, reported, date_reported) VALUES (%s, %s, %s, %s, %s, %s);"
        try:
            d_rprt = time_utility.sqltimestamp()
            self.CURSOR.execute(sql, (e_id, b_name, e_adrs, e_client_name, rprt, d_rprt))
        except Exception as e:
            print(traceback.format_exc())
            logger.error(f'DBManager.update_breach_email_records() : {e.args}')
        else:
            self.CONNECTION.commit()
            logger.info('breach_email record successfully inserted into database')
        finally:
            print(f'SUCCESS: {str(success)}')
            return success
    

    def insert_breach(self, breach: Breach):
        #print(f' VALUES PASSED IN: {vars(breach)}')
        logger.debug(f'DB.manager.insert_breach called. Inserting {breach.name} breach')
        last_row_id = 0
        sql = 'INSERT INTO breach (name, title, domain, breach_date, date_added, modified_date, pwn_count, is_verified, is_fabricated, is_sensitive, is_retired, is_spam_list, is_malware, logo_path) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'        
        try:
            self.CURSOR.execute(sql, (breach.name, breach.title, breach.domain, breach.breach_date, breach.added_date, breach.modified_date, breach.pwn_count, breach.is_verified, breach.is_fabricated, breach.is_sensitive, breach.is_retired, breach.is_spam_list, breach.is_malware, breach.logo_path))
            last_row_id = self.CURSOR.lastrowid
        except Exception as e:
            #print(traceback.format_exc())
            logger.error(f'DBManager.insert_breach() : {e.args}')
        else:
            self.CONNECTION.commit()
            logger.debug('breach data successfully inserted into database')
        finally:
            return last_row_id
    

    def insert_breach_description(self, breach_id:int, name:str, description:str):
        logger.debug('DB.manager.insert_breach_description called')
        sql = 'INSERT INTO `breach_description` (`breachid`, `breach_name`, `description`) VALUES (%s, %s, %s);' 
        try:
            self.CURSOR.execute(sql, (breach_id, name, description))
        except Exception as e:
            logger.error(f'DBManager.insert_breach_description() : {e.args}')
        else:
            logger.debug('breach data successfully inserted into database')
            self.CONNECTION.commit()
    
    
    def insert_breach_dataclass(self, breachid: int, name: str, dataclass: str):
        sql = 'INSERT INTO `discoverytools`.`breach_dataclasses` (`breachid`, `breach_name`, `dataclass`) VALUES (%s, %s, %s);'
        try:
            self.CURSOR.execute(sql, (breachid, name, dataclass))
        except Exception as e:
            logger.error(f'DBManager.insert_breach_dataclass : {e.args}')
        else:
            logger.debug(f'{name} breach dataclass successfully inserted into database')
            self.CONNECTION.commit()

    

    # NOTE: Connection establishment methods from here down ....
    def _get_db_connection(self):
        if self.server:
            logger.info('setting up remote Database Connection via ssh tunnel')
            return self._get_ssh_tunnelled_connection()
        else:
            logger.info('setting up local Database Connection')
            return self._get_connection()
    

    #use this when the script is running on the remote server
    def _get_connection(self):
        try:
            return pymysql.connect(host=local_host, user=local_user, password=local_password, db=local_db)
        except Exception as e:
            logger.error(e)
    
    #use this when you're trying to test the script remotely via ssh
    def _get_ssh_tunnelled_connection(self):
        try:
            return pymysql.connect(host=local_host, port=self.server.local_bind_port, user=local_user, password=local_password, db=local_db)
        except Exception as e:
            logger.error(e)
        return None



