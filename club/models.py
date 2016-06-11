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
    date   = models.DateField(default=datetime.date.today)

    cost   = models.FloatField(blank=True)
    deposit= models.FloatField(null=True, blank=True)

    comment= models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        s = u'%s * %.1f @ %s' % (self.member.name, self.weight, self.date)
        if self.cost:
            s += u' -￥%d' % self.cost
        if self.deposit:
            s += u' +￥%.2f' % self.deposit
        if self.comment:
            s += u' (%s)' % self.comment
        return s


class Member(models.Model):
    name = models.CharField(max_length=50)
    male = models.BooleanField()
    affiliation = models.CharField(max_length=20, null=True, blank=True)

    # Karma: the larger, the more possible this member will come next time
    weight = models.FloatField(default=0.0)

    balance = models.FloatField(default=0.0)
    hidden = models.BooleanField(default=False)
    hidden_date = models.DateField(null=True)
    cost_override = models.FloatField(null=True, blank=True)
    extra = models.TextField(default='{}')

    def __unicode__(self):
        return u'%s (balance: %.2f)' % (self.name, self.balance)

    @property
    def index(self):
        return ''.join(pinyin.get_initials(c) for c in self.name)

    @property
    def sex(self):
        return self.male and u'男' or u'女'

    @property
    def cost(self):
        if self.cost_override:
            return self.cost_override
        else:
            # When changing the default costs, consider also how to change the
            # existing overrides.
            if self.male:
                return 15.0
            else:
                return 10.0

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


