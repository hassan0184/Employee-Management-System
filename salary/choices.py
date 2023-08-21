from django.db import models
from django.utils.translation import gettext as _


class AllowanceType(models.TextChoices):
    BONUS = "Bonus", _('Bonus')
    MEDICAL = "Medical", _('Medical')
    CAR_FINANCE = "Car Finance", _('Car Finance')
    EXTRA_HOURS = "Extra Hours", _('Extra Hours')
    HOME_ALLOWANCE = "House Allowance", _('House Allowance')
    OTHER = "Other", _('Other')


class DeductionType(models.TextChoices):
    TAX = "Tax", _('Tax')
    FINE = "Fine", _('Fine')
    LUNCH = "Lunch", _('Lunch')
    LATE = "Late", _('Late')
    ABSENT = "Absent", _('Absent')
    OTHER = "Other", _('Other')