from CTRL_SHIFT import DataBaseManagementInterface
import mysql.connector


class MySQLManagement(DataBaseManagementInterface.DataBaseManagementInterface):

    def __init__(self):
        conn = None

    def connect_to_data_base(self, host, database, user, password):
        self.conn = mysql.connector.connect(host='localhost',
                                            database='ground_attendant',
                                            user='root',
                                            password='7********k')

    def create_data_base_cursor(self, buffered: bool):
        return self.conn.cursor(buffered)

    def data_base_execute_command(self, command: str, cursor):
        cursor.execute(command)

    def data_base_fetchall_data_from_last_execute_command(self, cursor):
        return cursor.fetchall()
