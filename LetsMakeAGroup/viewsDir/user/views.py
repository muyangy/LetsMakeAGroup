from LetsMakeAGroup.models import *
from django.shortcuts import render, redirect
# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

from django.db import transaction

from django.http import HttpResponse
import json


@login_required
@transaction.commit_on_success
def follow(request, id):
    try:
      newfriend = User.objects.get(id=id)
    except:
      return render(request,"pagenotfound.html")
    user = request.user
    relationself = UserFollowers.objects.get(user = user)
    relationfriend = UserFollowers.objects.get(user = newfriend)
    allfriends = relationself.friends.all();
    if newfriend in allfriends:
        relationself.friends.remove(newfriend)
        relationfriend.friends.remove(user)
    else:
        newunconfirm = UnConfirmedFriend(requestuser = user, user = newfriend);
        newunconfirm.save();
     #   relationself.friends.add(newfriend);
     #   relationfriend.friends.add(user);
    return redirect("/personalhome/"+id)

@login_required
@transaction.commit_on_success
def confirmfriendrequest(request, id):
    try:
        unconfirmed = UnConfirmedFriend.objects.get(id=id)
    except:
        return render(request,"pagenotfound.html")
    confirmuser = unconfirmed.user
    requestuser = unconfirmed.requestuser
    confirmuserrelation = UserFollowers.objects.get(user = confirmuser)
    requestuserrelation = UserFollowers.objects.get(user = requestuser)
    confirmuserrelation.friends.add(requestuser)
    requestuserrelation.friends.add(confirmuser)
    unconfirmed.delete()
    return HttpResponse()

@login_required
@transaction.commit_on_success
def refusefriend(request, id):
    try:
        unconfirmed = UnConfirmedFriend.objects.get(id=id)
    except:
        return render(request,"pagenotfound.html")
    unconfirmed.delete()
    return HttpResponse()

@login_required
@transaction.commit_on_success
def reset_password(request):
    if request.method == 'GET':
        return render(request, 'reset_password.html',{})

    if request.method == 'POST':
        feedback = []
        context = {}

        #Any input missing
        if not 'current_password' in request.POST or not request.POST['current_password']:
            feedback.append('Current password is required.')
        if not 'new_password1' in request.POST or not request.POST['new_password1']:
            feedback.append('New password is required.')
        if not 'new_password2' in request.POST or not request.POST['new_password2']:
            feedback.append('New password confirm is required.')
        #Password do not match
        if 'new_password1' in request.POST and 'new_password2' in request.POST \
        and request.POST['new_password1'] and request.POST['new_password2'] \
        and request.POST['new_password1'] != request.POST['new_password2']:
            feedback.append('New passwords did not match.')

        new_user = authenticate(username=request.user.username, password=request.POST['current_password'])
        if not new_user:
            feedback.append("Current password is wrong");

        #if anything wrong
        if feedback:
            context['feedback'] = feedback
            return render(request, 'reset_password.html',context)

        else:
            feedback.append("Password Changed!")
            new_user.set_password(request.POST['new_password1']);
            new_user.save();

        context['feedback'] = feedback
        return render(request, 'reset_password.html',context)

@login_required
def allUser(request):
    context = {}
    activity_users = User.objects.filter(is_active = True)
    people = Info.objects.filter(user__in = activity_users)
    unconfirmed = [];
    context['peoples'] = people

    friends = request.user.get_friends()
    friendsrequests = UnConfirmedFriend.objects.filter(requestuser = request.user)
    for relation in friendsrequests:
        unconfirmed.append(relation.user);
    context['unconfirmed'] = unconfirmed;
    for other_user in people:
        if other_user.user in friends:
            context['addfriendtext' + str(other_user.id)] = "Add Friend"
        else:
            context['addfriendtext' + str(other_user.id)] = "UnFriend"

    return render(request, 'people.html', context)

'''
@login_required
@transaction.commit_on_success
def update_user_location(request):
    print "foo"
    #if missing location information
    if not 'lat' in request.POST or not request.POST['lat']:
        return HttpResponse(1)

    if not 'lng' in request.POST or not request.POST['lng']:
        return HttpResponse(1)

    if UserLocation.objects.filter(user = request.user):
        userLocation = UserLocation.objects.get(user = request.user)
        userLocation.lat = request.POST['lat']
        userLocation.lng = request.POST['lng']
    else:
        UserLocation.objects.create(user = request.user,
                                    lat = request.POST['lat'],
                                    lng = request.POST['lng']).save()

    return HttpResponse(0)
'''


@login_required
@transaction.commit_on_success
def update_user_location(request):
    #if missing location information
    if not 'lat' in request.GET or not request.GET['lat']:
        return HttpResponse(1)

    if not 'lng' in request.GET or not request.GET['lng']:
        return HttpResponse(1)

    if UserLocation.objects.filter(user = request.user):

        userLocation = UserLocation.objects.get(user = request.user)
        userLocation.lat = request.GET['lat']
        userLocation.lng = request.GET['lng']
    else:
        UserLocation.objects.create(user = request.user,
                                    lat = request.GET['lat'],
                                    lng = request.GET['lng']).save()

    return HttpResponse(0)


#!Don't delete it, use as testing function!
@login_required
def getFriends(request):
    friends = request.user.user_friends()
    return HttpResponse(json.JSONEncoder().encode(friends))