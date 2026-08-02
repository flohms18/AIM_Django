from django.db import models
from tinymce.models import HTMLField
from django.utils.text import slugify 

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(blank=True,default="Slug to add")  # Add the slug field

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
            return self.name

class Post(models.Model):
    title = models.CharField(max_length=300,null=False)
    slug = models.SlugField(unique=True,null=False)
    excerpt = models.TextField(null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="posts")    
    content = HTMLField()
    published_date = models.DateField()
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)

    def __str__(self):
            return self.title

