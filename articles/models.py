from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Article(models.Model):
    id = models.AutoField(primary_key=True)
    heading = models.CharField(
                  _('heading'),
                  null=True,
                  blank=True,
                  max_length=250
    )
    body    = models.TextField(
                  _('body'),
                  null=True,
                  blank=True,
    )
