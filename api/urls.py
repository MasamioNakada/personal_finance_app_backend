from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BudgetViewSet, TransactionViewSet, FinancialGoalViewSet, 
    ChangeLogViewSet, TagViewSet, CategoryViewSet,
    register_user, login_user
)

# Creamos un router para las vistas de DRF
router = DefaultRouter()
router.register(r'budgets', BudgetViewSet, basename='budget')  
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'financial-goals', FinancialGoalViewSet, basename='financial-goal')
router.register(r'change-logs', ChangeLogViewSet, basename='change-log')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
]
