from django.db import models
from django.utils import timezone
from django.urls import reverse
from PIL import Image
from django.db import models
from django.db.models.signals import post_save
import uuid
import os
from django.contrib.auth.models import User



def image_upload(self, uploaded_file_name):
    prefix = 'post_images/%s/' %(self.author)
    extension = os.path.splitext(uploaded_file_name)[-1]
    if self.pk != None:
        return prefix + str(self.pk) + extension
    else:
        tmp_name = str(uuid.uuid4())
        self.temp_image = prefix + tmp_name + extension
        return self.temp_image

        
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    post_date = models.DateTimeField(default=timezone.now)
    post_update = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    onlyMe = models.NullBooleanField(default=False,blank=True, null=True)
    stuff = models.URLField( max_length=2000, blank=True, null=True)
    image = models.ImageField( default="#",upload_to=image_upload,blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-post_date',)
    
        

            
    def get_absolute_url(self):
        #return '/detail/{}'.format(self.pk)
        return reverse('detail', args=[self.pk])

    @property
    def get_photo_url(self, *args, **kwargs):
         if self.image and hasattr(self.image, 'url'):
            super().save(*args, **kwargs)
            img = Image.open(self.image.path)
            if img.width > 800 or img.height > 800:
                output_size = (800, 800)
                img.thumbnail(output_size)
                img.save(self.image.path)
            return self.image.url



class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,blank=True, null=True, related_name='user_comment')
    name = models.CharField(max_length=50, verbose_name='الأسم')
    email = models.EmailField(verbose_name="البريد الإلكتروني")
    body = models.TextField(verbose_name="التعليق")
    comment_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return 'علق {} على {}.'.format(self.name, self.post)

    class Meta:
        ordering = ('-comment_date',)



    

class Profile(models.Model):
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} profile'.format(self.user.username)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.width > 300 or img.height > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)



def create_profile(sender, **kwarg):
    if kwarg['created']:
        Profile.objects.create(user=kwarg['instance'])


post_save.connect(create_profile, sender=User)
