from django.urls import path, re_path
from main import views

urlpatterns = [
    path('', views.review_list, name='review_list'),
    path('top_commented', views.top_commented, name='top_commented'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    re_path(r'^(?P<id>\d+)/add_review/$', views.add_review, name='add_review'),
    re_path(r'^(?P<category_slug>[-\w]+)/$',
            views.review_list, name='movie_list_by_category'),
    re_path(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',
            views.review_detail, name='review_detail'),
]
