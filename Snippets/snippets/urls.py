from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from snippets import views
from snippets.views import SnippetList, SnippetDetail, UserList, UserDetail

urlpatterns = [
    path('users/', UserList.as_view(), name='user_list'),
    path('users/<int:pk>', UserDetail.as_view(), name='user_detail'),
    path('snippets/', SnippetList.as_view(), name='snippet_list'),
    path('snippets/<int:pk>', SnippetDetail.as_view(), name='snippet_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
