# -*- coding: utf-8 -*-
from django import forms
from django.utils.safestring import mark_safe
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Div, HTML, Field
from crispy_forms.bootstrap import InlineCheckboxes

from tickle.models.people import Person
from tickle.models.products import Purchase, Holding, Product
from tickle.forms import PersonForm, PublicNameModelChoiceField
from orchard.models import Orchestra, OrchestraMember, OrchestraMembership, OrchestraTicketType


class OrchestraStuffForm(forms.ModelForm):
    product = PublicNameModelChoiceField(queryset=Product.objects.exclude(ticket_type__isnull=False), widget=forms.HiddenInput)  # todo: filter this

    class Meta:
        model = Holding
        fields = ['product', 'quantity']


class RadioInput(forms.CheckboxInput):
    """ Custom hardcoded class for a simple radio button input used in formsets. """

    def render(self, name, value, attrs=None):
        if name.startswith('memberships-0'):
            return mark_safe(u'<input type="radio" name="primary" value="%s" checked />' % name)
        return mark_safe(u'<input type="radio" name="primary" value="%s" />' % name)

    def value_from_datadict(self, data, files, name):
        value = data.get('primary')
        return bool(name == value)


class OrchestraMembershipForm(forms.ModelForm):
    class Meta:
        model = OrchestraMembership
        fields = ['orchestra', 'active', 'primary']
        widgets = {
            'primary': RadioInput,  # TODO: Better multi-select solution.
        }


class OrchestraMemberRegistrationForm(forms.Form):
    ticket_type = forms.ModelChoiceField(queryset=OrchestraTicketType.objects.all())
    food = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    accommodation = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    dinner = forms.BooleanField(widget=forms.CheckboxInput, required=False, label=_("10-/25-year dinner"), help_text=_('Doing your 10th SOF/STORK in a row or the 25th in all? Go to the party!'))


class ApproveOrchestraMemberForm(forms.ModelForm):
    class Meta:
        model = Orchestra
        fields = []


class PersonFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(PersonFormHelper, self).__init__(*args, **kwargs)

        self.form_tag = False
        self.layout = Layout(
            Div(
                Div(
                    'first_name',
                    css_class='col-sm-6'
                ),
                Div(
                    'last_name',
                    css_class='col-sm-6'
                ),
                css_class='row'
            ),
            Div(
                Div(
                    'phone',
                    css_class='col-sm-6'
                ),
                Div(
                    'email',
                    css_class='col-sm-6'
                ),
                css_class='row'
            ),
            Div(
                Div(
                    'id_number',
                    css_class='col-sm-6'
                ),
                Div(
                    css_class='col-sm-6'
                ),
                css_class='row'
            ),
            Div(
                Div(
                    InlineCheckboxes('special_nutrition'),
                    css_class='col-sm-12'
                ),
                css_class='row'
            ),

            'notes'
            )


class OrchestraTicketFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(OrchestraTicketFormHelper, self).__init__(*args, **kwargs)

        self.form_tag = False
        self.layout = Layout(
            'ticket_type',
            'food',
            'accommodation',
            'dinner',
            Div(
                Div(
                    'id_number',
                    css_class='col-sm-6'
                ),
                Div(
                    css_class='col-sm-6'
                ),
                css_class='row'
            ),
            Div(
                Div(
                    Field('special_nutrition', ),
                    css_class='col-sm-12'
                ),
                css_class='row'
            ),
        )


class InlineFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(InlineFormSetHelper, self).__init__(*args, **kwargs)

        self.form_tag = False
        self.template = 'crispy/bootstrap3/table_inline_formset.html'