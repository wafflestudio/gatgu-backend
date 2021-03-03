from django.db import models
from django.contrib.auth.models import User
from article.models import Article


class OrderChat(models.Model):
    participants = models.ManyToManyField(
        User,
        through='ParticipantProfile',
        through_fields=('order', 'participant'),
    )
    article = models.OneToOneField(
        Article,
        on_delete=models.CASCADE,
        related_name='order_chat'
    )
    order_status = models.CharField(max_length=30)
    tracking_number = models.CharField(max_length=30)

    '''participants.count로 대체'''
    # cur_people = models.IntegerField()


class ChatMessage(models.Model):
    text = models.TextField(null=True)
    sent_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sent_at = models.DateTimeField(auto_now=True)
    chat = models.ForeignKey(
        OrderChat,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    media = models.URLField(null=True)
    type = models.CharField(max_length=30)


class ParticipantProfile(models.Model):
    order = models.ForeignKey(
        OrderChat,
        on_delete=models.CASCADE,
        related_name='participant_profile',
    )
    participant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='participant_profile',
    )
    joined_at = models.DateTimeField(auto_now=True)
    out_at = models.DateTimeField(null=True)
    pay_status = models.CharField(max_length=30)
    wish_price = models.IntegerField(null=True)

    class Meta:
        unique_together = (
            ('order', 'participant')
        )
