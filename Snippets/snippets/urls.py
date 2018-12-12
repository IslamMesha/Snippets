from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from snippets import views
from snippets.views import SnippetList, SnippetDetail

urlpatterns = [
    path('snippets/', SnippetList.as_view(), name='snippet_list'),
    path('snippets/<int:pk>', SnippetDetail.as_view(), name='snippet_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
