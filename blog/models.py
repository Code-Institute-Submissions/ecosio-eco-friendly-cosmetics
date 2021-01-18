from django.db import models

from products.models import Category


class Blog(models.Model):

    class Meta:
        ordering = ['-published_date']

    published_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=55)
    author = models.CharField(max_length=55, null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    blog_category = models.ForeignKey(Category, null=False, blank=False, on_delete=models.CASCADE, related_name='blog_category')
    header_image = models.ImageField()
    intro_paragraph = models.TextField(max_length=300)
    subheading_1 = models.CharField(max_length=55)
    blog_content_1 = models.TextField()
    subheading_2 = models.CharField(max_length=55)
    blog_content_2 = models.TextField()
    subheading_3 = models.CharField(max_length=55, null=True, blank=True)
    blog_content_3 = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
