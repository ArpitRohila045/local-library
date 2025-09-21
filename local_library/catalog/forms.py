from django import forms
import datetime 
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and four weeks (default 3 weeks)")


    def clean_renewal_date(self):
        date = self.cleaned_data['renewal_date']

        if date < datetime.date.today():
            raise ValidationError(_("invalid date - renewal in past "))
        
        if date > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_("Invalid date - renewal is more than 4 weeks "))
        
        return date
