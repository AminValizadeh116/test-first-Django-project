from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django_cleanup import cleanup
from django_resized import ResizedImageField


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_user')
    reading_time = models.PositiveIntegerField()
    slug = models.SlugField()

    class Status(models.TextChoices):
        DRAFT = 'DR', 'DRAFT'
        REJECTED = 'RJ', 'REJECTED'
        PUBLISHED = 'PB', 'PUBLISHED'
    status = models.CharField(max_length=120, choices=Status.choices, default=Status.DRAFT)

    CATEGORY_CHOICES = (
        ('programming language', 'programming language'),
        ('AI', 'AI'),
        ('frontend', 'frontend'),
        ('backend', 'backend'),
        ('security', 'security'),
        ('others', 'others')
    )

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['status']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        for img in self.images.all():
            storage, path = img.image_file.storage, img.image_file.path
            storage.delete(path)
        super().delete(*args, **kwargs)


class Comment(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    creation_time = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.title


@ cleanup.select
class Image(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    image_file = models.ImageField(upload_to='post_images/')

    def name(self):
        return str(self.title) if self.title else str(self.image_file.name)

    def __str__(self):
        return self.name()


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account', blank=True, null=True)
    job = models.CharField(max_length=120, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    photo = ResizedImageField(size=[200, 200], crop=['middle', 'center'], blank=True, null=True)
