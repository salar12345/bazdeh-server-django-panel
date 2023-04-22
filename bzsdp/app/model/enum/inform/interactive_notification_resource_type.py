from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class InteractiveNotificationResourceType(TextChoices):
    NEWS = 'NEWS', _('News')
    ANALYSIS = 'ANALYSIS', _('Analysis')
