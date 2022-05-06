"""levelup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from levelupapi.views import register_user, login_user
from rest_framework import routers 
from levelupapi.views import GameTypeView, EventView, GameView

# The DefaultRouter sets up the resource for each method that is present on the view.
# The trailing_slash=False tells the router to accept /gametypes instead of /gametypes/
router = routers.DefaultRouter(trailing_slash=False) 
# r'gametypes sets up the url
# GameTypeView is telling the server which view to use when it sees that url
# gametype is called the base name
router.register(r'gametypes', GameTypeView, 'gametype') # This line sets up the /gametypes resource
router.register(r'events', EventView, 'event')
router.register(r'games', GameView, 'game')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
