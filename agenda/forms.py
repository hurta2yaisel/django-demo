# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pickle

from django import forms
from django.core.validators import RegexValidator
from django.forms.formsets import BaseFormSet

from .models import Contact, ContactGroup, Phone
from .threadlocals import get_current_user


class MultiWidgetBasic(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [forms.TextInput(),
                   forms.TextInput()]
        super(MultiWidgetBasic, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return pickle.loads(value)
        else:
            return ['', '']


class MultiExampleField(forms.fields.MultiValueField):
    widget = MultiWidgetBasic

    def __init__(self, *args, **kwargs):
        list_fields = [forms.fields.CharField(max_length=31),
                       forms.fields.CharField(max_length=31)]
        super(MultiExampleField, self).__init__(list_fields, *args, **kwargs)

    def compress(self, values):
        ## compress list to single object
        ## eg. date() >> u'31/12/2012'
        return pickle.dumps(values)


class PhoneField(forms.MultiValueField):
    def compress(self, data_list):
        return ';'.join(data_list)

    def __init__(self, *args, **kwargs):
        # Define one message for all fields.
        error_messages = {
            'incomplete': 'Enter a country calling code and a phone number.',
        }
        # Or define a different message for each field.
        fields = (
            forms.CharField(
                error_messages={'incomplete': 'Enter a country calling code.'},
                validators=[
                    RegexValidator(r'^[0-9]+$', 'Enter a valid country calling code.'),
                ],
            ),
            forms.CharField(
                error_messages={'incomplete': 'Enter a phone number.'},
                validators=[RegexValidator(r'^[0-9]+$', 'Enter a valid phone number.')],
            ),
            forms.CharField(
                validators=[RegexValidator(r'^[0-9]+$', 'Enter a valid extension.')],
                required=False,
            ),
        )
        super(PhoneField, self).__init__(
            error_messages=error_messages, fields=fields,
            require_all_fields=False, *args, **kwargs
        )


class LinkForm(forms.Form):
    """
    Form for individual user links
    """
    anchor = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Link Name / Anchor Text',
        }),
        required=False)
    url = forms.URLField(
        widget=forms.URLInput(attrs={
            'placeholder': 'URL',
        }),
        required=False)


class ContactForm(forms.ModelForm):
    # phones = forms.MultiValueField(label='Phones')
    # phones = MultiExampleField(label='Phoness')

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'nick', 'email', 'address', 'avatar', 'user']

    """def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        # self.fields['phones'] = forms.MultiValueField('phone')
        # self.fields['myfield'].widget.attrs.update({'class': 'myfieldclass'})"""


class ContactGroupForm(forms.ModelForm):
    class Meta:
        model = ContactGroup
        fields = ['name', 'contacts', 'user']

    def __init__(self, *args, **kwargs):
        super(ContactGroupForm, self).__init__(*args, **kwargs)
        self.fields['contacts'] = forms.ModelMultipleChoiceField(
            queryset=Contact.objects.filter(user_id=get_current_user().id), widget=forms.CheckboxSelectMultiple())


class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = ['number', 'type', 'contact']


class BasePhoneFormSet(BaseFormSet):
    extra = 1

    def clean(self):
        """
        Adds validation to check that no two phones have the same number or type
        and that all phones have both a number and type.
        """
        if any(self.errors):
            return

        numbers = []
        types = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                number = form.cleaned_data['number']
                type_ = form.cleaned_data['type']

                # Check that no two links have the same anchor or URL
                if number and type_:
                    if number in numbers:
                        duplicates = True
                        numbers.append(number)

                    if type_ in types:
                        duplicates = True
                    types.append(type_)

                if duplicates:
                    raise forms.ValidationError(
                        'Phones must have unique numbers and types.',
                        code='duplicate_phones'
                    )

                # Check that all links have both an anchor and URL
                if type_ and not number:
                    raise forms.ValidationError(
                        'All type must have a number.',
                        code='missing_anchor'
                    )
                elif number and not type_:
                    raise forms.ValidationError(
                        'All numbers must have a type.',
                        code='missing_URL'
                    )
