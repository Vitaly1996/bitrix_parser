from django.urls import path

from leads.views import IndexPageView, update_leads, update_settings

urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
    path('update', update_leads, name='update'),
    path('settings', update_settings, name='settings'),


]
