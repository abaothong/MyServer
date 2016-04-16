__author__ = 'haoyi'

from django import forms
from django.contrib.auth.models import User

from datetime import date
from abaoblog.models import Post


# class PostForm(forms.Form):
#     title = forms.CharField(widget=forms.TextInput(attrs=dict(requited=True, max_length=150, size=20)), label="Title")
#
#     post_content = forms.CharField(
#         widget=forms.Textarea(attrs=dict(requited=True, rows=10, cols=90, style='resize:none')),
#         label="Title")
#
#     publish_date = forms.DateField(widget=forms.DateInput(attrs=dict(requited=True), format=(
#         '%d %b %Y')), initial=date.today, label="Publish Date")
#
#     publish_time = forms.TimeField(widget=forms.TimeInput(
#         attrs=dict(requited=True, input_formats=('%H:%M%A', '%H:%M %A', '%H:%M%a', '%H:%M %a'))),
#         label="Publish Time")

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)
        widgets = {
            'title': forms.TextInput(attrs=dict(requited=True, max_length=150, size=50)),
            'text': forms.Textarea(attrs=dict(requited=True, rows=10, cols=90, style='resize:none'))
        }


class RegistrationForm(forms.Form):
    username = forms.RegexField(regex="^\w+$",
                                widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
                                label="Username",
                                error_messages={
                                    'username': "Username must only contain letters, numbers and underscores"})

    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
                             label="Email")

    password_1 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(requited=True, max_length=30, render_value=False)),
        label="Password")

    password_2 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(requited=True, max_length=30, render_value=False)),
        label="Reenter Password")

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError({'username': ["The username already exists. Please try another one."]})

    def clean(self):
        if 'password_1' in self.cleaned_data and 'password_2' in self.cleaned_data:
            if self.cleaned_data['password_1'] != self.cleaned_data['password_2']:
                raise forms.ValidationError({'password_1': "Passwords must be the same."})
        return self.cleaned_data
