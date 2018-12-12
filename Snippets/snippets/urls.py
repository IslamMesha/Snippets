from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view
from snippets import views
# from snippets.views import SnippetList, SnippetDetail, UserList, UserDetail, SnippetHighlight
from snippets.views import UserViewSet, SnippetViewSet

# urlpatterns = [
#     path('', views.api_root, name='api_root'),
#     path('schema/', get_schema_view(title='Pastebin API'), name='schema_view'),
#     path('snippets/<int:pk>/highlight/', SnippetHighlight.as_view(), name='snippet-highlight'),
#     path('users/', UserList.as_view(), name='user-list'),
#     path('users/<int:pk>', UserDetail.as_view(), name='user-detail'),
#     path('snippets/', SnippetList.as_view(), name='snippet-list'),
#     path('snippets/<int:pk>', SnippetDetail.as_view(), name='snippet-detail')
# ]

# urlpatterns = [
#     path('', views.api_root, name='api_root'),
#     path('schema/', get_schema_view(title='Pastebin API'), name='schema_view'),
#     path('users/', UserViewSet.as_view({'get': 'list'}), name='user-list'),
#     path('users/<int:pk>', UserViewSet.as_view({'get': 'retrieve'}), name='user-detail'),
#     path('snippets/', SnippetViewSet.as_view({'get': 'list', 'post': 'create'}), name='snippet-list'),
#     path('snippets/<int:pk>',
#          SnippetViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
#          name='snippet-detail'),
#     path('snippets/<int:pk>/highlight/', SnippetViewSet.as_view({'get': 'highlight'}), name='snippet-highlight')
# ]


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'snippets', views.SnippetViewSet)

# The API URLs are now determined automatically by the router.

urlpatterns = [
    path('', include(router.urls)),
    path('schema/', get_schema_view(title='Pastebin API'), name='schema_view'),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
