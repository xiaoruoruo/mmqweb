# encoding: utf-8
from django.db import models

class Entity(models.Model):
    ENTITY_TYPES=(
            (1, "男生"),
            (2, "女生"),
            (3, "团体"),
            )

    name = models.CharField(max_length=10)
    type = models.IntegerField(choices=ENTITY_TYPES, null=True)
    categories = models.ManyToManyField('self', related_name="children", blank=True)
    text = models.TextField(blank=True)
    redirect = models.ForeignKey('self', blank=True, null=True)

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
