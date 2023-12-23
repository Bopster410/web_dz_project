from django import forms
from app.models import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)

    def clean_password(self):
        data = self.cleaned_data['password']
        if data == 'wrongpass':
            raise forms.ValidationError('Wrong password!')
        return data

    def style_form_error(self):
        for field in self.fields.keys():
            self.add_error(field, '')


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def clean(self):
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        if password != password_check:
            self.add_error('password', '')
            self.add_error('password_check', '')
            raise forms.ValidationError("Passwords don' match")
    
    def save(self, **kwargs):
        self.cleaned_data.pop('password_check')
        return User.objects.create_user(**self.cleaned_data)
