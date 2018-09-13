from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

# Exampt csrf token for testing or tutorial purpose only
# Normally, you will not do like this for security reason
@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()

        # Serialize all data from snippets query set,
        # Return all data in ordered dictionary format
        serializer = SnippetSerializer(snippets, many=True)

        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':

        # JSONParser parse request in json binary format to dictionary
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)

        # If JSON return is serializeable, then save the object
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)

        # If JSON cannot be serializeable, mean response from browser
        # Most likely an error
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':

        serializer = SnippetSerializer(snippet)

        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)

        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':

        snippet.delete()

        return HttpResponse(status=204)