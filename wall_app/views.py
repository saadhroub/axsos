from datetime import datetime, timezone
from django.shortcuts import render, redirect
from .models import Message, Comment
from login_registration_app.models import User
import pytz


def post_message(request, userid):
    user_id = int(userid)
    this_user = User.objects.get(id=user_id)
    Message.objects.create(
        message=request.POST['message'], user=this_user)
    return redirect('/dojo_wall/wall')


def post_comment(request, message_id, userid):
    user_id = int(userid)
    message_ID = int(message_id)
    this_message = Message.objects.get(id=message_ID)
    this_user = User.objects.get(id=user_id)
    Comment.objects.create(
        comment=request.POST['comment'], user=this_user, message=this_message)
    return redirect('/dojo_wall/wall')


def wall(request):
    if 'userid' in request.session:
        user = User.objects.get(id=int(request.session['userid']))
        if user:
            context = {
                'first_name': user.first_name,
                'messages': Message.objects.all().order_by('-created_at')
            }
            return render(request, 'wall.html', context)
        else:
            return redirect('/')
    else:
        return redirect('/')


def delete_message(request, message_id):
    message_ID = int(message_id)
    message_to_delete = Message.objects.get(id=message_ID)
    diff = datetime.now(timezone.utc)-message_to_delete.created_at
    diff_in_seconds = diff.seconds
    minutes = diff_in_seconds/60
    print(minutes)
    if message_to_delete.user.id == request.session['userid'] and minutes < 30:

        message_to_delete.delete()

    return redirect('/dojo_wall/wall')
