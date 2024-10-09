from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    
    phone = models.CharField(max_length = 13)
    profile_image = models.ImageField(upload_to = 'profile/')
    id_proof = models.ImageField(upload_to = 'profile/')
    profile_description = models.TextField(max_length = 100)
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    
   

class Blog(models.Model):
    status_choices = (
        ('PUBLISH', 'Publish'),
        ('DRAFT', 'Draft'),
       
    )
    title = models.CharField(max_length = 100)
    content = models.TextField(max_length = 200)
    blog_image = models.ImageField(upload_to = 'blog/')
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    status = models.CharField(max_length = 50, choices=status_choices, default='DRAFT')

    def __str__(self):
        return self.title

class Comment(models.Model):
    STATUS_CHOICES = (
        ('visible', 'Visible'),
        ('hidden', 'Hidden'),
    )
    comment = models.TextField(max_length = 300)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True) 
    status = models.CharField(max_length = 50, choices=STATUS_CHOICES, default='visible')   

    def __str__(self):
        return self.comment
