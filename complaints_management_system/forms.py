from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Complaints,Respondents,Purok,Position,Entities,Complainant

User = get_user_model()


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username","email","first_name","last_name","entity","password1","password2"]

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['required'] = 'true'
            visible.field.widget.attrs['placeholder'] = 'Enter your information'


class ComplaintsForm(ModelForm):

    class Meta:
        model = Complaints
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ComplaintsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = 'Enter your information'



class RespondentForm(ModelForm):

    class Meta:
        model = Respondents
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(RespondentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = 'Enter your information'

class PurokForm(ModelForm):

    class Meta:
        model = Purok
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PurokForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = 'Enter your information'


class PositionForm(ModelForm):

    class Meta:
        model = Position
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PositionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = 'Enter your information Ex: Brgy. Captain'

class EntitiesForm(ModelForm):

    class Meta:
        model = Entities
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(EntitiesForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = 'Enter your information'


class ComplainantForm(ModelForm):

    class Meta:
        model = Complainant
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ComplainantForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = 'Enter your information'
