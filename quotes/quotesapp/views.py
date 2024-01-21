from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
# from django.views.generic import ListView

#from django.http import HttpResponse

from .models import Tag, Author, Quote
from .forms import TagForm, AuthorForm, QuoteForm


# class QuoteListView(ListView):
#     paginate_by = 2
#     model = Quote

# def index(request):
#     return HttpResponse("Hello, world. Quotes App Page.")

def main(request):
    
    # dostęp do listy tylko dla zalogowanych
    # ale w tym projekcie jest on dostępny dla wszystkich
    #quote_list = Quote.objects.all() if request.user.is_authenticated else []
    
    quote_list = Quote.objects.all()
    paginator = Paginator(quote_list, 10)
    
    page_number = request.GET.get("page")
    quotes = paginator.get_page(page_number)
    return render(request, 'quotesapp/index.html', {'quotes': quotes})
    

@login_required
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/tag.html', {'form': form})

    return render(request, 'quotesapp/tag.html', {'form': TagForm()})


@login_required
def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/author.html', {'form': form})

    return render(request, 'quotesapp/author.html', {'form': AuthorForm()})

@login_required
def quote(request):
    tags = Tag.objects.all()
    author = Author.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            
            # author assign
            choice_author = Author.objects.get(fullname__in=request.POST.getlist('author'))
            new_quote.author = choice_author
            new_quote.save()
            
            # # tags assigns
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(*choice_tags)
            
            # print("DEBUG choice_author:", choice_author)
            # print("DEBUG quote:", new_quote.quote)
            # print("DEBUG tags:", choice_tags)

            # print("DEBUG new_quote.author:", new_quote.author)
            # print("DEBUG new_quote.quote:", new_quote.quote)
            # print("DEBUG new_quote.tags:", new_quote.tags)

            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/quote.html', {"tags": tags, "author": author, 'form': form})

    return render(request, 'quotesapp/quote.html', {"tags": tags, "author": author, 'form': QuoteForm()})


def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quotesapp/author_detail.html', {"author": author})


def quote_detail(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)
    return render(request, 'quotesapp/quote_detail.html', {"quote": quote})
