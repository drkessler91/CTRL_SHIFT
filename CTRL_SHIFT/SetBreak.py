#from ShiftWorker import T1
#from ShiftWorker import s
from CTRL_SHIFT.HelperSetBreak import HelperSetBreak


class SetBreak(HelperSetBreak):
    id: str = ""
    start_break_time: float = 0
    end_break_time: float = 0
    work_times: list = []
    break_time: float = 0
    employees_shift = [{}]

    def __init__(self, id: str, start_break_time: str, end_break_time: str, work_times: list, break_time: int, s, tool):
        if work_times is not None:
            self.id = id
            self.start_break_time = self.check_if_start_break_time_is_start_shift(start_break_time, s)
            self.end_break_time = self.check_if_end_break_time_is_end_shift(end_break_time, s)
            self.break_time = break_time / 60
            self.work_times = []
            for i, work_time in enumerate(work_times):
                if i % 2 == 0:
                    self.work_times.append({})
                    self.work_times[int(i / 2)]["start"] = tool.convert_str_time_to_float_time(work_times[i])
                else:
                    self.work_times[int(i / 2)]["end"] = tool.convert_str_time_to_float_time(work_times[i])
        else:
            self.id = id
            self.start_break_time = tool.convert_str_time_to_float_time(start_break_time)
            self.end_break_time = tool.convert_str_time_to_float_time(end_break_time)

    @staticmethod
    def check_if_start_break_time_is_start_shift(start_break_time: str,s):
        for employee in s.queue_employees:
            if employee.__getitem__(3) == start_break_time:
                hour_str = start_break_time.split(":")[0]
                minutes_str = start_break_time.split(":")[1]
                time_float = float(hour_str) + (float(minutes_str)+45) / 60
                break
        return time_float

    @staticmethod
    def check_if_end_break_time_is_end_shift(end_break_time: str, s):
        for employee in s.queue_employees:
            if employee.__getitem__(4) == end_break_time:
                hour_str = end_break_time.split(":")[0]
                minutes_str = end_break_time.split(":")[1]
                time_float = float(hour_str) + (float(minutes_str)-45) / 60
                break
        return time_float

    def is_break_time_possible(self):
        possible_break_times = self.convert_work_times_to_break_times(self.start_break_time, self.end_break_time,
                                                                      self.work_times)
        for possible_break_time in possible_break_times:
            if self.check_if_possible(possible_break_time, self.break_time):
                return possible_break_time["start"]
        return None

    @staticmethod
    def check_if_possible(possible_break_time: dict, break_time: float):

        if((possible_break_time["end"] -possible_break_time["start"]) >= break_time):
            return possible_break_time["start"] + break_time <= possible_break_time["end"]

    @staticmethod
    def convert_work_times_to_break_times(start_break_time: float, end_break_time: float, work_times: list):
        break_times = [{}]
        break_times[0]["start"] = start_break_time
        # print(work_times)

        for i, work_time in enumerate(work_times):
            # print(work_time)
            if len(work_times[i]) != 0:
                break_times[i]["end"] = work_times[i]["start"]
                break_times.append({})
                break_times[i + 1]["start"] = work_times[i]["end"]
            else:
                break
        break_times[len(break_times) - 1]["end"] = end_break_time
        # print(break_times)
        return break_times

    @staticmethod
    def where_to_insert_the_break(work_times, break_time_total: dict):
        counter = 0
        work_times_include_break_time = {}
        for i, work_time in enumerate(work_times):
            if counter == 0:
                if work_times[i]["start"] < break_time_total["start_break"]:
                    continue
                else:
                    work_times_include_break_time = break_time_total
                    break
        j = 1
        for j, work_time in enumerate(work_times):
            work_times_include_break_time.__setitem__(j, work_time)
            #work_times_include_break_time.__setitem__(j+1, dest_name)
        return work_times_include_break_time

    def add_work_time_as_break_time(self, start_break_time, end_break_time):
        for i in range(len(self.work_times)-1):
            if self.work_times[i]["end"] < start_break_time and self.work_times[i+1]["start"] > end_break_time:
                self.work_times.insert(i,{"start": start_break_time, "end": end_break_time})

    def insert_refreshment(self, work_time_include_break_time, break_time,tool):
        work_time_include_break_times = work_time_include_break_time
        for i, work in enumerate(work_time_include_break_times):
            if type(work) is str:
                continue
            else:
                if i+1 >= len(work_time_include_break_time):
                    work_time_include_break_times.__setitem__("start_refreshment", work_time_include_break_time[work]["end"])
                    work_time_include_break_times.__setitem__("end_refreshment", work_time_include_break_time[work]["end"] + break_time)
                    break
        return work_time_include_break_times


def check_if_employee_exist_on_flights(employee_shift, emp_num):
    for employee in employee_shift:
        if employee.keys().__contains__(emp_num):
            return False
    return True


def shift_include_break(flight_works_on,iter_on_teams_keys, iter_on_flights, ss, i, j, one_emp, s, tool):
    temp = int(iter_on_teams_keys)
    temp += 1
    iter_on_teams_keys = str(temp)
    start_end_work_time = []
    name_of_dest = {}
    destination_name = []
    while len(flight_works_on) > iter_on_flights:
        put_flight = str(iter_on_flights)
        name_of_dest.__setitem__(put_flight, flight_works_on[iter_on_flights][4])
        destination_name.append(flight_works_on[iter_on_flights][4])
        #name_of_dest.append(flight_works_on[iter_on_flights][4])
        start_end_work_time.append(flight_works_on[iter_on_flights][2])
        start_end_work_time.append(flight_works_on[iter_on_flights][1])
        iter_on_flights += 1
    #destination_name.append(name_of_dest)
    value_for_break = ss.employee_and_his_break.get(i)
    sb = None
    second_sb = None
    start_break_time = None
    end_break_time = None
    work_times_include_break_time = None
    if value_for_break < 1:
       sb = SetBreak(id=i, start_break_time=one_emp[3], end_break_time=one_emp[4],
                      work_times=start_end_work_time, break_time=value_for_break, s=s, tool=tool)
       start_break_time = (sb.is_break_time_possible())
       end_break_time = start_break_time + (value_for_break / 0.6)
       break_time_total = {}
       break_time_total.setdefault("start_break", start_break_time)
       break_time_total.__setitem__("end_break", end_break_time)
       change = break_time_total["start_break"]
       if type(change) is float:
           temp = str(change)
           break_time_total["start_break"] = tool.convert_str_time_to_float_time_again(temp)
       change = break_time_total["end_break"]
       temp = str(change)
       break_time_total["end_break"] = tool.convert_str_time_to_float_time_again(temp)
       for k, work in enumerate(sb.work_times):
            change = (work["start"])
            if type(change) is float:
                temp = str(change)
                sb.work_times[k]["start"] = tool.convert_str_time_to_float_time_again(temp)
            change = (work["end"])
            temp = str(change)
            sb.work_times[k]["end"] = tool.convert_str_time_to_float_time_again(temp)
       work_times_include_break_time = sb.where_to_insert_the_break(work_times=sb.work_times,
                                                                    break_time_total=break_time_total)
    else:
        sb = SetBreak(id=i, start_break_time=one_emp[3], end_break_time=one_emp[4],
                      work_times=start_end_work_time, break_time=0.45, s=s, tool=tool)
        start_break_time = (sb.is_break_time_possible())
        end_break_time = start_break_time + (0.45 / 0.6)
        break_time_total = {}
        break_time_total.setdefault("start_break", start_break_time)
        break_time_total.__setitem__("end_break", end_break_time)
        change = break_time_total["start_break"]
        if type(change) is float:
            temp = str(change)
            break_time_total["start_break"] = tool.convert_str_time_to_float_time_again(temp)
        change = break_time_total["end_break"]
        temp = str(change)
        break_time_total["end_break"] = tool.convert_str_time_to_float_time_again(temp)
        for k, work in enumerate(sb.work_times):
            change = (work["start"])
            if type(change) is float:
                temp = str(change)
                sb.work_times[k]["start"] = tool.convert_str_time_to_float_time_again(temp)
            change = (work["end"])
            temp = str(change)
            sb.work_times[k]["end"] = tool.convert_str_time_to_float_time_again(temp)
        work_times_include_break_time = sb.where_to_insert_the_break(work_times=sb.work_times,
                                                                     break_time_total=break_time_total)
        sb.break_time = 0.2
        work_times_include_break_time = sb.insert_refreshment(work_times_include_break_time, sb.break_time,tool)
    work_times_include_break_time.__setitem__("dest_name", destination_name)
    sb.employees_shift[j].__setitem__(i, work_times_include_break_time)
    return sb.employees_shift

