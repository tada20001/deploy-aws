import os
from uuid import uuid4

from django.db import models
from django.conf import settings

from embed_video.fields import EmbedVideoField
from django.forms import ValidationError
from accounts.models import User, Artist, Category
from django.urls import reverse

def min_length_3_validator(value):
    if len(value) < 3 :
        raise ValidationError('3글자 이상 입력해 주세요.')

def upload_to(instance, filename):
    uuid_name = uuid4().hex
    ext = os.path.splitext(filename)[-1].lower()
    return 'images/%s/%s/' % (
        instance.artist.user.profile.name,
        uuid_name[4:] + ext
    )

class Work(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, validators=[min_length_3_validator])
    image1 = models.ImageField(upload_to=upload_to, blank=True, null=True)
    image2 = models.ImageField(upload_to=upload_to, blank=True, null=True)
    image3 = models.ImageField(upload_to=upload_to, blank=True, null=True)
    image4 = models.ImageField(upload_to=upload_to, blank=True, null=True)
    image5 = models.ImageField(upload_to=upload_to, blank=True, null=True)

    video = EmbedVideoField(blank=True) # same like models.URLField()
    description = models.TextField(blank=True)
    category = models.ManyToManyField(Category)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    tags = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('ArtandArtists:work_detail', args=[self.id])

    def __str__(self):
        return self.title


# class Images(models.Model):
#     work = models.ForeignKey(Work, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to=upload_to, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.work.title + " images"
