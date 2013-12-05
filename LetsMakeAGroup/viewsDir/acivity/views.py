from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from LetsMakeAGroup.models import *
# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required
# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.db import transaction
from datetime import datetime
from django.http import HttpResponse
import json
from mimetypes import guess_type
import math

@transaction.commit_on_success
@login_required
def post_activity(request):
  if request.method == 'POST':
    #Because this form is in a popup table, we plan to validate the input in a javascript not here
    address = request.POST['address1'] + " " + request.POST['address2'] + ", " + request.POST['city']
    datetime = request.POST['date'] +" " + request.POST['time']
    if 'picture' in request.FILES and request.FILES['picture']:
      new_activity = Activity.objects.create(user         = request.user,
                                             name         = request.POST['name'],
                                             activitytype = request.POST['activity_type'],
                                             description  = request.POST['description'],
                                             address      = address,
                                             time         = datetime,
                                             picture      = request.FILES['picture'],
                                             privacy      = int(request.POST["privacy"]),
                                             lat          = 0,
                                             lng          = 0)
    else:
      new_activity = Activity.objects.create(user         = request.user,
                                             name         = request.POST['name'],
                                             activitytype = request.POST['activity_type'],
                                             description  = request.POST['description'],
                                             address      = address,
                                             time         = datetime,
                                             privacy      = int(request.POST["privacy"]),
                                             lat          = 0,
                                             lng          = 0)
    new_activity.save()
    if 'lat' in request.POST and request.POST['lat']:
      new_activity.lat = request.POST['lat']

    if 'lng' in request.POST and request.POST['lng']:
      new_activity.lng = request.POST['lng']

    new_activity.save()

    #TODO: use request.POST[invited_friend_i], which is the friend's id to generate an unread massage for him/her
    i=1;
    invited_friend_i = "invited_friend_" + str(i)
    while invited_friend_i in request.POST and request.POST[invited_friend_i]:
      invited_user = User.objects.get(id=request.POST[invited_friend_i])
      UnreadActivityInvitation.objects.create(user=invited_user, activityID=new_activity.id).save()
      i+=1
      invited_friend_i = "invited_friend_" + str(i)


  return redirect(reverse('index'))
  #return render(request, 'index.html', {})

@transaction.commit_on_success
@login_required
def getActivitiesAddress(request):
  activities = Activity.objects.all()
  addresses = []
  for activity in activities:
    if activity.privacy == 0 or activity.user==request.user or request.user in activity.user.get_friends():#if it is a public or is post by this user or this user is holder's friend
      addresses.append(activity.address)

  return HttpResponse(json.JSONEncoder().encode(addresses))#encode dictionaries to json for javascript

@transaction.commit_on_success
@login_required
def getActivityIntroductions(request):
  activities = Activity.objects.all()
  introductions = []
  for activity in activities:
    content = {};
    content["briefintro"] = "<p style='font-weight:bold'>"+'<img src="/static/pictures/'+activity.activitytype \
                             +'.png") style="max-height:30px;max-width:30px;">&nbsp&nbsp&nbsp'                      \
                             +activity.name + "</p><p>" + "Time: " + activity.time.strftime("%a, %d %b %Y %H:%M") + "</p><p>"  \
                             + "Location: " + activity.address + "</p>";
    content["detaillink"] = "activitydetail/"+str(activity.id);
    introductions.append(content);
  return HttpResponse(json.JSONEncoder().encode(introductions))

@login_required
@transaction.commit_on_success
def get_feedbackphoto(request, id):
    feedback = get_object_or_404(Feedback, id=id)
    if not feedback.picture:
        raise Http404
    content_type = guess_type(feedback.picture.name)
    return HttpResponse(feedback.picture, mimetype=content_type)


@transaction.commit_on_success
@login_required
def activitydetail(request,id):
  activity = Activity.objects.get(id = id);
  feedbacks = Feedback.objects.filter(activity__id = id);
  context = {"activity":activity, "feedbacks": feedbacks, "user":request.user};
  return render(request, 'activitydetail.html', context)


@transaction.commit_on_success
@login_required
def addfeedback(request,id):
    print("1")
    if (not request.POST['text'] or not 'text' in request.POST) and (not 'picture' in request.FILES or not request.FILES['picture']):
        print("2")
        return redirect('/activitydetail/'+id)
    activity = Activity.objects.get(id=id)
    new_feedback = Feedback.objects.create(user=request.user, activity = activity)
    if request.POST['text'] and 'text' in request.POST:
        text = request.POST['text']
        new_feedback.text = text
    if 'picture' in request.FILES and request.FILES['picture']:
        new_feedback.picture = request.FILES['picture']
    new_feedback.save();
    return redirect('/activitydetail/'+id)

@login_required
def get_unread_messages(request):
  '''
  unreadmessages_dic: a dictionary store all unread message informations
  activities : a list that store all unread activities, its elements are a dic: {ID: name}
  activity : an activity get from database
  activity_dic : activities'e element, in the form of {ID: name}
  '''
  unreadmessages_dic = {}
  activities = []
  uncomfirmedfriends = []
  for unread_activity in UnreadActivityInvitation.objects.filter(user=request.user):
    activity = Activity.objects.get(id=unread_activity.activityID)
    activities.append((activity.id, activity.name))

  userself = UserFollowers.objects.get(user = request.user)
  allfriends = UnConfirmedFriend.objects.filter(confirmuser = userself)
  for friend in allfriends:
    uncomfirmedfriend_dic = {}
    uncomfirmedfriend_dic["requestfriendname"] = friend.requestuser.info.firstname+" "+friend.requestuser.info.lastname
    uncomfirmedfriend_dic["unConfirmID"] = friend.id;
    uncomfirmedfriend_dic["requestfriendid"] = friend.requestuser.id;
    uncomfirmedfriends.append(uncomfirmedfriend_dic)

  #nearby activity
  nearbyActivities = []
  for activity in Activity.objects.all():
    #If this activity has been ignored
    if IgnoredNearByActivity.objects.filter(user = request.user, activityID = activity.id):
      continue
    #If activity is private
    if activity.privacy == 1:
      continue
    #If activity is posted by this user
    if activity.user == request.user:
      continue
    userLocation = UserLocation.objects.filter(user = request.user)
    #If user has no location information
    if not userLocation:
      continue
    #If activity has no location information
    userLocation = userLocation[0]
    if activity.lat == 0 or activity.lng == 0:
      continue
    #IF this activity is too far away
    if getdistance(userLocation.lat, userLocation.lng, activity.lat, activity.lng) > 2:
      continue
    nearbyActivities.append((activity.id, activity.name))

  unreadmessages_dic['activities'] = activities
  unreadmessages_dic['uncomfirmedfriends'] = uncomfirmedfriends
  unreadmessages_dic['nearbyActivities'] = nearbyActivities
  return HttpResponse(json.JSONEncoder().encode(unreadmessages_dic))#encode dictionaries to json for javascript

#A helper function to calculate distance
def getdistance(lat1,lng1,lat2,lng2):
    EARTH_RADIUS = 6378.137
    lat1rad=lat1*math.pi/180.0;
    lng1rad=lng1*math.pi/180.0;
    lat2rad=lat2*math.pi/180.0;
    lng2rad=lng2*math.pi/180.0;
    a=lat1rad-lat2rad;
    b=lng1rad-lng2rad;
    dis=2*EARTH_RADIUS*math.asin(math.sqrt(math.pow(math.sin(a/2),2)+math.cos(lat1rad)*math.cos(lat1rad)*math.pow(math.sin(b/2),2)))
    return dis


@transaction.commit_on_success
@login_required
def delete_unread_activity(request, id):
  activity = UnreadActivityInvitation.objects.get(user=request.user, activityID=id)
  if activity:
    activity.delete()
  return HttpResponse()

@login_required
def get_events(request):
  events = {}

  holding = []
  for activity in Activity.objects.filter(user = request.user):
    holding.append((activity.id, activity.name, activity.time.strftime('%Y-%m-%dT%H:%M:%SZ')));

  following = []
  for follower in Followers.objects.filter(user = request.user):
    activity = follower.activity
    following.append((activity.id, activity.name, activity.time.strftime('%Y-%m-%dT%H:%M:%SZ')));

  events['holding'] = holding;
  events['following'] = following
  return HttpResponse(json.JSONEncoder().encode(events))

@transaction.commit_on_success
@login_required
def ignore_activity(request, id):
  IgnoredNearByActivity.objects.create(user = request.user, activityID = id).save();
  return HttpResponse()



