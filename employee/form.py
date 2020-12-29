from django import forms
from django.contrib.auth.models import User,Group
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ModelChoiceField(queryset=Group.objects.all())
    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'email', 'username','password'
                  ]


        # excludes = ['']

        label = {
            'password': 'Password'
        }
    # To see user role
    def __init__(self,*args,**kwargs):
        if kwargs.get('instance'):
            #We get the 'Initial' keyword argument or initialize it
            #as a dict of it did't exits.
            initial =kwargs.setdefault('initial',{})
            # the widget for a ModelultipleChoiceField expects
            # a list of primary key for the selected data
            if kwargs['instance'].groups.all():
                initial["role"] = kwargs['instance'].groups.all()[0]
            else:
                initial['role'] =None
        forms.ModelForm.__init__(self,*args,**kwargs)

        ##Custom Validation
        # def clean_email(self):
        #     if self.cleaned_data["email"].endsWith('@aravtech.com'):
        #         return self.cleaned_date['email']
        #     else:
        #         raise ValidationError
        # returning hash password
    def save(self):
        password = self.cleaned_data.pop('password')
        role = self.cleaned_data.pop('role')
        u = super().save()
        # save role
        u.groups.set([role])
        u.set_password(password)
        u.save()
        return u

    #  need filter all emplyees and hash paaword #14 | CRUD operations on User
