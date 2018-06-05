import random

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Bestpic, Streamlinks, Genre
from .forms import MovieForm

def index(request):
    form = MovieForm()
    return render(request, 'movies/index.html', {'form': form})

def entry(request,bestpic_id):
    movie_result = Bestpic.objects.get(id = bestpic_id)
    stream_links = Streamlinks.objects.get(id = bestpic_id)
    template = loader.get_template('movies/entry.html')
    image_link = 'images/' + str(bestpic_id) + '.jpg'
    context = {
        'bestpic':movie_result,
        'streamlinks':stream_links,
        'imagelink':image_link,
        'search':0
    }
    return HttpResponse(template.render(context, request))

def search(request):
    form = MovieForm(request.GET)
    query = Bestpic.objects.all()
    winner = request.GET.get('winner', False)
    streaming = request.GET.get('streaming', False)
    if form.is_valid():
        if form.data['min_length']:
            query = query.filter(length__gte = form.cleaned_data['min_length'])
        if form.data['max_length']:
            query = query.filter(length__lte = form.cleaned_data['max_length'])
        if form.data['min_year']:
            query = query.filter(year__gte = form.cleaned_data['min_year'])
        if form.data['max_year']:
            query = query.filter(year__lte = form.cleaned_data['max_year'])
        if form.cleaned_data['genre']:
            query = query.filter(genre__contains = form.cleaned_data['genre'])
        if winner:
            query = query.filter(winner = 1)
        if streaming:
            query = query.filter(streaming = 1)

    total = query.count()
    if total != 0:
        movie_result = query.all()[random.randint(0, total - 1)]
        stream_result = Streamlinks.objects.get(id = movie_result.id)
        image_link = 'images/' + str(movie_result.id) + '.jpg'
        template = loader.get_template('movies/entry.html')
        context = {
            'bestpic':movie_result,
            'streamlinks': stream_result,
            'imagelink':image_link,
            'search':1
        }
    else:
        template = loader.get_template('movies/noresult.html')
        context = {

        }

    return HttpResponse(template.render(context, request))
# Create your views here.
