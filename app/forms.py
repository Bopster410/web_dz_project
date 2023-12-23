from django import forms

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