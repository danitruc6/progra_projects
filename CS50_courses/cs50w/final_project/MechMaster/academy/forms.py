from django import forms
from .models import *

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic_upload','bio']
        widgets = {
            'bio': forms.Textarea(attrs={'placeholder': 'Enter you bio here...', 'rows': 3, 'cols': 40})
        }
        labels ={
            'profile_pic_upload':'Upload your profile image \n',
            'bio': 'Bio Description',
        }

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    rating = forms.ChoiceField(
        label='Select your Rating',
        choices=RATING_CHOICES,
        initial=5,  # Set the initial/default value to 5 (five stars)
        widget=forms.Select(attrs={'class': "form-control review-form"})
    )
    comment = forms.CharField(
        label='Comment',
        widget=forms.Textarea(attrs={'rows': 3, 'class': "form-control review-form"})
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']



class ForumTopicForm(forms.ModelForm):
    class Meta:
        model = ForumTopic
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Title', 'size':70}),
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'rows': 4, 'cols': 70}),
        }
        # Removing the labels, not aesthetic 
        labels = {
            'title': '',
            'description': '',
        }

class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder':'Write your reply here...', 'cols': 95, 'rows':3}),  
        }
        labels = {
            'content': ''
        }

class QuizAttemptForm(forms.Form):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        options = Option.objects.filter(question=question)
        choices = [(option.id, option.text) for option in options]
        self.fields['options'] = forms.ChoiceField(widget=forms.RadioSelect, choices=choices)

