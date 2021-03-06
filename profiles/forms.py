from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = (
            'user', 'earned_loyalty_points',
            'donated_loyalty_points', 'total_loyalty_points',
            'going_to_event', 'donated_loyalty_points_plant_tree',
            'donated_loyalty_points_recycle_plastic', 'donated_loyalty_points_clean_forest',
            )
        labels = {
            'default_phone_number': 'phone number',
            'default_country': 'country',
            'default_postcode': 'postcode',
            'default_town_or_city': 'town or city',
            'default_street_address': 'street address',
        }

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'phone number',
            'default_postcode': 'postcode',
            'default_town_or_city': 'town or city',
            'default_street_address': 'street address',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]}'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'rounded-0 profile-form-input'
