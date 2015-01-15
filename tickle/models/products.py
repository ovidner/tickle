# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField


@python_2_unicode_compatible
class Event(MPTTModel):
    name = models.CharField(max_length=256, verbose_name=_('name'))
    parent = TreeForeignKey('self', null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('name'))
    description = models.TextField(blank=True, verbose_name=_('description'))

    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('price'))
    quantitative = models.BooleanField(default=False, help_text=_('Can you purchase more than one (1) of this product?'))

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class TicketType(models.Model):
    product = models.OneToOneField('Product', related_name='ticket_type')
    events = models.ManyToManyField('Event', verbose_name=_('events'))

    def __str__(self):
        return self.product.name


@python_2_unicode_compatible
class Holding(models.Model):
    person = models.ForeignKey('Person')
    product = models.ForeignKey('Product')

    quantity = models.PositiveIntegerField(default=1)  # todo: validate this! base on Product.quantitative

    def __str__(self):
        return u'{0} {1}'.format(self.product, self.person)


@python_2_unicode_compatible
class Delivery(models.Model):
    holdings = models.ManyToManyField('Holding')
    delivered = models.DateTimeField()

    def __str__(self):
        return u'{0}, {1}'.format(self.holdings, self.delivered)


@python_2_unicode_compatible
class Purchase(models.Model):
    person = models.ForeignKey('Person')
    holdings = models.ManyToManyField('Holding')

    purchased = models.DateTimeField()

    valid = models.BooleanField(default=True)

    def __str__(self):
        return u'{0}'.format(self.person)