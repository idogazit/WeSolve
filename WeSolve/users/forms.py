from django_registration.forms import RegistrationForm
from users.models import CustomUser
from django import forms as dj_forms


class CustomUserForm(RegistrationForm):
    first_name = dj_forms.CharField(max_length=30, required=True)
    last_name = dj_forms.CharField(max_length=30, required=True)
    user_image = dj_forms.ImageField(required=False)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if self.cleaned_data['user_image']:
            user.userPic = self.cleaned_data['user_image']

        if commit:
            user.save()

        return user

    class Meta(RegistrationForm.Meta):
        field = ('first_name','last_name','user_image')
        model = CustomUser

    def clean(self):
        if not str(self.cleaned_data['email']).endswith("tau.ac.il"):
            raise dj_forms.ValidationError('Only TAU email accounts are allowed')
