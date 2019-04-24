from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Sword(models.Model):
    name = models.CharField(max_length=100)
    link = models.URLField(max_length=200)
    manufacturer = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    sword_type = models.CharField(max_length=50)
    weight = models.CharField(max_length=20, blank=True)
    overall_length = models.CharField(max_length=30, blank=True)
    tip_type = models.CharField(max_length=20, blank=True)

    def average_rating(self):
        return self.review_set.aggregate(models.Avg('rating'))['rating__avg']

    def __str__(self):
        return self.name


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    sword = models.ForeignKey(Sword, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    rating = models.IntegerField(choices=RATING_CHOICES)

    def __str__(self):
        return f'{self.author.username} reviewed {self.sword.name}'

    def get_absolute_url(self):
        return reverse('sword_detail', kwargs={'pk': self.sword.pk})


class Cluster(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    def get_members(self):
        return "\n".join([u.username for u in self.users.all()])
