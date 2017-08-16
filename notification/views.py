from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from notification.models import Notification
from projet3.decorators import ajax_required


@login_required
def notifications(request):
    user = request.user
    notifications = Notification.objects.filter(to_user=user)
    
    unread = Notification.objects.filter(to_user=user, is_read=False)
    for notification in unread:
        notification.is_read = True
        notification.save()

    return render(request, 'notification/notifications.html',
                  {'notifications': notifications})


@login_required
@ajax_required
def last_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(to_user=user,
                                                is_read=False)[:5]
    print(notifications)
    for notification in notifications:
        notification.is_read = True
        notification.save()

    return render(request,
                  'notification/last_notifications.html',
                  {'notifications': notifications})


@login_required
@ajax_required
def check_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(to_user=user,
                                                is_read=False)[:5]
    # print(notifications)
    return HttpResponse(len(notifications))
    # return HttpResponse(0)
