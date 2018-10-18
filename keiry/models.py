# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

# 各種設定用(Config) 
class Config(models.Model):
    key        = models.CharField(max_length=2, primary_key=True)
    param      = models.TextField()
    remark     = models.TextField()

    def __unicode__(self):
       return u'%s = %s' % ( self.key, self.remark )

# 税率マスタ(TaxRate) * 消費税率を設定する
class TaxRate(models.Model):
    type        = models.CharField(max_length=1, primary_key=True)  # 1. 消費税(通常), 2. 消費税(軽減税率)
    rate        = models.FloatField()                               # 例. 0.08
    name        = models.TextField()                                # 名称
    displayed   = models.BooleanField()                             # 表示/非表示

    def __unicode__(self):
       return u'%s = %s' % ( self.name, self.rate )

# 取引先マスタ
class BusinessAcount(models.Model):
    account_id       = models.CharField(max_length=5, primary_key=True)   # 取引先ID
    name_jp          = models.TextField()                                 # 名称(日本語)
    name_en          = models.TextField()                                 # 名称(英語)
    person_name      = models.TextField()                                 # 担当者名
    person_postal_no = models.TextField()                                 # 担当者郵便番号
    person_address   = models.TextField()                                 # 担当者住所
    person_tel_1     = models.TextField()                                 # 担当者TEL1
    person_tel_2     = models.TextField()                                 # 担当者TEL2
    person_mail      = models.TextField()                                 # 担当者Mai
    homepage_url     = models.TextField()                                 # 会社HP_URL
    corporate_no     = models.TextField()                                 # 法人番号
    bank_name        = models.TextField()                                 # 口座情報・銀行名
    branch_name      = models.TextField()                                 # 口座情報・支店名
    stock_cat        = models.TextField()                                 # 口座情報・預金区分
    bank_account_no  = models.TextField()                                 # 口座情報・番号
    holder_name      = models.TextField()                                 # 口座情報・名義
    description      = models.TextField()                                 # 説明
    ins_date         = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    upd_date         = models.DateTimeField(auto_now=True)

    def __unicode__(self):
      return u'%s %s' % (self.account_id, self.name_jp)
    
# 勘定マスタ
class Item(models.Model):
    item_id          = models.CharField(max_length=4, primary_key=True)   # 勘定ID
    name_jp          = models.TextField()                                 # 名称(日本語)
    name_en          = models.TextField()                                 # 名称(英語)
    category         = models.TextField()                                 # 分類
    category_name_jp = models.TextField()                                 # 分類名(日本語)
    category_name_en = models.TextField()                                 # 分類名(英語)
    description      = models.TextField()                                 # 説明
    displayed        = models.BooleanField()                              # 表示/非表示
    ins_date         = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    upd_date         = models.DateTimeField(auto_now=True)

    def __unicode__(self):
      return u'%s %s' % (self.item_id, self.name_jp)

# 販管費勘定マスタ
class GCItem(models.Model):
    item_id          = models.CharField(max_length=3, primary_key=True)   # 勘定ID
    name_jp          = models.TextField()                                 # 名称(日本語)
    name_en          = models.TextField()                                 # 名称(英語)
    description      = models.TextField()                                 # 説明
    displayed        = models.BooleanField()                              # 表示/非表示
    ins_date         = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    upd_date         = models.DateTimeField(auto_now=True)

    def __unicode__(self):
       return u'%s %s' % (self.item_id, self.name_jp)

# セグメントマスタ
class Segment(models.Model):
    seg_id           = models.CharField(max_length=2, primary_key=True)   # セグメントID
    name_jp          = models.TextField()                                 # 名称(日本語)
    name_en          = models.TextField()                                 # 名称(英語)
    description      = models.TextField()                                 # 説明
    displayed        = models.BooleanField()                              # 表示/非表示
    ins_date         = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    upd_date         = models.DateTimeField(auto_now=True)

    def __unicode__(self):
       return u'%s %s' % (self.seg_id, self.name_jp)

# 仕訳帳
class Journal(models.Model):
    rec_date         = models.DateField()                                 # 計上日
    seq              = models.IntegerField()                              # 通番
    debit_item_id    = models.TextField()                                 # 借方・勘定ID
    credit_item_id   = models.TextField()                                 # 貸方・勘定ID
    amount_inc_tax   = models.IntegerField()                              # 金額(税込)
    tax              = models.IntegerField()                              # 消費税
    remark           = models.TextField()                                 # 摘要
    tax_type         = models.CharField(max_length=1)                     # 税区分
    description      = models.TextField()                                 # 説明
    gc_item_id       = models.TextField(null=True, blank=True)            # 販管費勘定ID
    cash_io          = models.IntegerField(null=True, blank=True)         # 現金増減
    voucher_no       = models.TextField(null=True, blank=True)            # 伝票No
    debt_no          = models.TextField(null=True, blank=True)            # 債務No
    credit_no        = models.TextField(null=True, blank=True)            # 債権No
    order_no         = models.TextField(null=True, blank=True)            # 契約No
    seg_id           = models.TextField(null=True, blank=True)            # セグメントID
    closed_date      = models.DateField(null=True, blank=True)            # 締め年月
    ins_date         = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    upd_date         = models.DateTimeField(auto_now=True)

    #https://stackoverflow.com/questions/2201598/how-to-define-two-fields-unique-as-couple
    class Meta:
       unique_together = ('rec_date', 'seq',)

    def __unicode__(self):
       return u'%s %d' % (self.rec_date.strftime("%Y%m%d"), self.seq)

class Sales(models.Model):
    mgt_no                     = models.CharField(max_length=18, primary_key=True) # 売上管理No
    subject                    = models.TextField()                                # 件名
    customer_id                = models.TextField()                                # 客先ID
    quote_no                   = models.TextField(null=True, blank=True)           # 見積No
    quote_issue_date           = models.DateField(null=True, blank=True)           # 見積発行日
    quote_delv_date            = models.DateField(null=True, blank=True)           # 見積納期
    quote_price_not_inc_tax    = models.IntegerField(null=True, blank=True)        # 見積金額(税抜)
    quote_tax                  = models.IntegerField(null=True, blank=True)        # 見積金額(消費税)
    order_no                   = models.TextField(null=True, blank=True)           # 契約No
    order_date                 = models.DateField(null=True, blank=True)           # 契約日
    order_delv_date            = models.DateField(null=True, blank=True)           # 契約納期
    price_not_inc_tax          = models.IntegerField(null=True, blank=True)        # 契約金額(税抜)
    tax                        = models.IntegerField(null=True, blank=True)        # 契約金額(消費税)
    tax_type                   = models.CharField(max_length=1)                    # 税区分
    contract_conditions        = models.TextField(null=True, blank=True)           # 契約条件
    latest_proposal_date       = models.DateField(null=True, blank=True)           # 検収依頼日(最新)
    total_appr_price_inc_tax   = models.IntegerField(null=True, blank=True)        # 検収金額(累計・税込み)
    total_left_price_inc_tax   = models.IntegerField(null=True, blank=True)        # 未検収金額(累計・税込み)
    approve_conditions         = models.TextField(null=True, blank=True)           # 検収条件
    latest_recept_date         = models.DateField(null=True, blank=True)           # 入金日(最新)
    total_recept_price_inc_tax = models.IntegerField(null=True, blank=True)        # 入金額(累計・税込み)
    next_recept_date           = models.DateField(null=True, blank=True)           # 入金予定日(最新)
    recept_conditions          = models.TextField(null=True, blank=True)           # 入金条件
    receivable_price_inc_tax   = models.IntegerField(null=True, blank=True)        # 未回収額(累計・税込み)
    order_canceled             = models.BooleanField()                             # 失注
    ins_date                   = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    upd_date                   = models.DateTimeField(auto_now=True)
 
class SalesRevise(models.Model):
    mgt_no                     = models.CharField(max_length=18, primary_key=True) # 売上管理No
    seq                        = models.IntegerField()                             # 通番
    rev_date                   = models.DateField()                                # 変更契約日
    rev_delv_date              = models.DateField(null=True, blank=True)           # 変更契約納期
    rev_price_not_inc_tax      = models.IntegerField(null=True, blank=True)        # 変更契約金額(差額・税抜)
    rev_tax                    = models.IntegerField(null=True, blank=True)        # 変更契約金額(差額・消費税)
    tax_type                   = models.CharField(max_length=1)                    # 税区分
    rev_conditions             = models.TextField(null=True, blank=True)           # 変更契約条件
    ins_date                   = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    upd_date                   = models.DateTimeField(auto_now=True)

    class Meta:
       unique_together = ('mgt_no', 'seq',)

    def __unicode__(self):
       return u'%s %d' % (self.sales_mgt_no, self.seq)

class SalesAccept(models.Model):
    mgt_no                     = models.CharField(max_length=18, primary_key=True) # 売上管理No
    seq                        = models.IntegerField()                             # 通番
    proposal_date              = models.DateField()                                # 検収依頼日
    proposal_price_not_inc_tax = models.DateField(null=True, blank=True)           # 検収依頼金額(税抜)
    proposal_tax               = models.IntegerField(null=True, blank=True)        # 検収依頼金額(消費税)
    est_recept_date            = models.IntegerField(null=True, blank=True)        # 入金予定日
    act_recept_date            = models.TextField(null=True, blank=True)           # 入金日
    ins_date                   = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    upd_date                   = models.DateTimeField(auto_now=True)

    class Meta:
       unique_together = ('mgt_no', 'seq',)

    def __unicode__(self):
       return u'%s %d' % (self.sales_mgt_no, self.seq)

class Purchase(models.Model):
    mgt_no                     = models.CharField(max_length=18, primary_key=True) # 仕入管理No
    subject                    = models.TextField()                                # 件名
    supplier_id                = models.TextField()                                # 取引先ID
    quote_no                   = models.TextField(null=True, blank=True)           # 見積No
    quote_issue_date           = models.DateField(null=True, blank=True)           # 見積発行日
    quote_delv_date            = models.DateField(null=True, blank=True)           # 見積納期
    quote_price_not_inc_tax    = models.IntegerField(null=True, blank=True)        # 見積金額(税抜)
    quote_tax                  = models.IntegerField(null=True, blank=True)        # 見積金額(消費税)
    order_no                   = models.TextField(null=True, blank=True)           # 契約No
    order_date                 = models.DateField(null=True, blank=True)           # 契約日
    order_delv_date            = models.DateField(null=True, blank=True)           # 契約納期
    price_not_inc_tax          = models.IntegerField(null=True, blank=True)        # 契約金額(税抜)
    tax                        = models.IntegerField(null=True, blank=True)        # 契約金額(消費税)
    tax_type                   = models.CharField(max_length=1)                    # 税区分
    contract_conditions        = models.TextField(null=True, blank=True)           # 契約条件
    latest_approved_date       = models.DateField(null=True, blank=True)           # 検収日(最新)
    total_appr_price_inc_tax   = models.IntegerField(null=True, blank=True)        # 検収金額(累計・税込み)
    total_left_price_inc_tax   = models.IntegerField(null=True, blank=True)        # 未検収金額(累計・税込み)
    approve_conditions         = models.TextField(null=True, blank=True)           #  検収条件
    latest_paying_date         = models.DateField(null=True, blank=True)           # 支払日(最新)
    total_paying_price_inc_tax = models.IntegerField(null=True, blank=True)        # 支払額(累計・税込み)
    next_paying_date           = models.DateField(null=True, blank=True)           # 支払予定日(最新)
    paying_conditions          = models.TextField(null=True, blank=True)           # 支払条件
    unpaid_price_inc_tax       = models.IntegerField(null=True, blank=True)        # 未払額(累計・税込み)
    order_canceled             = models.BooleanField()                             # キャンセル
    ins_date                   = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    upd_date                   = models.DateTimeField(auto_now=True)

class PurchaseRevise(models.Model):
    mgt_no                     = models.CharField(max_length=18, primary_key=True) # 仕入管理No
    seq                        = models.IntegerField()                             # 通番
    rev_date                   = models.DateField()                                # 変更契約日
    rev_delv_date              = models.DateField(null=True, blank=True)           # 変更契約納期
    rev_price_not_inc_tax      = models.IntegerField(null=True, blank=True)        # 変更契約金額(差額・税抜)
    rev_tax                    = models.IntegerField(null=True, blank=True)        # 変更契約金額(差額・消費税)
    tax_type                   = models.CharField(max_length=1)                    # 税区分
    rev_conditions             = models.TextField(null=True, blank=True)           # 変更契約条件
    ins_date                   = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    upd_date                   = models.DateTimeField(auto_now=True)

    class Meta:
       unique_together = ('mgt_no', 'seq',)

    def __unicode__(self):
       return u'%s %d' % (self.sales_mgt_no, self.seq)

class PurchaseAccept(models.Model):
    mgt_no                     = models.CharField(max_length=18, primary_key=True) # 仕入管理No
    seq                        = models.IntegerField()                             # 通番
    proposal_date              = models.DateField()                                # 検収依頼日
    proposal_price_not_inc_tax = models.DateField(null=True, blank=True)           # 検収依頼金額(税抜)
    proposal_tax               = models.IntegerField(null=True, blank=True)        # 検収依頼金額(消費税)
    est_paying_date            = models.IntegerField(null=True, blank=True)        # 支払予定日
    act_paying_date            = models.TextField(null=True, blank=True)           # 支払日
    ins_date                   = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    upd_date                   = models.DateTimeField(auto_now=True)

    class Meta:
       unique_together = ('mgt_no', 'seq',)

    def __unicode__(self):
       return u'%s %d' % (self.sales_mgt_no, self.seq)

class Expense(models.Model):
    voucher_no                = models.CharField(max_length=18, primary_key=True)  # 伝票No
    subject                   = models.TextField()                                 # 件名
    debit_item_id             = models.TextField()                                 # 勘定ID
    gc_item_id                = models.TextField(null=True, blank=True)            # 勘定ID(販管費)
    rec_date                  = models.DateField()                                 # 計上日
    price_inc_tax             = models.IntegerField()                              # 金額(税込み)
    tax                       = models.IntegerField()                              # 消費税
    tax_type                  = models.CharField(max_length=1)                     # 税区分
    paying_conditions         = models.TextField(null=True, blank=True)            # 支払条件
    paying_date               = models.DateField(null=True, blank=True)            # 支払予定日
    paid_date                 = models.DateField(null=True, blank=True)            # 支払日
    ins_date                  = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    upd_date                  = models.DateTimeField(auto_now=True)

#class TrialSheet(models.Model):

#class BalanceSheet(models.Model):

#class ProfitLossSheet(models.Model):


