from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import status
from rest_framework.decorators import api_view


@csrf_exempt
# @api_view(['GET', 'POST', 'PUT', 'DELETE'])
def snippet_list(request, format=None):
    """List all code snippets, or create a new snippet."""
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        """Create a new snippet"""
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            """The HTTP 201 Created success status response code
             indicates that the request has succeeded and has led
              to the creation of a resource."""
            return JsonResponse(serializer.data, status=201)
        else:
            """The HyperText Transfer Protocol (HTTP) 400 Bad Request
             response status code indicates that the server could not
              understand the request due to invalid syntax"""
            return JsonResponse(serializer.errors, status=400)


@csrf_exempt
# @api_view(['GET', 'POST'])
def snippet_detail(request, pk, format=None):
    """Retrieve, update or delete a code snippet."""
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        """The HTTP 404 Not Found client error response
         code indicates that the server can't find the 
         requested resource. """
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser.parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            return HttpResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        snippet.delete()
        """The HTTP 204 No Content success status response
         code indicates that the request has succeeded, 
         but that the client doesn't need to go away from its current page."""
        return HttpResponse(status=204)
