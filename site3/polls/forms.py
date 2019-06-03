from django import forms

class RegisterForm(forms.Form):

    #username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    #email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    #password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    #password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    phone_number = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    student_number = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    national_id = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    #entry_year = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    can_presure = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'form-control'}), required=0, )


    '''
    user
    first_name
    last_name
    phone_number
    student_number
    entry_year

    can_presure
    '''

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
