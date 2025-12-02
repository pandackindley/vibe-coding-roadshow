from django import forms
from .models import CPEExperience

class CPEExperienceForm(forms.ModelForm):
    class Meta:
        model = CPEExperience
        fields = ['title', 'details', 'credit_hours', 'date_accomplished']
        widgets = {
            'date_accomplished': forms.DateInput(attrs={'type': 'date'}),
        }