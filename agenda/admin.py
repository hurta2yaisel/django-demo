from django.contrib import admin

# Register your models here.
from .models import Contact, ContactGroup, Phone


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass


@admin.register(ContactGroup)
class ContactGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    pass
