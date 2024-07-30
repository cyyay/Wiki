from django.shortcuts import redirect, render
from django.http import HttpResponse

from . import util




def index(request):
    q = request.GET.get('q')
    entries = util.list_entries()
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
        "body": util.get_entry(name)
    })
