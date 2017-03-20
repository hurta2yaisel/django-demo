from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Contact(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    nick = models.CharField(max_length=30)
    email = models.EmailField()
    # phones = models.CharField(max_length=255, default='-')
    # phones = models.ManyToManyField(Phone)
    avatar = models.ImageField(upload_to='avatars')
    address = models.CharField(max_length=255)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return '%s %s (%s)' % (self.first_name, self.last_name, self.nick)

    class Meta:
        ordering = ('first_name',)


class ContactGroup(models.Model):
    name = models.CharField(max_length=30)
    contacts = models.ManyToManyField(Contact)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Phone(models.Model):
    number = models.CharField(max_length=30)
    type = models.CharField(max_length=30, choices=(('mobile', 'Mobile'),
                                                    ('home', 'Home'),
                                                    ('work', 'Work'),
                                                    ('fax', 'Fax'),
                                                    ('other', 'Other')),
                            default='mobile')
    contact = models.ForeignKey(Contact)

    def __unicode__(self):
        return self.number

    class Meta:
        ordering = ('number',)
