from django.db import models

class News(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly define the id as auto-incrementing
    title = models.CharField(max_length=255)  # Title of the news
    text = models.TextField()  # Content of the news
    picture = models.CharField(max_length=500,  null=True)  # URL for the news picture
    tags = models.JSONField(default=list, blank=True)  # Tags as a JSON array
    views = models.PositiveIntegerField(default=0)  # Number of views
    like = models.PositiveIntegerField(default=0)  # Number of likes
    dislike = models.PositiveIntegerField(default=0)  # Number of dislikes
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the news was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the news was last updated

