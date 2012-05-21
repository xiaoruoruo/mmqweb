# encoding: utf-8
from django.db import models

class Entity(models.Model):
    Man = 1
    Woman = 2
    Team = 3
    ENTITY_TYPES=(
            (1, "男生"),
            (2, "女生"),
            (3, "团体"),
            )
    ENTITY_TYPES_DICT = dict(ENTITY_TYPES)

    #主要属性
    name = models.CharField(max_length=50)
    type = models.IntegerField(choices=ENTITY_TYPES, null=True)
    text = models.TextField(blank=True)

    #重定向
    redirect = models.ForeignKey('self', blank=True, null=True)

    #冗余属性
    categories = models.ManyToManyField('self', related_name="children", blank=True)

    def __unicode__(self):
        return unicode(self.name)
    
    def alt_names(self):
        "返回该实体的别名序列，即redirect到该实体的实体"
        return Entity.objects.filter(redirect = self.id)

    def children(self):
        "返回以该实体为category的实体"
        raise NotImplementedError()

    def picURL(self):
        "text中出现的第一个URL，将其作为图片地址返回，否则返回None"
        raise NotImplementedError()

class YssyRegistration(models.Model):
    "用来维护注册队列，另一进程向这些id发密码"
    yssyid = models.CharField(max_length=12)
    date = models.DateField()
    code = models.CharField(max_length=10)

    def __unicode__(self):
        return self.yssyid


