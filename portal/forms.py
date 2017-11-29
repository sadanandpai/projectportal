from django import forms

class StudentForm(forms.Form):
    username = forms.CharField(max_length=10)
    first_name = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=50)
    last_name = forms.CharField(max_length=20)
    branch = forms.CharField(max_length=3)
    year = forms.CharField(max_length=4)


class SigninForm(forms.Form):
    username = forms.CharField(min_length=5, max_length=20)
    password = forms.CharField(min_length=5, max_length=20)