from django.shortcuts import render, redirect

from . import util

from markdown2 import Markdown
import os, random


# Mardown coverter
markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
 
# generating any entri by its title name from the list of entries
# also converting its content to MD to HTML
def entry(request, title):
    # getting list of entries
    entries_list = util.list_entries()

    # checking if the request entry is part of the registered entries
    if title not in entries_list:
        return render(request, "encyclopedia/not_found.html", {
            "title":title
                })
    return render(request, "encyclopedia/entry.html", {
        "content": markdowner.convert(util.get_entry(f"{title}")),
        "title":title
        })

def search(request):
    # getting the search word from the search bar stored in q
    query = request.GET.get("q")
    
    # filtering entries by this term
    all_entries = util.list_entries()
    if query in all_entries:
        return render(request, "encyclopedia/entry.html", {
            "content": markdowner.convert(util.get_entry(f"{query}")),
            "title":query
            })

    # if the query term does not match, show list of entryis with matching query substring
    else:
        matching_entries = []
        match = False
        for entry in all_entries:
            if query.lower() in entry.lower():
                matching_entries.append(entry)
        if matching_entries:
            match = True
            
        return render(request, "encyclopedia/search.html", {
            "query":query, 
            "matching_entries":matching_entries,
            "match":match
    })

def new_page(request):
    return render(request, "encyclopedia/new_page.html")

def entry_created(request):
    all_entries = util.list_entries()
    if request.method == "POST":
        title = request.POST.get("title")
        new_content = request.POST.get("new_page")
        if title in all_entries:
            # entry already exist in db
            return render(request, "encyclopedia/apology.html", {
                "title": title
            })
        else:
            util.save_entry(title, new_content)
            return entry(request, title)

def edit_page(request, entry_name):
    title = entry_name
    content = util.get_entry(title)
    if request.method == "GET":
        return render(request, "encyclopedia/edit.html",{
            "title":title,
            "content":content
        })
    if request.method == "POST":
        new_content = request.POST.get("edit_page")
        new_title = request.POST.get("title")

        # renaming entry in db
        os.rename(f"./entries/{title}.md", f"./entries/{new_title}.md")
        util.save_entry(new_title, new_content)
        return entry(request,new_title)
    
def random_page(request):
    all_entries=util.list_entries()
    title = random.choice(all_entries)
    return entry(request, title)