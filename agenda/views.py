from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import authenticate, login as login_, logout as logout_
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.files.storage import FileSystemStorage
from django.db.backends.dummy.base import DatabaseError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from weasyprint import HTML

from .forms import ContactForm, ContactGroupForm, PhoneForm
from .models import Contact, ContactGroup, Phone


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password'] if 'password' in request.POST else request.POST['password1']
        user = authenticate(username=username, password=password)
        if user:
            login_(request, user)
            messages.success(request, "User autenticated successfully")
            pass
        else:
            messages.error(request, "User not autenticated")

    return redirect('home')


def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "User registered successfully")
                login(request)
                return redirect('home')
            except DatabaseError:
                messages.error(request, "User not registered")

    return render(request, 'agenda/register.html', {'form': form})


@login_required
def logout(request):
    logout_(request)
    return redirect('home')


def home(request):
    if request.method == 'GET':
        return render(request, 'agenda/home.html')


@login_required(login_url='/')
def export_contact(request):
    contacts = Contact.objects.filter(user_id=request.user.id)
    host = request.META.get('HTTP_HOST', 'localhost:8000')
    data = {'object_list': contacts, 'host': host}
    html_string = render_to_string('agenda/contact/pdf.html', data)
    html = HTML(string=html_string)
    pdf_file = '%s_contacts.pdf' % request.user.username
    html.write_pdf(target='/tmp/%s' % pdf_file)
    fs = FileSystemStorage('/tmp')
    with fs.open(pdf_file) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s"' % pdf_file
        return response


@login_required(login_url='/')
def list_contact(request):
    if request.method == 'GET':
        contacts = Contact.objects.filter(user_id=request.user.id)
        data = {'object_list': contacts}
        return render(request, 'agenda/contact/list.html', data)


@login_required(login_url='/')
def add_contact(request):
    # user = request.user
    if request.method == 'POST':
        contact = ContactForm(request.POST, request.FILES)
        contact.data['user'] = request.user.id
        if contact.is_valid():
            try:
                contact.save()
                phone_ids = []
                for number_key in contact.data:
                    if number_key.startswith('phone_number'):
                        phone_id = number_key.split('_')[-1]
                        if phone_id not in phone_ids:
                            type_key = 'phone_type_{0}'.format(phone_id)
                            data = {'number': contact.data.get(number_key, '-'),
                                    'type': contact.data.get(type_key, 'mobile'),
                                    'contact': contact.instance.id}
                            phone = PhoneForm(data)
                            if phone.is_valid():
                                phone.save()
                                phone_ids.append(phone_id)
            except DatabaseError:
                messages.error(request, "There was an error saving your contact.")
                return redirect('list_contact')
            messages.success(request, "Contact saved successfully")
        return redirect('list_contact')

    elif request.method == 'GET':
        contact = ContactForm()
        return render(request, 'agenda/contact/new.html', {'form': contact})


@login_required(login_url='/')
def edit_contact(request, id):
    # user = request.user
    instance = get_object_or_404(Contact, id=id)
    contact = ContactForm(request.POST or None, request.FILES or None, instance=instance)
    contact.data['user'] = request.user.id
    if request.method == 'POST' and id:
        if contact.is_valid():
            try:
                contact.save()
                Phone.objects.filter(contact_id=contact.instance.id).delete()
                phone_ids = []
                for number_key in contact.data:
                    if number_key.startswith('phone_number'):
                        phone_id = number_key.split('_')[-1]
                        if phone_id not in phone_ids:
                            type_key = 'phone_type_{0}'.format(phone_id)
                            data = {'number': contact.data.get(number_key, '-'),
                                    'type': contact.data.get(type_key, 'mobile'),
                                    'contact': contact.instance.id}
                            phone = PhoneForm(data)
                            if phone.is_valid():
                                phone.save()
                                phone_ids.append(phone_id)
            except DatabaseError:
                messages.error(request, "There was an error saving your contact.")
                return redirect('list_contact')
            messages.success(request, "Contact updated successfully")
        return redirect('list_contact')

    return render(request, 'agenda/contact/edit.html', {'form': contact})


@login_required(login_url='/')
def delete_contact(request, id):
    if request.method == 'GET':
        instance = get_object_or_404(Contact, id=id)
        instance.delete()
        messages.success(request, "Contact deleted successfully")
    return redirect('list_contact')


@login_required(login_url='/')
def list_group(request):
    if request.method == 'GET':
        groups = ContactGroup.objects.filter(user_id=request.user.id)
        data = {'object_list': groups}
        return render(request, 'agenda/group/list.html', data)


@login_required(login_url='/')
def add_group(request):
    if request.method == 'POST':
        group = ContactGroupForm(request.POST)
        group.data['user'] = request.user.id
        if group.is_valid():
            group.save()
            return redirect('list_group')

    elif request.method == 'GET':
        group = ContactGroupForm()
        return render(request, 'agenda/group/new.html', {'form': group})


@login_required(login_url='/')
def edit_group(request, id):
    instance = get_object_or_404(ContactGroup, id=id)
    group = ContactGroupForm(request.POST or None, instance=instance)
    if request.method == 'POST' and id:
        group.data['user'] = request.user.id
        if group.is_valid():
            group.save()
            return redirect('list_group')

    elif request.method == 'GET':
        return render(request, 'agenda/group/edit.html', {'form': group})


@login_required(login_url='/')
def delete_group(request, id):
    if request.method == 'GET':
        instance = get_object_or_404(ContactGroup, id=id)
        instance.delete()
        return redirect('list_group')
