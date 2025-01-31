from django.shortcuts import render, redirect

from . import util

from markdown2 import Markdown
import random

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
    html_content = convert(filename).strip()
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
        if request.method == "POST":
            q = request.POST.get('q').strip()
            html_content = convert(q)
            if html_content is not None:
                print("Search query:", q)  
                return render(request, "encyclopedia/entry.html", {
                    "content": html_content,
                    "title" : q,
                    })        
            
            else:
                recommendations = []
                for item in util.list_entries():
                    if q.lower() in item.lower():
                        recommendations.append(item)

                
                print("Recommendations found:", recommendations)
                return render(request, "encyclopedia/search.html", {
                    "entries" : recommendations,
                    "q" : q,
                    })
            
def newpage(request):
    if request.method == "POST":
        content = request.POST.get('content')
        title = request.POST.get("title").strip()

        if title in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                "message" : "this entry already exists!",
            })
        else:
            util.save_entry(title, content)
            return redirect('markdown_page', filename=title)
    return render(request, "encyclopedia/newpage.html")
        



def  edit(request):
        if request.method == "POST":
            title = request.POST.get("entry_title".strip())
            content = util.get_entry(title)
            return render(request, "encyclopedia/edit.html",{
                "content": content,
                "title" : title,
            })
        
def save_edit(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if content == "":
            return render(request, "encyclopedia/error.html",{
                "message": "Can't save with empty field.",
                           })
        else:
            util.save_entry(title, content)
            content= convert(title)
            return render(request, "encyclopedia/entry.html", {
                    "content": content,
                    "title" : title,
                })
        
def rand_page(request):
    entries = util.list_entries()
    entry_title = random.choice(entries)
    return(entry(request, entry_title))