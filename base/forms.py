from django import forms
from django.contrib.auth import get_user_model
from .models import Car

# Get the custom user model
User = get_user_model()

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'profile_image', 
            'phone', 'address', 'job_title', 'bio'
        ]
        
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'profile_image':
                self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['bio'].widget.attrs.update({'rows': 4})

class NotificationSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email_notifications', 'push_notifications', 'sms_notifications']
        
class PrivacySettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_visibility', 'contact_preference', 'data_collection', 'personalized_ads']
        
class AccountSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['two_factor_auth']
        
class AppearanceSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['theme_preference']

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['name', 'brand', 'year', 'price', 'description', 'image']