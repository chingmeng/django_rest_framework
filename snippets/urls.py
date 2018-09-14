from django.urls import path, include
from rest_framework.routers import DefaultRouter
from snippets import views
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title='Pastebin API')


# Note using router will bypass your api-view get method, so you won't see your print in the
# server message
# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('schema/', schema_view),
]