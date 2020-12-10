

class HelperSetBreak:
    hash_breakType = " "  # checks whether it's break or refreshment and sets time for
    employee_and_his_break = {}
    breakTime = 0
    set_flight_tl = []

    def set_none_shift(self):
        for j in range(self.emp.tl):
            for i in range(6):
                name = self.emp.skill["tl"][j][0]
                aval = self.emp.skill["tl"][j][1]
                if self.f[i].get_tl() == "" and aval is True:
                    self.f[i].set_tl(name)
                    self.emp.skill["tl"][j][1] = False
                    self.emp.skill["ga"][j][1] = False
                    break

    def create_shift_employee(self, work: list):
        j = 0
        for i in work:
            self.set_break(j, work=work)
            j += 1
        return self.employee_and_his_break

    def set_break(self, index, work: list):
        if work[index][4] == "19:00" and work[index][3] == "12:30" or work[index][4] == "19:00" and work[index][
            3] == "11:00" or work[index][4] == "21:00" and work[index][3] == "14:00" or work[index][4] == "01:30" and \
                work[index][3] == "18:00" or work[index][4] == "01:30" and work[index][3] == "19:00":
            HelperSetBreak.hash_breakType = "45_break"
            HelperSetBreak.breakTime = 0.45
            self.employee_and_his_break.setdefault(work[index][2], HelperSetBreak.breakTime)
            return self.employee_and_his_break
        elif work[index][4] == "01:30" and work[index][3] == "21:00":
            HelperSetBreak.hash_breakType = "no break"
            print(work[index][0], work[index][1], "have no break")
        #      elif shift_time <= 5:
        #         SettingBreak.hash_breakType = "refreshment"
        #        SettingBreak.breakTime = 0.20
        elif work[index][4] == "01:30" and work[index][3] == "14:00" or work[index][4] == "00:30" and work[index][3] == "14:00":  # 10 hours shift
            HelperSetBreak.hash_breakType = "45_20_break"
            HelperSetBreak.breakTime = 1.05
            self.employee_and_his_break.setdefault(work[index][2], HelperSetBreak.breakTime)

