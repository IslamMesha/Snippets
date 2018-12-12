from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins, permissions
from rest_framework import generics
from rest_framework import renderers
from rest_framework import viewsets

from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view, action


# API Root.
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user_list', request=request, format=format),
        'snippets': reverse('snippet_list', request=request, format=format)
    })


# User Views
# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# User Views using ViewSets
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Snippet Views

# Snippet Views using ViewSets
class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Using Mixins
# class SnippetList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#
# class SnippetDetail(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# class SnippetHighlight(generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     renderer_classes = (renderers.StaticHTMLRenderer,)
#
#     def get(self, request, *args, **kwargs):
#         snippet = self.get_object()
#         return Response(snippet.highlighted)

# Class Based Views
# class SnippetList(APIView):
#     def get(self, request, format=None):
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class SnippetDetail(APIView):
#
#     @staticmethod
#     def get_snippet_object(pk):
#         try:
#             snippet = Snippet.objects.get(pk=pk)
#             return snippet
#         except snippet.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         snippet = self.get_snippet_object(pk=pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         snippet = self.get_snippet_object(pk=pk)
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         snippet = self.get_snippet_object(pk=pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# Function Based Views.
# @csrf_exempt
# # @api_view(['GET', 'POST', 'PUT', 'DELETE'])
# def snippet_list(request, format=None):
#     """List all code snippets, or create a new snippet."""
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return JsonResponse(serializer.data, safe=False)
#     elif request.method == 'POST':
#         """Create a new snippet"""
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             """The HTTP 201 Created success status response code
#              indicates that the request has succeeded and has led
#               to the creation of a resource."""
#             return JsonResponse(serializer.data, status=201)
#         else:
#             """The HyperText Transfer Protocol (HTTP) 400 Bad Request
#              response status code indicates that the server could not
#               understand the request due to invalid syntax"""
#             return JsonResponse(serializer.errors, status=400)
#
#
# @csrf_exempt
# # @api_view(['GET', 'POST'])
# def snippet_detail(request, pk, format=None):
#     """Retrieve, update or delete a code snippet."""
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         """The HTTP 404 Not Found client error response
#          code indicates that the server can't find the
#          requested resource. """
#         return HttpResponse(status=404)
#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return JsonResponse(serializer.data)
#     elif request.method == 'PUT':
#         data = JSONParser.parse(request)
#         serializer = SnippetSerializer(snippet, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         else:
#             return HttpResponse(serializer.errors, status=400)
#     elif request.method == 'DELETE':
#         snippet.delete()
#         """The HTTP 204 No Content success status response
#          code indicates that the request has succeeded,
#          but that the client doesn't need to go away from its current page."""
#         return HttpResponse(status=204)
