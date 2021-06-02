from django import forms
from django.db.models import fields
from accounts.models import *

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields=['subject','review','rating']