# Generated by Django 2.1.1 on 2018-10-09 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_moviedetails_review_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='movie_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='main.MovieDetails'),
        ),
    ]
