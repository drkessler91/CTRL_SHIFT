

class DataBaseManagementInterface:
    def connect_to_data_base(self, host, database, user, password):
        pass

    def create_data_base_cursor(self, buffered: bool):
        pass

    def data_base_execute_command(self, command: str, cursor):
        pass

    def data_base_fetchall_data_from_last_execute_command(self, cursor):
        pass