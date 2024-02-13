from django.db import models
from django.utils.translation import gettext_lazy as _

class JenisPertanyaan(models.TextChoices) :
    LIKERT = "LIKERT", _('Likert')
    TEXT = "TEXT", _('Text')