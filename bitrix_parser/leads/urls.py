from django.urls import path

from leads.views import IndexPageView, update_leads

urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
    path('update', update_leads, name='update')
]