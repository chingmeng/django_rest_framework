from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import mixins
from rest_framework import generics


class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        # From ListModelMixin
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # From CreateModelMixin
        return self.create(request, *args, **kwargs)


class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        # From RetrieveModelMixin
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        # From UpdateModelMixin
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # From DestroyModelMixin
        return self.destroy(request, *args, **kwargs)
