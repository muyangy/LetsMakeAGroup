from django.shortcuts import render, redirect, get_object_or_404
from LetsMakeAGroup.models import *
# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required
# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import transaction
from mimetypes import guess_type
from django.http import HttpResponse, Http404

@transaction.commit_on_success
@login_required
def index(request):
    activities = Activity.objects.all();
    for activity in activities:
       if activity.privacy==1 :
            posterfriends = activity.user.get_friends();
            if request.user not in posterfriends and request.user != activity.user:
               thisid = activity.id
               activities = activities.exclude(id = thisid)
    context = {"activities":activities}
    return render(request, 'index.html', context)

def search(request):
    context = {}
    activities = []
    if 'search_query' in request.GET and request.GET['search_query']:
        activities = Activity.objects.filter(name__contains = request.GET['search_query'])

    for activity in activities:
       if activity.privacy==1 :
            posterfriends = activity.user.get_friends();
            if request.user not in posterfriends and request.user != activity.user:
               thisid = activity.id
               activities = activities.exclude(id = thisid)
    context = {"activities":activities}
    return render(request, 'index.html', context)


@login_required
@transaction.commit_on_success
def get_activityphoto(request, id):
    activity = get_object_or_404(Activity, id=id)
    if not activity.picture:
        raise Http404
    content_type = guess_type(activity.picture.name)
    return HttpResponse(activity.picture, mimetype=content_type)


@login_required
@transaction.commit_on_success
def get_infophoto(request, id):
    info = get_object_or_404(Info, id=id)
    if not info.picture:
        raise Http404
    content_type = guess_type(info.picture.name)
    return HttpResponse(info.picture, mimetype=content_type)


@login_required
@transaction.commit_on_success
def join(request, id):
    activity = Activity.objects.get(id=id)
    if(request.user == activity.user):
      return redirect("/")
    oldfollower = Followers.objects.filter(user=request.user,activity = activity)
    if(not oldfollower):
      newfollower = Followers(user=request.user,activity = activity)
      newfollower.save()
    return redirect("/")

@login_required
@transaction.commit_on_success
def personalhome(request, id):
    pageowner = User.objects.get(id=id)
    organized = []
    activities = Activity.objects.filter(user=pageowner)
    for activity in activities:
        if activity.privacy==0 or activity.user==request.user or request.user in activity.user.get_friends():
            organized.append(activity)

    participated = []
    followers = Followers.objects.filter(user=pageowner)
    for follower in followers:
        if follower.activity.privacy==0 or follower.activity.user==request.user:
            participated.append(follower.activity)
    if request.user == pageowner:
        context = {"pageowner":pageowner, "organized":organized, "participated":participated }
        return render(request, 'home.html', context)
    otherpage = 1;
    friendsrequests = UnConfirmedFriend.objects.filter(requestuser = request.user).filter(confirmuser = pageowner)

    if friendsrequests:
        addsent = "1"
    else:
        addsent = "0"
    if pageowner not in request.user.get_friends():
        addfriendtext = "Add Friend"
    else:
        addfriendtext = "Unfriend"
    context = {"pageowner":pageowner, "addfriendtext": addfriendtext, "otherpage": otherpage, "organized":organized, "participated":participated, "addsent": addsent}
    return render(request, 'home.html', context)

@login_required
@transaction.commit_on_success
def comment(request, id):
    if not 'comment' in request.POST or not request.POST['comment']:
        return redirect(reverse('index'))

    activity = Activity.objects.filter(id=id)[0]
    comment = Comment(text=request.POST['comment'], activity=activity, commenter=request.user)
    comment.save()
    return redirect(reverse('index'));



