from django import forms

class RegisterForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    phone_number = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    student_number = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    national_id = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    can_presure = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'form-control'}), required=0, )

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

class NationalIdForm(forms.Form):
    national_id = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}))

class PaymentIdForm(forms.Form):
    payment_id = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}))

class ExtraWorkForm(forms.Form):
    info = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    hour = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
