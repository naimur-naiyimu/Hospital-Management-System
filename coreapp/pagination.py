from rest_framework.pagination import LimitOffsetPagination
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class LargeResultsSetPagination(LimitOffsetPagination):
    default_limit = 300
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = None


def paginate(request, queryset, items_per_page):
    page = request.GET.get('page')
    paginator = Paginator(queryset, items_per_page)

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results.
        items = paginator.page(paginator.num_pages)

    return items
