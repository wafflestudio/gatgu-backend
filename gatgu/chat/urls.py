from django.urls import path, include
from rest_framework.routers import SimpleRouter
from chat.views import OrderChatViewSet, ChatMessageViewSet

router = SimpleRouter()
router.register('chattings', OrderChatViewSet, basename='chatttings')
router.register('message', ChatMessageViewSet, basename='message')

urlpatterns = [
    path('', include((router.urls)))
]

'''urlpatterns = [
    path('', views.chats, name='chats'),
    path('<int:chat_id>/', views.chat, name='chat'),
    path('<int:chat_id>/join/', views.join, name='join'),
    path('<int:chat_id>/out/', views.out, name='out'),
    path('<int:chat_id>/messages/', views.messages, name='messages'),
    path('message/<int:message_id>/', views.message, name='message'),
    path('<int:chat_id>/participants/', views.participants, name='participants'),

    path('<int:chat_id>/set_status/', views.set_status, name='set_status'),
    path('<int:chat_id>/set_buy_amount/', views.set_buy_amount, name='set_buy_amount'),
    path('<int:chat_id>/paid/', views.paid, name='paid')

]'''