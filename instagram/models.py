from django.db import models
from django.conf import settings
import re
from django.urls import reverse

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True # 실제 DB table은 생성되지 않는다.

class Post(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="instagram/post/%Y/%m/%d")
    caption = models.CharField(max_length=500)
    tag_set = models.ManyToManyField('Tag', blank=True)
    location = models.CharField(max_length=100)
    

    def __str__(self):
        return self.caption

    def get_absolute_url(self):
        return reverse("instagram:post_detail", args=[self.pk])

    def extract_tag_list(self):
        tag_name_list = re.findall(r"#([a-zA-Z\dㄱ-힣]+)", self.caption)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list
    

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name