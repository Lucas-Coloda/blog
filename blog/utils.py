from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def load_pages(request, queryset_list):
    paginator = Paginator(queryset_list, 10)

    page = request.GET.get('pag')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    return queryset
