from django.db import models
from django.utils.translation import gettext as _

class ExtraTimeStatus(models.TextChoices):
    PENDING = "0", _('PENDING')
    APPROVED = "1", _('APPROVED')