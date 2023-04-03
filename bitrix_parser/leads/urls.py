from django.urls import path
from leads.logging_config import setup_logging
from leads.views import IndexPageView, logs, update_leads, update_settings

setup_logging()

urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
    path('update', update_leads, name='update'),
    path('settings', update_settings, name='settings'),
    path('logging', logs, name='logging')

]
