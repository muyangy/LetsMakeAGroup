from django.conf.urls import patterns, include, url
from LetsMakeAGroup.viewsDir.signin_up import views
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'LetsMakeAGroup.viewsDir.index.views.index', name='index'),
    url(r'^post_newactivity$', 'LetsMakeAGroup.viewsDir.acivity.views.post_activity', name='new_activity'),
    url(r'^signup.html$','LetsMakeAGroup.viewsDir.signin_up.views.signup', name = 'signup'),
    # url(r'^signin.html$', 'LetsMakeAGroup.viewsDir.signin_up.views.signin', name='signin'),
    url(r'^resetpassword_signin.html$', 'LetsMakeAGroup.viewsDir.signin_up.views.resetpassword_signin', name='resetinsignin'),
    url(r'^signin.html$', 'django.contrib.auth.views.login', {'template_name':'signin.html'}, name = 'signin'),
    url(r'^signout.html$', 'django.contrib.auth.views.logout_then_login', name = 'signout'),
    url(r'^activityphoto/(?P<id>\d+)$', 'LetsMakeAGroup.viewsDir.index.views.get_activityphoto', name='activityphoto'),
    url(r'^feedbackphoto/(?P<id>\d+)$', 'LetsMakeAGroup.viewsDir.acivity.views.get_feedbackphoto', name='feedbackphoto'),
    url(r'^infophoto/(?P<id>\d+)$', 'LetsMakeAGroup.viewsDir.index.views.get_infophoto', name='infophoto'),
    url(r'^getActivitiesAddress', 'LetsMakeAGroup.viewsDir.acivity.views.getActivitiesAddress'),
    url(r'^getActivityIntroduction', 'LetsMakeAGroup.viewsDir.acivity.views.getActivityIntroductions'),
    url(r'^activitydetail/(?P<id>\d+)$', 'LetsMakeAGroup.viewsDir.acivity.views.activitydetail', name='activitydetail'),
    url(r'^addfeedback/(?P<id>\d+)$', 'LetsMakeAGroup.viewsDir.acivity.views.addfeedback', name='addfeedback'),
    url(r'^join/(?P<id>\d+)$', 'LetsMakeAGroup.viewsDir.index.views.join', name='join'),
    url(r'^personalhome/(?P<id>\d+)$', 'LetsMakeAGroup.viewsDir.index.views.personalhome', name='personalhome'),
    url(r'^comment/(?P<id>\d+)$', 'LetsMakeAGroup.viewsDir.index.views.comment', name='comment'),
    url(r'^reset_password$', 'LetsMakeAGroup.viewsDir.user.views.reset_password', name='reset_password'),
    url(r'^follow/(?P<id>\d+)$', 'LetsMakeAGroup.viewsDir.user.views.follow', name='follow'),
    url(r'^getFriends$', 'LetsMakeAGroup.viewsDir.user.views.getFriends', name='getFriends'),
    url(r'^people$', 'LetsMakeAGroup.viewsDir.user.views.allUser', name='people'),
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@.\+\-]+)/(?P<token>[a-z0-9\-]+)$', 'LetsMakeAGroup.viewsDir.signin_up.views.confirm_registration', name='confirm'),
    url(r'^forgetpassword$', 'LetsMakeAGroup.viewsDir.signin_up.views.forget_password', name='forgetpassword'),
    url(r'^getbackpassword/(?P<username>[a-zA-Z0-9_@.\+\-]+)/(?P<token>[a-z0-9\-]+)$', 'LetsMakeAGroup.viewsDir.signin_up.views.getbackpassword', name='getbackpassword'),
    url(r'^resetpassword$', 'LetsMakeAGroup.viewsDir.signin_up.views.resetpassword', name='resetpassword'),
    url(r'^get_unread_messages$', 'LetsMakeAGroup.viewsDir.acivity.views.get_unread_messages'),
    url(r'^delete_unread_activity/(?P<id>\d+)$', 'LetsMakeAGroup.viewsDir.acivity.views.delete_unread_activity'),
    url(r'^confirmfriendrequest/(?P<id>\d+)$', 'LetsMakeAGroup.viewsDir.user.views.confirmfriendrequest'),
    url(r'^refusefriend/(?P<id>\d+)$', 'LetsMakeAGroup.viewsDir.user.views.refusefriend'),
    url(r'^get_events$', 'LetsMakeAGroup.viewsDir.acivity.views.get_events'),
    url(r'^update_user_location$', 'LetsMakeAGroup.viewsDir.user.views.update_user_location'),
    url(r'^ignore_activity/(?P<id>\d+)$', 'LetsMakeAGroup.viewsDir.acivity.views.ignore_activity'),
    url(r'^search$', 'LetsMakeAGroup.viewsDir.index.views.search', name='search'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)