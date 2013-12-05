from django.db import models
from django.contrib.auth.models import User
from django.contrib import auth
# Create your models here.

class Activity(models.Model):
    activitytype = models.TextField(max_length=20)
    name = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=500)
    time = models.DateTimeField()
    posttime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    picture = models.ImageField(upload_to="activity-photos",blank=True)
    privacy = models.PositiveIntegerField(default=0)       # 0: public  1: private
    lat = models.FloatField(blank=True)
    lng = models.FloatField(blank=True)

    def getFollowers(self):
        return Followers.objects.filter(activity = self)

    def getComments(self):
        return Comment.objects.filter(activity = self)

class Followers(models.Model):
    activity = models.ForeignKey(Activity)
    user = models.ForeignKey(User)

class UserFollowers(models.Model):
    user = models.ForeignKey(User, related_name='user')
    friends = models.ManyToManyField(User, related_name='user_friends')
    active = models.BooleanField(default=False)
    def __unicode__(self):
        return self.user

class UnConfirmedFriend(models.Model):
    requestuser = models.ForeignKey(User, related_name='requestuser')
    confirmuser = models.ForeignKey(User, related_name='confirmuser')

class IgnoredNearByActivity(models.Model):
    user = models.ForeignKey(User)
    activityID = models.CharField(max_length=20)

class Info(models.Model):
    firstname = models.CharField(max_length=200,blank=True)
    lastname = models.CharField(max_length=200,blank=True)
    email = models.CharField(max_length=200)
    level = models.PositiveIntegerField(default=0)
    user = models.OneToOneField(User)
    #interests = models.ManyToManyField(Interest)
    address = models.CharField(max_length=200,blank=True)
    picture=models.ImageField(upload_to="info-photos",blank=True)

class Comment(models.Model):
    text         = models.CharField(max_length=200)
    activity     = models.ForeignKey(Activity)
    posting_time = models.DateTimeField(auto_now_add=True)
    commenter    = models.ForeignKey(User)

    def __unicode__(self):
        return self.text

    #def getUserPicture(self):
    #    info = Info.objects.filter(user = self.commenter)[0]
    #    return info.picture;

class Feedback(models.Model):
    activity = models.ForeignKey(Activity)
    text = models.CharField(max_length=500,blank=True)
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    picture = models.ImageField(upload_to="feedback-photos",blank=True)

class UnreadActivityInvitation(models.Model):
    user = models.ForeignKey(User)
    activityID = models.CharField(max_length=20)

class UserLocation(models.Model):
    user = models.ForeignKey(User)
    lat = models.FloatField()
    lng = models.FloatField()

#add customed function to User model
def get_friends(self):
 #   checkuser = UserFollowers.objects.get(user=self)
 #   if(len(checkuser)>0):
    userfollow = UserFollowers.objects.get(user=self)
    friends = userfollow.friends.all()
    return friends

auth.models.User.add_to_class('get_friends', get_friends)
