from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from survey import urls as survey_urls

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('survey/', include(survey_urls)),
]
