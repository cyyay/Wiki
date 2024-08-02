import random
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
from . import util
import markdown2

class NewPage(forms.Form):
    title= forms.CharField(label="Enter the title:", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title', 'style': 'width: 50%;'}))
    content= forms.CharField(label="Enter the content:",  widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Content', 'style': 'width: 50%;'}))

entries = util.list_entries()

def index(request):
    q = request.GET.get('q')
    if q:
        if q.lower() in [s.lower() for s in entries]:
            return redirect('page', name=q)
        elif any(q.lower() in s.lower() for s in entries):
            entry = [e for e in entries if q.lower() in e.lower()]
            return render(request, "encyclopedia/search.html", {
                "q": q,
                "entries": entry
            })
        else:
            return render(request, "encyclopedia/search.html", {
                "i": True,
                "text": q
            })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, name):
    return render(request, "encyclopedia/page.html", {
        "name": name,
        "body": markdown2.markdown(util.get_entry(name))
    })

def create(request):
    if request.method == "POST":
        form=NewPage(request.POST)

        if form.is_valid():
            t= form.cleaned_data["title"]
            c= form.cleaned_data["content"]

            if t not in entries:
                util.save_entry(t, c)
                return HttpResponseRedirect(reverse('page', args=[t]))
            else:
                return render(request, "encyclopedia/create.html", {
                    "form": form,
                    "error": True
                })
    else:
        form= NewPage()


    return render (request, "encyclopedia/create.html", {
        "form": form
    })

def edit(request, name):
    if request.method == "POST":
        form= NewPage(request.POST)
        if form.is_valid():
            content= form.cleaned_data["content"]
            util.save_entry(name, content)
            return HttpResponseRedirect(reverse('page', args=[name]))
    else:
        initial_data= {'title': name,   'content': util.get_entry(name)}
        form= NewPage(initial=initial_data)

    return render(request, "encyclopedia/edit.html", {
        "form": form,
        "title": name
    })

def random_page(request):
    entriees = util.list_entries()
    random_entry = random.choice(entriees)
    return HttpResponseRedirect(reverse('page', args=[random_entry]))