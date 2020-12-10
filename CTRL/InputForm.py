from django import forms


# creating a form
class InputForm(forms.Form):
    uname = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput())
