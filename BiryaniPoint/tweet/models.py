from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    text = models.TextField(max_length=280)
    
    photo = models.ImageField(
        upload_to='tweet_photos/',
        blank=True,
        null=True
        )
    
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies"
    )
   
    likes = models.ManyToManyField(
        User,
        related_name='liked_tweets',
        blank=True
    )
    
    retweets = models.ManyToManyField(
        User,
        related_name="retweeted_tweets",
        blank = True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def retweet_count(self):
        return self.retweets.count()
    
    @property
    def is_reply(self):
        return self.parent is not None
    
    @property
    def like_count(self):
        return self.likes.count()
    
    @property
    def reply_count(self):
        return self.replies.count()
        
    
   
    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["parent"]),
            ]

        
    def clean(self):
        if not self.text and not self.photo:
            raise ValidationError("Tweet must contain text or photo.")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

            
    def __str__(self):
        return f"{self.user.username}: {(self.text or 'Photo Tweet')[:50]}"     


class Follow(models.Model):
    follower = models.ForeignKey(
        User,on_delete=models.CASCADE,related_name="following_relationships"
    )
    
    following = models.ForeignKey(
        User,on_delete=models.CASCADE,related_name="follower_relationships"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
            fields=["follower", "following"],
            name="unique_follow_relationship"
        )
        ]
        indexes = [
        models.Index(fields=["follower"]),
        models.Index(fields=["following"]),
        ]

    def clean(self):
        if self.follower == self.following:
            raise ValidationError("You cannot follow yourself.")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
    
        
        