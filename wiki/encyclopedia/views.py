from django.shortcuts import render

from . import util

from markdown2 import Markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def convert(filename):
    markdowner = Markdown()
    if util.get_entry(filename) == None:
        return None
    return markdowner.convert(util.get_entry(filename))

def entry(request, filename):
    print(f"Searching for entry: {filename}")
    html_content = convert(filename.strip())
    print(html_content)
    if html_content == None:
        return render(request, "encyclopedia/error.html",{
            "message": "this entry doesnt exist"
        })
        
    else:
        return render(request, "encyclopedia/entry.html", {
            "content": html_content,
            "title" : filename,
        })

def search(request):
        q = request.POST.get('q'.strip())
        print(q)
        if q in util.list_entries():
            html_content = convert(q)
            if html_content is not None:
                return render(request, "encyclopedia/entry.html", {
                    "content": html_content,
                    "title" : q,
                })
            
def newpage(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                "message" : "this entry already exists!",
            })
        else:
            util.save_entry(title, content)
    return render(request, "encyclopedia/newpage.html")
        



def  edit(request):
    return(request, "encyclopedia/edit.html")