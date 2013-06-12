# encoding: utf8
import datetime

from django.db import models

from xpinyin import Pinyin
pinyin = Pinyin()

# Changing the models here will impact the revisions

class Activity(models.Model):
    member = models.ForeignKey('Member')
    # 算几次
    weight = models.FloatField(default=1.0)
    date   = models.DateField(default=datetime.date.today())

    cost   = models.FloatField(blank=True)
    deposit= models.FloatField(null=True, blank=True)

    def __unicode__(self):
        s = u'%s * %.1f @ %s' % (self.member.name, self.weight, self.date)
        s += u' -￥%d' % self.cost
        if self.deposit:
            s += u' +￥%.2f' % self.deposit
        return s

class Member(models.Model):
    name  = models.CharField(max_length=50)
    male  = models.BooleanField()
    phone = models.CharField(max_length=15, null=True, blank=True)
    affiliation = models.CharField(max_length=20, null=True, blank=True)
    weight = models.FloatField(default=0.0)
    balance = models.FloatField(default=0.0)
    hidden = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s (balance: %.2f)' % (self.name, self.balance)

    @property
    def index(self):
        return ''.join(pinyin.get_initials(c) for c in self.name)

    @property
    def sex(self):
        return self.male and u'男' or u'女'

    def is_low_balance(self):
        return self.balance <= 0

    def running_total(self):
        "Return (activities, running total, total balance) of the member"

        acts = Activity.objects.filter(member=self).order_by('-date', '-id')

        # filter out zero activity
        acts = list(filter(lambda a: a.deposit or a.cost, acts))
        acts.reverse()

        # calculate running totals
        sum = 0.0
        running = []
        for a in acts:
            if a.deposit:
                sum += a.deposit
            if a.cost:
                sum -= a.cost
            running.append(sum)

        return (acts, running, sum)


