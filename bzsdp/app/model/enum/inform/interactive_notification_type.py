from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class InteractiveNotificationType(TextChoices):
    COMMENT_UP_VOTE = 'COMMENT_UP_VOTE', _('Comment up vote')
    COMMENT_MENTION = 'COMMENT_MENTION', _('Comment mention')
    COMMENT_REPLY = 'COMMENT_REPLY', _('Comment reply')
    RIGHT_GAME_VOTE = 'RIGHT_GAME_VOTE', _('Right game vote')
    WRONG_GAME_VOTE = 'WRONG_GAME_VOTE', _('Wrong game vote')
