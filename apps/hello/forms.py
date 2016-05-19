from django import forms
from apps.hello.models import Person


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=30,
                               required=True)


class EditForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'birth_date',
                  'con_email', 'con_jabbber', 'con_skype', 'con_other',
                  'bio', 'photo')
                
