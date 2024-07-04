from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "mobile", "password1", "password2"]

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        user.password = self.cleaned_data["password1"]
        user.mobile = self.cleaned_data["mobile"]
        if commit:
            user.save()
        else:
            print("ERROR")
        return user
