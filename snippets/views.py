from rest_framework import permissions

from snippets.serializers import *
from snippets.permissions import IsOwnerOrReadOnly

from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

from rest_framework import renderers

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


# used the ModelViewSet class in order to get the complete set of default read and write operations.
class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    # Notice that we've also used the @action decorator to create a custom action, named highlight.
    # This decorator can be used to add any custom endpoints
    # that don't fit into the standard create/update/delete style.

    # Custom actions which use the @action decorator will respond to GET requests by default.
    # We can use the methods argument if we wanted an action that responded to POST requests.

    # The URLs for custom actions by default depend on the method name itself.
    # If you want to change the way url should be constructed, you can include url_path as a decorator keyword argument.
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@api_view(['GET'])
def api_root(request, format=None):
    # note the user-list and snippet-list are the named from url.py
    print("Reverse of user-list: " + reverse('user-list', request=request, format=format))
    print("Reverse of snippet-list: " + reverse('snippet-list', request=request, format=format))
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })
