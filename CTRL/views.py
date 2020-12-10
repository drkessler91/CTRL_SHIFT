from django.shortcuts import render, HttpResponse, redirect
from CTRL_SHIFT import CtrlShift
from CTRL.InputForm import InputForm


# Create your views here.


def login(request):
    context = {}
    context['form'] = InputForm()
    return render(request, 'login_page.html', context)

employees_name = CtrlShift.name_for_employee_in_shift
employees_shifts = CtrlShift.fillEmp()
print(employees_shifts)

def shift(request):
    print('Worker Number')
    if request.method == 'POST':
        emp_id = request.POST.get('uname')
        print(emp_id)
        for i in range(employees_shifts.__len__()):
            key = employees_shifts.__getitem__(i)
            if key.get(int(emp_id)):
                print(key)
                for employee_name in range(employees_name.__len__()):
                    key_name = employees_name.__getitem__(employee_name)
                    if key_name[2] == (int(emp_id)):
                        for j in range(key.__len__()):
                            emp = key[int(emp_id)]
                            emp.__setitem__('first_name', key_name[0])
                            emp.__setitem__('last_name', key_name[1])


                            print('emp')
                            print(emp)

                        return render(request, 'shift_page.html', {'emp':emp})


"""
class CtrlConfig(AppConfig):
    name = "CTRL"
"""


