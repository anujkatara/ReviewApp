from django.db import models
import os
import time
import numpy as np
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


def get_file_path(instance, filename):  # give custom name to file
    ext = filename.split('.')[-1]
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename = "%s.%s" % (str(instance.review_user_id) +
                          "-" + str(timestr), ext)
    return os.path.join('uploads/', filename)


class Category(models.Model):
    """
    This define category
    """
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
                create SEO-friendly url from our app url patterns
        """
        return reverse('movie_list_by_category', args=[self.slug])


class MovieDetails(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    information = models.TextField()
    release_date = models.DateTimeField('date of released')
    pub_date = models.DateTimeField(default=timezone.now)
    cast = models.CharField(max_length=200)
    image_field = models.ImageField(upload_to=get_file_path)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'MovieDetails'
        ordering = ('name', )
        index_together = (('id', 'slug'),)

    def get_absolute_url(self):
        return reverse('main:review_detail', args=[self.id, self.slug])

    def average_rating(self):
        all_ratings = map(lambda x: x.rating, self.review_set.all())
        return np.mean(all_ratings)


class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_name = models.ForeignKey(
        MovieDetails, related_name='comments', on_delete=models.CASCADE)
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    rating = models.IntegerField(choices=RATING_CHOICES)
    pub_date = models.DateTimeField(default=timezone.now)
    comment = models.CharField(max_length=200)

    def __str__(self):
        return self.movie_name.name
