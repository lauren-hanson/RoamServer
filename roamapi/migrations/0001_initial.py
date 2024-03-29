# Generated by Django 4.1.7 on 2023-05-03 22:18

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
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=25)),
                ('state', models.CharField(max_length=25)),
                ('latitude', models.FloatField(blank=True, max_length=25, null=True)),
                ('longitude', models.FloatField(blank=True, max_length=25, null=True)),
                ('tips', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DestinationStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(auto_now_add=True)),
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
                ('subscribers', models.ManyToManyField(related_name='subscriber', through='roamapi.Subscription', to='roamapi.traveler')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=300)),
                ('image_url', models.CharField(blank=True, max_length=250)),
                ('publication_date', models.DateField(auto_now_add=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('weather', models.CharField(blank=True, max_length=300)),
                ('notes', models.CharField(max_length=500)),
                ('public', models.BooleanField(default=False)),
                ('complete', models.BooleanField(default=False)),
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
            field=models.ManyToManyField(through='roamapi.TripDestination', to='roamapi.destination'),
        ),
        migrations.AddField(
            model_name='trip',
            name='tag',
            field=models.ManyToManyField(through='roamapi.TripTag', to='roamapi.tag'),
        ),
        migrations.AddField(
            model_name='trip',
            name='traveler',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip_traveler', to='roamapi.traveler'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='subscriber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribed_follower', to='roamapi.traveler'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='traveler',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='traveler_with_subscribers', to='roamapi.traveler'),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_category', to='roamapi.category')),
            ],
        ),
        migrations.AddField(
            model_name='destination',
            name='destination_status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='status_destination', to='roamapi.destinationstatus'),
        ),
    ]
