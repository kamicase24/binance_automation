from allauth.account.forms import LoginForm

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Agregar clases a los campos
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = None
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'remember':
                field.widget.attrs['class'] = 'form-check-input'
                field.label = 'Mantener sesión'