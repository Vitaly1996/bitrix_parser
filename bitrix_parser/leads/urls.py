from django.urls import path

from leads.views import update_leads, update_settings, IndexPageView, logs
from leads.logging_config import setup_logging

setup_logging()

urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
    path('update', update_leads, name='update'),
    path('settings', update_settings, name='settings'),
    path('logging', logs, name='logging')

]
