import math

class Tools:

    @staticmethod
    def convert_str_time_to_float_time(str_time: str):
        hour_str = str_time.split(":")[0]
        minutes_str = str_time.split(":")[1]
        time_float = float(hour_str) + float(minutes_str) / 60
        # print(time_float)
        return time_float

    @staticmethod
    def convert_str_time_to_float_time_again(str_time: str):
        hour_str = str_time.split(".")[0]
        minutes_str = str_time.split(".")[1]
        if minutes_str[0] == "0":
            check = math.ceil(float(minutes_str) *0.6)
            if minutes_str.__len__() > 1:
                minutes_str1 = str(check)[:2]
                minutes_str2 = float(minutes_str1)/1000
                time_float = float(hour_str) + float(minutes_str2)
            else:
                minutes_str1 = str(check)[:2]
                minutes_str2 = float(minutes_str1)/10
                time_float = float(hour_str) + float(minutes_str2)
        else:
            check = float(minutes_str) *0.6
            if minutes_str.__len__() > 1:
                minutes_str1 = str(check)[:2]
                minutes_str2 = float(minutes_str1)/100
                time_float = float(hour_str) + float(minutes_str2)
            else:
                minutes_str1 = str(check)[:2]
                minutes_str2 = float(minutes_str1)/10
                time_float = float(hour_str) + float(minutes_str2)
        # print(time_float)
        return time_float