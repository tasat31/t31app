# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

from django import forms
from django.forms import BaseFormSet
from django.forms import formset_factory

from .models import *

from .forms import *

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import datetime

from django.db.models import Sum, Max

# Create your views here.
@login_required
def index(request):
    
    context = {}

    return render(request,'keiry/index.html', context)

class BaseJournalFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)

        # 税率選択メニュー設定
        tax_rate_choice_list = []
        for q in list(TaxRate.objects.filter(displayed=True).order_by('type')):
            tax_rate_choice_list.append( ( q.type, q.name ) )

        form.fields['tax_type'].choices = tuple(tax_rate_choice_list)

        # 勘定ID選択メニュー設定
        item_choice_list = []
        for q in list(Item.objects.filter(displayed=True).order_by('item_id')):
            item_choice_list.append( ( q.item_id, q.name_jp ) )

        form.fields['debit_item_id'].choices  = item_choice_list
        form.fields['credit_item_id'].choices = item_choice_list

        # 販管費勘定ID選択メニュー設定
        gc_item_choice_list = [('','---'),]
        for q in list(GCItem.objects.filter(displayed=True).order_by('item_id')):
            gc_item_choice_list.append( ( q.item_id, q.name_jp ) )

        form.fields['gc_item_id'].choices = gc_item_choice_list

        # セグメント選択メニュー設定
        segment_choice_list = []
        for q in list(Segment.objects.filter(displayed=True).order_by('seg_id')):
            segment_choice_list.append( ( q.seg_id, q.name_jp ) )

        form.fields['seg_id'].choices = tuple(segment_choice_list)

@login_required
def journal(request, rec_date_fm, rec_date_to):
    
    ( year_fm, month_fm, day_fm ) = ( int(rec_date_fm[0:4]), int(rec_date_fm[4:6]), int(rec_date_fm[6:8]) )
    ( year_to, month_to, day_to ) = ( int(rec_date_to[0:4]), int(rec_date_to[4:6]), int(rec_date_to[6:8]) )
    
    journal_list = []
    try:
       query_journal = Journal.objects.filter(rec_date__gte=datetime.date(year_fm, month_fm, day_fm), rec_date__lte=datetime.date(year_to, month_to, day_to)).order_by('rec_date', 'seq')
       for q in query_journal:
           journal_list.append({
                               'rec_date'       : q.rec_date       ,
                               'seq'            : q.seq            ,
                               'debit_item_id'  : q.debit_item_id  ,
                               'credit_item_id' : q.credit_item_id ,
                               'amount_inc_tax' : q.amount_inc_tax ,
                               'tax'            : q.tax            ,
                               'remark'         : q.remark         ,
                               'tax_type'       : q.tax_type       ,
                               'description'    : q.description    ,
                               'gc_item_id'     : q.gc_item_id     ,
                               'cash_io'        : q.cash_io        ,
                               'voucher_no'     : q.voucher_no     ,
                               'debt_no'        : q.debt_no        ,
                               'credit_no'      : q.credit_no      ,
                               'order_no'       : q.order_no       ,
                               'seg_id'         : q.seg_id         ,
                               'closed_date'    : q.closed_date    ,
                              })

    except ( Journal.DoesNotExist ):
       pass

    JournalFormSet = formset_factory(JournalForm, formset=BaseJournalFormSet, extra=0)
    journal_formset = JournalFormSet(initial=journal_list)
    

    context = {
       'journal_formset'    : journal_formset , 
    }

    return render(request,'keiry/journal.html', context)

class JournalView(LoginRequiredMixin,View):
    # http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

    def dispatch(self, *args, **kwargs):
        if self.request.method == 'POST':
           method = self.request.POST.keys()
           if 'put' in method :
              return self.put(*args, **kwargs)
           if 'delete' in method:
              return self.delete(*args, **kwargs)

        return super(JournalView, self).dispatch(*args, **kwargs)

    #仕訳帳の表示(GET)
    def get(self, request, rec_date=None, seq=None):

       if ( ( rec_date is None ) or ( seq is None ) ):
          journal_form  = JournalForm(initial = {'rec_date' : None, 'seq': None } )
       else:
           ( rec_year, rec_month, rec_day ) = ( int(rec_date[0:4]), int(rec_date[4:6]), int(rec_date[6:8]) )

           try:
             query_journal = Journal.objects.get(rec_date=datetime.date(rec_year, rec_month, rec_day ), seq=int(seq))
             journal_form  = JournalForm(
                             initial = {
                               'rec_date'       : query_journal.rec_date       ,
                               'seq'            : query_journal.seq            ,
                               'debit_item_id'  : query_journal.debit_item_id  ,
                               'credit_item_id' : query_journal.credit_item_id ,
                               'amount_inc_tax' : query_journal.amount_inc_tax ,
                               'tax'            : query_journal.tax            ,
                               'remark'         : query_journal.remark         ,
                               'tax_type'       : query_journal.tax_type       ,
                               'description'    : query_journal.description    ,
                               'gc_item_id'     : query_journal.gc_item_id     ,
                               'cash_io'        : query_journal.cash_io        ,
                               'voucher_no'     : query_journal.voucher_no     ,
                               'debt_no'        : query_journal.debt_no        ,
                               'credit_no'      : query_journal.credit_no      ,
                               'order_no'       : query_journal.order_no       ,
                               'seg_id'         : query_journal.seg_id         ,
                               'closed_date'    : query_journal.closed_date    ,
                                       }
                                 )

             journal_form.fields['rec_date'].widget = forms.HiddenInput()

           except ( Journal.DoesNotExist ):
              journal_form  = JournalForm(initial = {'rec_date' : None, 'seq': None } )
 
       context = {
           'journal_form'    : journal_form    , 
        }

       return render(request,'keiry/journal_input.html', context)

    #仕訳帳の編集(POST)
    def post(self, request):
       journal_form = JournalForm(request.POST)
        
       if journal_form.is_valid():
          rec_date_str = journal_form.cleaned_data['rec_date'].strftime('%Y%m%d')

          if ( journal_form.cleaned_data['seq'] == '' ):
             q = Journal.objects.filter(rec_date=journal_form.cleaned_data['rec_date']).aggregate(Max('seq'))
             if ( q['seq__max'] is None ):
                seq = 1
             else:
                seq = q['seq__max'] + 1

          else:
             seq = journal_form.cleaned_data['seq']

          # 消費税の計算
          rate = TaxRate.objects.get(type=journal_form.cleaned_data['tax_type']).rate
          tax = int(float(journal_form.cleaned_data['amount_inc_tax']) - (float(journal_form.cleaned_data['amount_inc_tax']) / ( 1.0 + rate ) ) )

          query = Journal(
                      rec_date       = journal_form.cleaned_data['rec_date']            ,
                      seq            = seq                                              ,
                      debit_item_id  = journal_form.cleaned_data['debit_item_id']       ,
                      credit_item_id = journal_form.cleaned_data['credit_item_id']      ,
                      amount_inc_tax = int(journal_form.cleaned_data['amount_inc_tax']) ,
                      tax            = tax                                           ,
                      remark         = journal_form.cleaned_data['remark']         ,
                      tax_type       = journal_form.cleaned_data['tax_type']       ,
                      description    = journal_form.cleaned_data['description']    ,
                      gc_item_id     = journal_form.cleaned_data['gc_item_id']     ,
                      cash_io        = int(journal_form.cleaned_data['cash_io'])   ,
                      voucher_no     = journal_form.cleaned_data['voucher_no']     ,
                      debt_no        = journal_form.cleaned_data['debt_no']        ,
                      credit_no      = journal_form.cleaned_data['credit_no']      ,
                      order_no       = journal_form.cleaned_data['order_no']       ,
                      seg_id         = journal_form.cleaned_data['seg_id']         ,
                      closed_date    = journal_form.cleaned_data['closed_date']    ,
                  )
                  
          query.save()

          context = {
              'journal_form' : journal_form , 
          }

          return HttpResponseRedirect(reverse('journal_detail', args=(rec_date_str, seq, )))

       else:
          context = {
              'journal_form' : journal_form , 
          }

          return render(request,'keiry/journal_input.html', context)


    def put(self, request):
        pass

    #仕訳帳の削除(DELETE)
    def delete(self, request):
        journal_form = JournalForm(request.POST)
        
        if journal_form.is_valid():
           Journal.objects.filter(req_date=journal_form.cleaned_data['rec_date'], seq=journal_form.cleaned_data['seq']).delete()
        
        return HttpResponseRedirect(reverse('journal_input', args=(None,)))


@login_required
def items(request):
    items = list(Item.objects.all().values('item_id', 'name_jp', 'category_name_jp', 'description', 'displayed').order_by('item_id'))
     
    context = {
           'items'    : items    , 
    }

    return render(request,'keiry/items.html', context)

@login_required
def gcitems(request):
    gcitems = list(GCItem.objects.all().values('item_id', 'name_jp', 'description', 'displayed').order_by('item_id'))

    context = {
           'gcitems'    : gcitems    , 
    }

    return render(request,'keiry/gcitems.html', context)

