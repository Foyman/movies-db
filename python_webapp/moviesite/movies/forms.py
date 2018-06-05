from django import forms
#import floppyforms as forms
from .models import Genre

# class Slider(forms.RangeInput):
#     min = 60
#     max = 270
#     step = 30
#     template_name = 'slider.html'
#
#     class Media:
#         js = (
#             'js/jquery.min.js',
#             'js/jquery-ui.min.js',
#         )
#         css = {
#             'all': (
#                 'css/jquery-ui.css',
#             )
#         }

class MovieForm(forms.Form):
    #test_slider = forms.IntegerField(widget=Slider)
    min_year = forms.IntegerField(label = 'min_year', max_value = 2017, min_value = 1927, required = False)
    max_year = forms.IntegerField(label = 'max_year', max_value = 2017, min_value = 1927, required = False)
    min_length = forms.IntegerField(label = 'min_length', max_value = 248, min_value = 66, required = False)
    max_length = forms.IntegerField(label = 'max_length', max_value = 248, min_value = 66, required = False)
    genre = forms.ChoiceField(choices = Genre.GENRE_CHOICES, required = False)
    winner = forms.BooleanField(label = 'winner', initial = False, required = False)
    streaming = forms.BooleanField(label = 'streaming', initial = False, required = False)
