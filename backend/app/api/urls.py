from django.urls import path
from .views import GenerateQueryView, ExecuteQueryView

urlpatterns = [
    path('generate-query/', GenerateQueryView.as_view(), name='generate-query'),
    path('execute-query/', ExecuteQueryView.as_view(), name='execute-query'),
]
