from django import forms
from .models import Profile
from .models import NewsletterUser
from crispy_forms.helper import FormHelper

# Profile Form
# Clean function allows the user to upload an image, if there's no image upload, a default image will be uploaded
# Sign up function retrieves additional sign up info from the user


class ProfileForm(forms.Form):
    name = forms.CharField(max_length=30, label='Name')
    location = forms.CharField(max_length=80, label='Location')
    image = forms.ImageField(required=False)

    def clean(self):
        self.cleaned_data = super().clean()
        image = self.cleaned_data.get('image')
        if not image:
            self.cleaned_data['image'] = 'uploads/profile_pics/default.jpg'

    def signup(self, request, user):
        user.save()
        profile = Profile()
        profile.user = user
        profile.name = self.cleaned_data['name']
        profile.location = self.cleaned_data['location']
        profile.image = self.cleaned_data['image']
        profile.save()


# Newsletter Sign up form


class NewsletterUserSignUpForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_show_labels = False

    class Meta:
        model = NewsletterUser
        fields = ['email']

        def clean_email(self):
            email = self.cleaned_data.get('email')

            return email
