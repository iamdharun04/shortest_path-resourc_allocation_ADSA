# forms.py

from django import forms
from .models import Gear

WEATHER_CHOICES = [
    ('Sunny', 'Sunny'),
    ('Rainy', 'Rainy'),
    ('Snowy', 'Snowy'),
    ('Cold', 'Cold'),
    ('Clear', 'Clear'),
]

TERRAIN_CHOICES = [
    ('Mountain', 'Mountain'),
    ('Forest', 'Forest'),
    ('Beach', 'Beach'),
    ('Lake', 'Lake'),
    ('River', 'River'),
    ('City', 'City'),
    ('Park', 'Park'),
]

class GearPlannerForm(forms.Form):
    trip_duration = forms.IntegerField(label='Trip Duration (days)', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter trip duration'}))
    weather_condition = forms.ChoiceField(choices=WEATHER_CHOICES, label='Weather Condition', widget=forms.Select(attrs={'class': 'form-control'}))
    terrain_type = forms.ChoiceField(choices=TERRAIN_CHOICES, label='Terrain Type', widget=forms.Select(attrs={'class': 'form-control'}))
    max_weight = forms.IntegerField(label='Maximum Weight Capacity (kg)', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter max weight capacity'}))
