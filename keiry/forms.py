# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings

from .models import TaxRate, Item, GCItem, Segment

# JournalForm
class JournalForm(forms.Form):
    rec_date          = forms.DateField(
                          label=u'計上日' ,
                          required=True ,
                          widget=forms.DateInput(),
                          input_formats=settings.DATE_INPUT_FORMATS
                       )

    seq               = forms.CharField(
                          label=u'通番',
                          required=False ,
                          widget=forms.HiddenInput() ,
                          help_text=u'', 
                          initial=u''
                       )

    debit_item_id     = forms.ChoiceField(
                          label=u'借方' ,
                          required=True ,
                          widget=forms.Select,
                          choices=()       # 勘定マスタの内容をViewで動的に設定する
                       )
                       
    credit_item_id    = forms.ChoiceField(
                          label=u'貸方' ,
                          required=True ,
                          widget=forms.Select,
                          choices=()       # 勘定マスタの内容をViewで動的に設定する
                       )
                       
    amount_inc_tax    = forms.CharField(
                          label=u'金額(税込み)' ,
                          required=True ,
                          widget=forms.NumberInput() ,
                          help_text=u'', 
                          initial=u'0'
                       )

    tax               = forms.CharField(
                          label=u'消費税' ,
                          required=False ,
                          widget=forms.HiddenInput() ,
                          help_text=u'', 
                          initial=u''
                       )
                       
    tax_type          = forms.ChoiceField(
                          label=u'税区分' ,
                          required=True ,
                          widget=forms.Select,
                          choices=()       # 税率マスタの内容をViewで動的に設定する
                       )
                       
    remark            = forms.CharField(
                          label=u'摘要' ,
                          max_length=256 ,
                          required=True ,
                          widget=forms.TextInput(),
                          help_text=u'', 
                          initial=u''
                       )

    description       = forms.CharField(
                          label=u'説明' ,
                          max_length=256 ,
                          required=False ,
                          widget=forms.Textarea(attrs={'cols':'50', 'rows':'10'}) ,
                          help_text=u'', 
                          initial=u''
                       )

    gc_item_id        = forms.ChoiceField(
                          label=u'販管費目' ,
                          required=False ,
                          widget=forms.Select,
                          choices=()       # 販管費勘定マスタの内容をViewで動的に設定する
                       )

    cash_io           = forms.CharField(
                          label=u'現金増減' ,
                          required=False ,
                          widget=forms.NumberInput() ,
                          help_text=u'', 
                          initial=u'0'
                       )

    voucher_no         = forms.CharField(
                          label=u'伝票No' ,
                          required=False ,
                          widget=forms.TextInput() ,
                          help_text=u'', 
                          initial=u''
                       )

    debt_no           = forms.CharField(
                          label=u'債務No' ,
                          required=False ,
                          widget=forms.TextInput(),
                          help_text=u'', 
                          initial=u''
                       )

    credit_no         = forms.CharField(
                          label=u'債権No' ,
                          required=False ,
                          widget=forms.TextInput() ,
                          help_text=u'', 
                          initial=u''
                       )

    order_no          = forms.CharField(
                          label=u'契約No' ,
                          required=False ,
                          widget=forms.TextInput() ,
                          help_text=u'', 
                          initial=u''
                       )

    seg_id           = forms.ChoiceField(
                          label=u'セグメント' ,
                          required=False ,
                          widget=forms.Select,
                          choices=()       # セグメントマスタの内容をViewで動的に設定する
                       )

    closed_date      = forms.DateField(
                          label=u'締め日' ,
                          required=False ,
                          widget=forms.DateInput()
                       )

    # https://stackoverflow.com/questions/18531970/override-the-initialization-of-a-choicefield-in-django
    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)

        # 税率選択メニュー設定
        tax_rate_choice_list = []
        for q in list(TaxRate.objects.filter(displayed=True).order_by('type')):
            tax_rate_choice_list.append( ( q.type, q.name ) )

        self.fields['tax_type'].choices = tuple(tax_rate_choice_list)

        # 勘定ID選択メニュー設定
        item_choice_list = [('', u'------'),]
        for q in list(Item.objects.filter(displayed=True).order_by('item_id')):
           item_choice_list.append( ( q.item_id, q.name_jp ) )

        self.fields['debit_item_id'].choices  = tuple(item_choice_list)
        self.fields['credit_item_id'].choices = tuple(item_choice_list)

        # 販管費勘定ID選択メニュー設定
        gc_item_choice_list = [('', u'------'),]
        for q in list(GCItem.objects.filter(displayed=True).order_by('item_id')):
           gc_item_choice_list.append( ( q.item_id, q.name_jp ) )

        self.fields['gc_item_id'].choices = tuple(gc_item_choice_list)

        # セグメント選択メニュー設定
        segment_choice_list = []
        for q in list(Segment.objects.filter(displayed=True).order_by('seg_id')):
           segment_choice_list.append( ( q.seg_id, q.name_jp ) )

        self.fields['seg_id'].choices = tuple(segment_choice_list)
