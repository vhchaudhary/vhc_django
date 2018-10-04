from django import forms

GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))
B_GRP_CHOICES = (('ap', 'A+'), ('bp', 'B+'), ('abp', 'AB+'), ('op', 'O+'))


class PersonForm(forms.Form):

    name = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(max_length=20, required=True)
    dob = forms.DateField()
    address = forms.CharField(max_length=50, widget=forms.Textarea())
    mobile = forms.CharField(max_length=13, required=True)
    bld_group = forms.ChoiceField(choices=B_GRP_CHOICES)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect())

