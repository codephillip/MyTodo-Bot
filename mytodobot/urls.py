from django.conf.urls import include, url

from mytodobot.views import MyTodoBotView

urlpatterns = [
    url(r'^9f3227073e6d0cd04ba0f5f750bcff4f5b0e7d22ae762d9067/?$', MyTodoBotView.as_view())
]
