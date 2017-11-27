from django import forms

class StudentForm(forms.Form):
    stud_id = forms.CharField(max_length=10)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    branch = forms.CharField(max_length=3)
    year = forms.CharField(max_length=4)