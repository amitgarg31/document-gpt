from django.urls import path
from .views import ask_question,health_check,upload_pdf

urlpatterns = [
    path("ask-question/", ask_question),
    path("health/",health_check),
    path("file/",upload_pdf)
]
