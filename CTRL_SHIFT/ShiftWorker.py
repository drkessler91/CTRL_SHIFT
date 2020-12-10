

class ShiftWorker:
    queue_tl = []
    queue_at = []
    queue_employees = []

    def add_tl(self, obj):
        self.queue_tl.append(obj)

    def add_at(self, obj):
        self.queue_at.append(obj)

    def add_employee(self, obj):
        self.queue_employees.append(obj)

    @staticmethod
    def fill_teams_in_flight_sets(team_leader, attendants, team_flights, tool):
        team_flights.add_team_members(team_leader, attendants, tool=tool)

    @staticmethod
    def check_equality_teamLeader_to_flights(shift_worker, team_flights, order_flights, needed_more_employees_result,tool):
        if shift_worker.queue_tl.__len__() == team_flights:
            print("match")
        elif shift_worker.queue_tl.__len__() > team_flights:
            amount_of_flights_needed = shift_worker.queue_tl.__len__()-team_flights
            rearranging_the_flights(order_flights.team_flights.flights, amount_of_flights_needed, tool=tool)
        else:
            amount_of_tl_needed = team_flights - len(shift_worker.queue_tl)
            bring_more_employees(amount_of_tl_needed, needed_more_employees_result, shift_worker)
        if shift_worker.queue_at.__len__() >= team_flights:
            print("we have enough attendants")
        else:
            amount_of_at_needed = len(shift_worker.queue_at) - team_flights


def bring_more_employees(number_of_employees_needed, needed_more_employees_result, s):
    if number_of_employees_needed <= needed_more_employees_result.__len__():
        print("you will use this employees: ")
        print(s.queue_tl)
        for employee in needed_more_employees_result:
            if s.queue_tl.__contains__(employee):
                continue
            elif number_of_employees_needed > 0:
                s.add_tl(needed_more_employees_result.pop())
                s.queue_at.pop()
                number_of_employees_needed -= 1
            else:
                break


def rearranging_the_flights(flights, number_of_team_leaders, tool):
    split = []
    first_split = []
    key = 0
    temp = []
    while number_of_team_leaders > 0:
        for i, flight in enumerate(flights.values()):
            if split.__len__() == 0:
                split.append(flight)
            else:
                if len(flight) > split[0].__len__():
                    split = flight
                    key = i
        flights_out = int(split[0].__len__()/2)
        for i in range(flights_out):
            if type(split[0]) is list:
                first_split.append(split[0].pop(0))
            elif type(split[0]) is tuple:
                first_split.append(split.pop(i))
        try_it = split[0].__getitem__(2)
        if type(try_it) is str:
            if tool.convert_str_time_to_float_time(try_it) > tool.convert_str_time_to_float_time(first_split[0].__getitem__(2)):
                temp = split
                flights.__setitem__(str(key), first_split)
                flights[str(flights.__len__())] = temp
        else:
            if tool.convert_str_time_to_float_time(try_it[2]) > tool.convert_str_time_to_float_time(first_split[0].__getitem__(2)):
                temp = (split[0])
                flights.__setitem__(str(key), first_split)
                flights[str(flights.__len__())] = temp
        key = 0
        split = []
        first_split = []
        number_of_team_leaders -= 1

"""
def sort_by_boarding(flights):
    return flights[1]
    
    
    num_of_emp_on_flights = conn.cursor()
    
    num_of_emp_on_flights.execute('''select flightNum,boardingTime,attendants,teamLeader,tsa
                                    from flights
                                    where boardingTime > 11 and boardingTime < 22''')
    help_build_the_mat = num_of_emp_on_flights.fetchall()
"""
