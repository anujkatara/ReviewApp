from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 40, 'rows': 15}))

    class Meta:
        model = Review
        fields = ['review_user', 'rating', 'comment']
