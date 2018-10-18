from django import template
from keiry.models import Config
from django.urls import reverse

register = template.Library()

# {{field|addcss:"form-control"}} for bootstrap 3
@register.filter(name='addcss')
def addcss(field, css):
   return field.as_widget(attrs={"class":css})

# simple_tag
@register.simple_tag
def company_name():
   return Config.objects.get(pk='00').param

# 今期決算開始日
@register.simple_tag
def this_fy_fm():
   return Config.objects.get(pk='01').param

# 今期決算終了日
@register.simple_tag
def this_fy_to():
   return Config.objects.get(pk='02').param

# 今期のkeiry_journalのurl
@register.simple_tag
def keiry_journal_url_this_year():
   return reverse('journal', args=(this_fy_fm(), this_fy_to(), ))

# 前期の決算開始日
@register.simple_tag
def last_fy_fm():
   return Config.objects.get(pk='03').param

# 前期の決算終了日
@register.simple_tag
def last_fy_to():
   return Config.objects.get(pk='04').param


