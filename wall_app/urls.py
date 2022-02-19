from django.urls import path
from . import views


urlpatterns = [
    path('wall', views.wall),
    path('post_message/<userid>', views.post_message),
    path('post_comment/<message_id>/<userid>', views.post_comment),
    path('delete_message/<message_id>', views.delete_message)
]
