# Generated by Django 4.1.7 on 2023-03-13 18:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=25)),
                ('state', models.CharField(max_length=25)),
                ('latitude', models.FloatField(max_length=25)),
                ('longitude', models.FloatField(max_length=25)),
                ('start', models.BooleanField(default=False)),
                ('end', models.BooleanField(default=False)),
                ('quickStop', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Traveler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(max_length=500)),
                ('profile_image_url', models.CharField(max_length=250)),
                ('followers', models.ManyToManyField(related_name='follower', through='roamapi.Follower', to='roamapi.traveler')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('notes', models.CharField(max_length=500)),
                ('public', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TripTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tag_trips', to='roamapi.tag')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip_tags', to='roamapi.trip')),
            ],
        ),
        migrations.CreateModel(
            name='TripDestination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_trip', to='roamapi.destination')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip_destination', to='roamapi.trip')),
            ],
        ),
        migrations.AddField(
            model_name='trip',
            name='destination',
            field=models.ManyToManyField(related_name='destinations_of_trip', through='roamapi.TripDestination', to='roamapi.destination'),
        ),
        migrations.AddField(
            model_name='trip',
            name='tag',
            field=models.ManyToManyField(related_name='tags_of_post', through='roamapi.TripTag', to='roamapi.tag'),
        ),
        migrations.AddField(
            model_name='trip',
            name='traveler',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roamapi.traveler'),
        ),
        migrations.AddField(
            model_name='follower',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_traveler', to='roamapi.traveler'),
        ),
        migrations.AddField(
            model_name='follower',
            name='traveler',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='traveler_follower', to='roamapi.traveler'),
        ),
    ]
