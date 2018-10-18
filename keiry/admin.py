# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Config)
admin.site.register(TaxRate)
admin.site.register(BusinessAcount)
admin.site.register(Item)
admin.site.register(GCItem)
admin.site.register(Segment)
admin.site.register(Journal)

