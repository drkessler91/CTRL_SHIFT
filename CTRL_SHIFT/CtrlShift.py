from CTRL_SHIFT import Flights
from CTRL_SHIFT import ShiftWorker
from CTRL_SHIFT.HelperSetBreak import HelperSetBreak
from CTRL_SHIFT import SetBreak
from CTRL_SHIFT import MySQLManagement
from CTRL_SHIFT import Tools
import mysql.connector


conn = mysql.connector.connect(host='localhost',
                               database='ground_attendant',
                               user='root',
                               password='78583033k')

cursor = conn.cursor()

# create object with flights needed to assigned with attendants
cursor.execute(
         ''' select FirstName,
                    LastName,
                    employeeNumber
            from attendants_details1
                ''')


name_for_employee_in_shift = cursor.fetchall()


def check_the_name_of_employee(i, name_for_employee_in_shift):
    for employee in name_for_employee_in_shift:
        if i.__contains__(employee[2]):
            return employee
            break


def sort_by_boarding(flights):
    return flights[2]


employees_shifts = []


def fillEmp():
    data_base_management = MySQLManagement.MySQLManagement()

    data_base_management.connect_to_data_base(host='localhost',
                               database='ground_attendant',
                               user='root',
                               password='78583033k')
    cursor = data_base_management.create_data_base_cursor(buffered= False)
    data_base_management.data_base_execute_command(''' select
                                                            flightNum,
                                                            deptTime,
                                                            boardingTime,
                                                            date,
                                                            destName
                                                        from flights1
                                                        where boardingTime > 11 and boardingTime < 22''', cursor=cursor)

    assign_att = data_base_management.data_base_fetchall_data_from_last_execute_command(cursor=cursor)
    order_flights = Flights.Flights()

    for i in assign_att:
        order_flights.add_flight(i)

    order_flights.queue_flights.sort(key=sort_by_boarding)
    order_flights.build_the_matrix(order_flights.queue_flights, order_flights.queue_tree, 0, 0)

    cursor = data_base_management.create_data_base_cursor(buffered=True)
    attendant = data_base_management.create_data_base_cursor(buffered=True)
    needed_more_employees = data_base_management.create_data_base_cursor(buffered=True)

    data_base_management.data_base_execute_command(
        '''select
        FirstName,
        LastName,
        groundAttendantId,
        startShift,
        endShift,
        date
        from worker_shift1 as w, attendants_details1 as ad
        where ad.employeeNumber = w.groundAttendantId and w.startShift > "10:00" and w.startShift < "16:00"
              and w.TeamLeader = 1''', cursor=cursor
    )

    data_base_management.data_base_execute_command(
        '''select
        FirstName,
        LastName,
        groundAttendantId,
        startShift,
        endShift,
        date
        from worker_shift1 as ws, attendants_details1 as a
        where a.employeeNumber = ws.groundAttendantId and ws.startShift > "10:00" and ws.startShift < "16:00"
              and ws.attendant = 1''', cursor=attendant
    )

    data_base_management.data_base_execute_command(
        '''select
    FirstName,
    LastName
    from worker_shift1 as ws, attendants_details1 as a
    where a.employeeNumber = ws.groundAttendantId and a.teamLeader = 1''', cursor=needed_more_employees
    )

    attendants = data_base_management.data_base_fetchall_data_from_last_execute_command(attendant)
    team_leader_result = data_base_management.data_base_fetchall_data_from_last_execute_command(cursor)
    needed_more_employees_result = data_base_management.data_base_fetchall_data_from_last_execute_command(needed_more_employees)

    tool = Tools.Tools()
    shift_worker = ShiftWorker.ShiftWorker()
    for i in team_leader_result:
        shift_worker.add_tl(i)
        shift_worker.add_employee(i)

    for i in attendants:
        shift_worker.add_at(i)
        shift_worker.add_employee(i)

    shift_worker.check_equality_teamLeader_to_flights(shift_worker, order_flights.team_flights.flights.__len__(), order_flights, needed_more_employees_result, tool=tool)

    shift_worker.fill_teams_in_flight_sets(shift_worker.queue_tl, shift_worker.queue_at, order_flights.team_flights, tool=tool)

    helper_set_break = HelperSetBreak()
    helper_set_break.employee_and_his_break = helper_set_break.create_shift_employee(shift_worker.queue_employees)
    team_flights = list(order_flights.team_flights.team_members.values())
    iter_on_teams_keys = "0"
    j = 0
    counter = 0
    name_of_dest = []

    for team in team_flights:
        iter_on_flights = 0
        iter_on_employee = 0
        flight_works_on = order_flights.team_flights.flights.pop(iter_on_teams_keys)
        while team.__len__() != iter_on_employee:
            one_emp = list(team).pop(iter_on_employee)
            i = one_emp[2]
            employees_shifts = (SetBreak.shift_include_break(flight_works_on=flight_works_on, iter_on_teams_keys=iter_on_teams_keys,
                                    iter_on_flights=iter_on_flights, ss=HelperSetBreak, i=i, j=j, one_emp=one_emp, s=shift_worker, tool=tool))
            iter_on_employee += 1
            temp = int(iter_on_teams_keys)
            temp += 1
            iter_on_teams_keys = str(temp)
            j += 1
            employees_shifts.append({})
        counter += 1
        iter_on_teams_keys = str(counter)


    for attendant in shift_worker.queue_at:
        if SetBreak.check_if_employee_exist_on_flights(employees_shifts, attendant[2]):
            value_for_break = HelperSetBreak.employee_and_his_break.get(attendant[2])
            if value_for_break < 1:
                sb = SetBreak.SetBreak(id=attendant[2], start_break_time=attendant[3], end_break_time=attendant[4],
                              work_times=None, break_time=value_for_break, s=shift_worker, tool=tool)
                attendant_start_work_float = sb.start_break_time
                attendant_end_work_float = sb.end_break_time
                break_insertion = (attendant_end_work_float - attendant_start_work_float) / 2
                hour_of_break = attendant_start_work_float + break_insertion
                end_break_time = hour_of_break + (value_for_break / 0.6)
                break_time_total = {}
                break_time_total.setdefault("start_break", hour_of_break)
                break_time_total.__setitem__("end_break", end_break_time)
                employees_shifts[j].__setitem__(attendant[2], break_time_total)
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
                j += 1
                employees_shifts.append({})
            else:
                sb = SetBreak.SetBreak(id=attendant[2], start_break_time=attendant[3], end_break_time=attendant[4],
                              work_times=None, break_time=0.45, s=shift_worker, tool=tool)
                attendant_start_work_float = sb.start_break_time
                attendant_end_work_float = sb.end_break_time
                break_insertion = (attendant_start_work_float - attendant_end_work_float) / 3
                hour_of_break = attendant_start_work_float + break_insertion
                end_break_time = hour_of_break + (0.45 / 0.6)
                break_time_total = {}
                break_time_total.setdefault("start_break",hour_of_break)
                break_time_total.__setitem__("end_break", end_break_time)
                hour_of_break = break_time_total["end_break"] + break_insertion
                end_break_time = hour_of_break + (0.2/0.6)
                break_time_total.__setitem__("start_refreshment", hour_of_break)
                break_time_total.__setitem__("end_refreshment", end_break_time)
                change = break_time_total["start_refreshment"]
                if type(change) is float:
                    temp = str(change)
                    break_time_total["start_refreshment"] = tool.convert_str_time_to_float_time_again(temp)
                    change = break_time_total["end_refreshment"]
                    temp = str(change)
                    break_time_total["end_refreshment"] = tool.convert_str_time_to_float_time_again(temp)
                employees_shifts[j].__setitem__(attendant[2], break_time_total)
                j += 1
                employees_shifts.append({})
        else:
            continue

    for i in employees_shifts:
        employee_name = check_the_name_of_employee(i, name_for_employee_in_shift)
        if employee_name is None:
            continue
        else:
            for check in shift_worker.queue_employees:
                if check[2] != employee_name[2]:
                    continue
                else:
                    #print("This the attendant ", employee_name)
                    #print("This is the start of the shift ", check[3])
                    #print("This is the end of the shift ", check[4])
                    #print("this is the shift", i)
                    print()
        return employees_shifts

