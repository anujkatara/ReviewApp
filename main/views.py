"""
View for my review Site
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg, Count
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import MovieDetails, Category, Review
from .forms import ReviewForm
import datetime

# Create your views here.


def review_list(request, category_slug=None):
    """
    Function used to display a list of products.
    Second parameter category_slug=None use if products are filtered using
    a given category by our users.
    """
    category = None
    categories = Category.objects.all()
    latest_review_list = MovieDetails.objects.all()
    a = Review.objects.all().aggregate(Avg('rating'))
    b = ''.join('{}'.format(val) for key, val in a.items())
    c = int(float(b))

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        latest_review_list = MovieDetails.objects.filter(category=category)

    paginator = Paginator(latest_review_list, 2)
    page = request.GET.get('page')
    try:
        latest_review_list = paginator.page(page)
    except PageNotAnInteger:
        latest_review_list = paginator.page(1)
    except EmptyPage:
        latest_review_list = paginator.page(paginator.num_pages)

    context = {
        'category': category,
        'categories': categories,
        'latest_review_list': latest_review_list,
        'c': c,
        'total_rating': range(5)
    }
    return render(request, 'review_list.html', context)


def review_detail(request, id, slug):
    """
    Movie Details
    """
    review = get_object_or_404(MovieDetails, id=id, slug=slug)
    a = Review.objects.filter(movie_name=review).aggregate(Avg('rating'))
    b = ''.join('{}'.format(val) for key, val in a.items())
    c = int(float(b))

    posts_list = Review.objects.filter(movie_name=review).order_by('-id')
    print(posts_list)

    paginator = Paginator(posts_list, 3)

    try:
        page = int(request.GET.get('page', '1'))
    except PageNotAnInteger:
        page = 1

    try:
        # posts = paginator.page(page)
        posts = paginator.get_page(page)
        print(posts)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'review': review,
        'posts': posts,
        'c': c,
        'total_rating': range(5)
    }
    return render(request, 'review_detail.html', context)


@login_required
def add_review(request, id):
    movie = get_object_or_404(MovieDetails, pk=id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review_user = form.cleaned_data['review_user']
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        review = Review()
        review.movie_name = movie
        review.review_user = review_user
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        return HttpResponseRedirect(reverse('review_detail', args=(movie.id, movie.slug)))

    return render(request, 'reviewform.html', {'movie': movie, 'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('review_list')
            else:
                return HttpResponse("account is disable")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return redirect('review_list')


def top_commented(request):
    tops = MovieDetails.objects.annotate(
        like_count=Count('comments')).order_by('-like_count')
    return render(request, 'top_rated_movie.html', {'tops': tops})
