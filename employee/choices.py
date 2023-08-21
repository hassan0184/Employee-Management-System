from django.db import models
from django.utils.translation import gettext as _

class EmployeeStatus(models.TextChoices):
    PERMANENT = 'Permanent', _('Permanent')
    PROBATION = 'Probation', _('Probation')
    INTERN = 'Intern', _('Intern')
class AttendenceStatus(models.TextChoices):
    PRESENT = 'Present', _('Present')
    ABSENT = 'Absent', _('Absent')
    LATE = 'Late', _('Late')
    SICK_LEAVE = 'Sick Leave', _('Sick Leave')
    CASUAL_LEAVE = 'Casual Leave', _('Casual Leave')
    WFH = 'WFH', _('WFH')