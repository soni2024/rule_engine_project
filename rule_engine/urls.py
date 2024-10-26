from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_rule/', views.create_rule_view, name='create_rule'),
    path('combine_rules/', views.combine_rules_view, name='combine_rules'),
    path('evaluate_rule/', views.evaluate_rule_view, name='evaluate_rule'),
    # API Endpoints
    path('api/create_rule/', views.create_rule_api, name='create_rule_api'),
    path('api/combine_rules/', views.combine_rules_api, name='combine_rules_api'),
    path('api/evaluate_rule/', views.evaluate_rule_api, name='evaluate_rule_api'),
]
