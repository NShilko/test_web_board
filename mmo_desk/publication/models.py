from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.TextField()
    main_text = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory', default='Без категории')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}: {self.main_text[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    kind_names = [
        ('onread', 'Ожидание'),
        ('accept', 'Принято'),
        ('cancel', 'Отменено'),
    ]

    main_text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    kind = models.CharField(max_length=6, choices=kind_names, default='onread')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.main_text[:20]

    def get_absolute_url(self):
        return reverse_lazy('post_detail')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    confirmation_code = models.CharField(max_length=10, blank=True, null=True)