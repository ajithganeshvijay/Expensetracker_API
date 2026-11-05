"""
URL configuration for expense_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from spending import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register',views.RegisterAPIView.as_view()),
    path('cuser',views.CurrentUserAPIView.as_view()),
    path('login',obtain_auth_token),
    path('expense',views.ExpenseView.as_view()),
    path('list',views.GetExpenseView.as_view()),
    path('retrieve/<int:i>',views.RetrieveExpense.as_view()),
    path('update/<int:i>',views.UpdateExpense.as_view()),
    path('delete/<int:i>',views.DeleteExpense.as_view()),
    path('summary',views.ExpenseSummary.as_view()),
    path('category',views.ExpenseCategorySummary.as_view()),
    path('plan',views.MonthlyBudgetPlan.as_view())
]
