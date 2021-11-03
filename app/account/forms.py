from django.forms import Form, EmailField, PasswordInput, CharField, ValidationError


class LoginForm(Form):
    """Форма входа"""
    email = EmailField()
    password = CharField(widget=PasswordInput)


class RegisterForm(Form):
    """Форма регистрации"""
    password = CharField(label="password", min_length=8, widget=PasswordInput)
    password2 = CharField(label="repeat password", min_length=8, widget=PasswordInput)
    code = CharField(label="access code")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError("passwords don't match")
        return cd['password2']
