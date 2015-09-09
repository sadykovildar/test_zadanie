#!/usr/local/bin/python
# coding: utf-8
import json
from django.http import HttpResponse
from .models import Note, Category
from django.contrib import auth
from django.shortcuts import get_object_or_404, render, redirect
from .forms import NoteForm
from django.core.context_processors import csrf
import datetime
from django.core.urlresolvers import reverse


def index(request):
    # Fill Categories, if didn't it yet
    temp = Category.create('TODO')
    if Category.objects.get(category=temp.category):
        pass
    else:
        temp.save()

    temp = Category.create('Заметка')
    if Category.objects.get(category=temp.category):
        pass
    else:
        temp.save()

    temp = Category.create('Памятка')
    if Category.objects.get(category=temp.category):
        pass
    else:
        temp.save()

    temp = Category.create('Ссылка')
    if Category.objects.get(category=temp.category):
        pass
    else:
        temp.save()
    note_form = NoteForm(initial={'category': Category.objects.get(category='Заметка')})
    context = {}
    context.update(csrf(request))
    username = auth.get_user(request).username
    latest_note_list = []
    if username:
        latest_note_list = Note.objects.order_by('-pub_date').filter(user=request.user)[:]
    context['latest_note_list'] = latest_note_list
    context['username'] = username
    context['form'] = note_form

    return render(request, 'notes/index.html', context)


def one_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    args = {}
    username = auth.get_user(request).username
    args['note'] = note
    args['username'] = username
    args['url'] = request.build_absolute_uri(reverse('one_note', args=(note.pk, )))
    return render(request, 'notes/one_note.html', args)


def newnote(request):
    if request.POST:
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.pub_date = datetime.datetime.now()
            form.save()
    return redirect('/')


def edit_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    if note.user != request.user:
        return redirect('/note/%s' % note_id)
    note_form = NoteForm(initial={'header': note.header, 'text': note.text,
                                  'category': note.category, 'chosen': note.chosen})
    context = {}
    context.update(csrf(request))
    username = auth.get_user(request).username
    context['username'] = username
    context['form'] = note_form
    context['note'] = note
    return render(request, 'notes/note_edit.html', context)


def save_edited_notes(request, note_id):
    a = Note.objects.get(pk=note_id)
    if a.user != request.user:
        return redirect('/note/%s' % note_id)
    if request.POST:
        form = NoteForm(request.POST, instance=a)
        if form.is_valid():
            note = form.save()
            note.user = request.user
            form.save()
    return redirect('/note/%s' % note_id)


def delete_note(request, note_id):
    a = Note.objects.get(pk=note_id)
    if a.user != request.user:
        return redirect('/note/%s' % note_id)
    a.delete()
    return redirect('/')


def sort_ajax(request):
    username = auth.get_user(request).username

    # Create criterion of sorting
    if not request.user.username == username or not request.POST.get('s_category') \
            or not request.POST.get('s_cret'):
        return 'error'
    else:
        if request.POST.get('s_category') == '1':
            m = "" if request.POST.get('s_cret') == '1' else "-"
            m += "pub_date"
        elif request.POST.get('s_category') == '2':
            m = "" if request.POST.get('s_cret') == '1' else "-"
            m += "category"
        elif request.POST.get('s_category') == '3':
            m = "" if request.POST.get('s_cret') == '1' else "-"
            m += "chosen"
        else:
            return 'error'
    sorted_note_list = Note.objects.filter(user=request.user).order_by(m)
    context_json = [temp.as_dict() for temp in sorted_note_list]
    response_data = {'notes': context_json, 'username': username}

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def search_ajax(request):
    username = auth.get_user(request).username
    print("!")
    criterion = request.POST.get('id_of_criterion')
    data = request.POST.get('data')
    if not request.user.username == username or not criterion \
            or not data:
        return 'error'
    else:
        print(criterion)
        print(data)

        # create criterion of search, and search notes
        context_json = []
        if criterion == "1":
            print("date!")
            d = data[0:2]
            m = data[3:5]
            y = data[6:]
            searched_notes = Note.objects.filter(user=request.user,
                                                 pub_date__year=y, pub_date__month=m, pub_date__day=d)
            print(searched_notes)
            if len(searched_notes) > 0:
                for temp in searched_notes:
                    context_json.append(temp.as_dict())
            else:
                return HttpResponse('Нет заметок')
        elif criterion == "2":
            searched_notes = Note.objects.filter(user=request.user, header=data)
            print(searched_notes)
            if len(searched_notes) > 0:
                context_json = [temp.as_dict() for temp in searched_notes]
            else:
                return HttpResponse('Нет заметок')

            print("header!")
        elif criterion == "3":
            print("category!")
            cat = Category.objects.get(category=data)
            searched_notes = Note.objects.filter(user=request.user, category=cat)
            if len(searched_notes) > 0:
                context_json = [temp.as_dict() for temp in searched_notes]
            else:
                return HttpResponse('Нет заметок')
        elif criterion == "4":
            print("checked!")
            bool_data = 1 if data == "1" else 0
            searched_notes = Note.objects.filter(user=request.user, chosen=bool_data)
            if len(searched_notes) > 0:
                context_json = [temp.as_dict() for temp in searched_notes]
            else:
                return HttpResponse('Нет заметок')

        response_data = {'notes': context_json}
        print(response_data)
        return HttpResponse(json.dumps(response_data), content_type="application/json")


def del_note_on_index(request):
    uuid = request.POST.get('note_uuid')
    a = Note.objects.get(pk=uuid)
    a.delete()
    username = auth.get_user(request).username
    sorted_note_list = Note.objects.filter(user=request.user).order_by('-pub_date')
    context_json = [temp.as_dict() for temp in sorted_note_list]
    response_data = {'notes': context_json, 'username': username}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def set_chosen(request):
    uuid = request.POST.get('note_uuid')
    a = Note.objects.get(pk=uuid)
    print(a)
    print(a.chosen)
    if a.chosen:
        a.chosen = False
    else:
        a.chosen = True
    a.save()
    return HttpResponse(a.chosen)


def open_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    if not note.uuid_boolean:
        note.uuid_boolean = True
    note.save()
    args = {}
    username = auth.get_user(request).username
    args['note'] = note
    args['username'] = username
    args['url'] = request.build_absolute_uri(reverse('one_note', args=(note.pk, )))
    return render(request, 'notes/one_note.html', args)


def close_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    if note.uuid_boolean:
        note.uuid_boolean = False
    note.save()
    args = {}
    username = auth.get_user(request).username
    args['note'] = note
    args['username'] = username
    args['url'] = request.build_absolute_uri(reverse('one_note', args=(note.pk, )))
    return render(request, 'notes/one_note.html', args)
