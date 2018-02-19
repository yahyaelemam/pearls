from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="User ", max_length=20)
    password = forms.CharField(label="Password ", widget=forms.PasswordInput)
