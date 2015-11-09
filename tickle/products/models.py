from decimal import Decimal

from django.db import models, transaction
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from tickle.common.db.fields import MoneyField, NameField, SlugField, DescriptionField
from tickle.common.behaviors import NameMixin, NameSlugMixin, NameSlugDescriptionMixin
from .querysets import ProductQuerySet, HoldingQuerySet, CartQuerySet


@python_2_unicode_compatible
class Cart(models.Model):
    person = models.ForeignKey(
        'people.Person',
        related_name='carts',
        verbose_name=_('person'))
    purchased = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('purchased'))

    objects = CartQuerySet.as_manager()

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')

    def __str__(self):
        return '{} / {}'.format(self.seller, self.person)

    def purchase(self):
        self.purchased = now()


@python_2_unicode_compatible
class Holding(models.Model):
    person = models.ForeignKey(
        'people.Person',
        related_name='holdings',
        verbose_name=_('person'))
    product = models.ForeignKey(
        'Product',
        related_name='holdings',
        verbose_name=_('product'))
    product_variation_choices = models.ManyToManyField(
        'ProductVariationChoice',
        related_name='holdings',
        verbose_name=_('product variation choices'))
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_('quantity'))

    cart = models.ForeignKey(
        'Cart',
        related_name='holdings',
        verbose_name=_('cart'))

    utilized = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('utilized'))

    purchase_price = MoneyField(
        null=True,
        blank=True,
        verbose_name=_('purchase price'))

    objects = HoldingQuerySet.as_manager()


    class Meta:
        verbose_name = _('holding')
        verbose_name_plural = _('holdings')

    def __str__(self):
        return u'{0} {1}'.format(self.product, self.person)

    def clean(self):
        if not self.product.quantitative and not self.quantity == 1:
            raise ValidationError(_('Quantity must be exactly 1 for un-quantitative products.'))

    def send_ticket(self):
        msg = TemplatedEmail(
            to=[self.person.pretty_email],
            from_email='Biljett SOF15 <biljett@sof15.se>',
            subject_template='tickle/email/ticket_subject.txt',
            body_template_html='tickle/email/ticket.html',
            context={
                'holding': self,
                'host': settings.PRIMARY_HOST,
            },
            tags=['tickle', 'ticket'])
        msg.send()

    #Discount from product variations
    def product_variation_choice_delta(self):
        delta = Decimal (0)
        for choice in self.product_variation_choices:
            delta += choice.delta()

    #The final price of the holding.
    #Should only be used when all ProducVariationChoices have been added properly
    def price(self):
        return self.product.base_price + self.product.modifier_delta(self.person) + self.product_variation_choice_delta()


class Product(NameSlugDescriptionMixin, models.Model):
    name = NameField()
    slug = SlugField()
    description = DescriptionField()

    main_event = models.ForeignKey(
        'events.MainEvent',
        verbose_name=_('main event'))

    base_price = MoneyField(
        verbose_name=_('base price'))

    published = models.BooleanField(
        default=True,
        verbose_name=_('published'))
    personal_limit = models.PositiveIntegerField(
        default=1,
        null=True,
        blank=True,
        verbose_name=_('personal limit'),
        help_text=_('Blank means no limit.'))
    total_limit = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('total limit'),
        help_text=_('Blank means no limit.'))
    transferable = models.BooleanField(
        default=True,
        verbose_name=_('transferable'),
        help_text=_('If people should be able to transfer this product to '
                    'other people.'))

    objects = ProductQuerySet.as_manager()

    class Meta:
        unique_together = [
            ['main_event', 'name'],
            ['main_event', 'slug']
        ]
        ordering = ['name']
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def modifier_delta(self, person):
        return self.product_modifiers.met(person).real_delta()

    #Not used for calculating final price.
    def modified_price(self, person):
        self.base_price + self.product_modifiers.met(person).real_delta()

    def has_reached_limit(self):
        return self.limit and self.holdings.purchased().quantity() >= self.limit

class ProductVariation(NameMixin, models.Model):
    name = NameField()

    product = models.ForeignKey(
        'Product',
        related_name='variations',
        verbose_name=_('product'))

    class Meta:
        ordering = ['name']
        unique_together = [
            ['name', 'product']
        ]
        verbose_name = _('product variation')
        verbose_name_plural = _('product variations')
:
class ProductVariationChoice(NameMixin, models.Model)
    name = NameField()
    order = models.PositiveIntegerField(verbose_name=_('order'))
    delta_amount = MoneyField(
        null=True,
        blank=True,
        verbose_name=_('delta (amount)'),
        help_text=_('For discount, enter a negative value.'))

    product_variation = models.ForeignKey(
        'ProductVariation',
        related_name='choices',
        verbose_name=_('product variation'))

    class Meta:
        ordering = ['order']
        unique_together = [
            ['name', 'product_variation']
        ]
        verbose_name = _('product variation choice')
        verbose_name_plural = _('product variation choices')

    def delta(self):
        return self.delta_amount







