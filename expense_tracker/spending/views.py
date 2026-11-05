from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from spending.permission import IsOwner


from spending import serializers
from spending.models import ExpenseModel
from spending.serializers import UserSerializer,ExpenseSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated

class RegisterAPIView(APIView):
    permission_classes=[AllowAny]

    def post(self, request):
        serializer_instance=UserSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(serializer_instance.data,status=status.HTTP_201_CREATED)
        return Response(serializer_instance.errors,status=status.HTTP_400_BAD_REQUEST)


#to retrieve data of current loggedin user
class CurrentUserAPIView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        serializer_instance=UserSerializer(request.user)
        return Response(serializer_instance.data,status=status.HTTP_200_OK)

# api view for adding expense

class ExpenseView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer_instances=ExpenseSerializer(data=request.data)
        if serializer_instances.is_valid():
            serializer_instances.save(owner=request.user)
            return Response(serializer_instances.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer_instances.errors)

class GetExpenseView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        e=ExpenseModel.objects.filter(owner=request.user)
        serializers_instances=ExpenseSerializer(e,many=True)
        return Response(serializers_instances.data,status=status.HTTP_200_OK)

from django.shortcuts import get_object_or_404
class RetrieveExpense(APIView):
    permission_classes = [IsOwner]
    def get(self,request,i):
        e=get_object_or_404(ExpenseModel,id=i)
        self.check_object_permissions(request,e)
        serializer_instances=ExpenseSerializer(e) #to check whether user has permission to read
        return Response(serializer_instances.data)

class UpdateExpense(APIView):
    permission_classes = [IsAuthenticated,IsOwner]
    def put(self,request,i):
        e=get_object_or_404(ExpenseModel,id=i)
        self.check_object_permissions(request,e)
        serializers_instances=ExpenseSerializer(e,data=request.data)
        if serializers_instances.is_valid():
            serializers_instances.save()
            return Response(serializers_instances.data,status=status.HTTP_200_OK)
        else:
            return Response(serializers_instances.errors,status=status.HTTP_400_BAD_REQUEST)

class DeleteExpense(APIView):
     permission_classes=[IsAuthenticated,IsOwner]
     def delete(self,request,i):

         e=get_object_or_404(ExpenseModel,id=i)
         self.check_object_permissions(request, e)
         e.delete()
         return Response({"Message":"Deleted successfully"},status=status.HTTP_204_NO_CONTENT)

#aggregating based on salary
from django.db.models import Sum
from datetime import datetime
class ExpenseSummary(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        today=datetime.now().date() #ORM query for fetching current date
        today_expense=ExpenseModel.objects.filter(owner=request.user,created_at__date=today)
        if today_expense:
            # grouping based on salary by using aggregate
            today_total=today_expense.aggregate(total=Sum('amount')).get('total')
            return Response({"Expense_summary": today_total})
        else:
            return Response({"today-total": 0})



#annotate based on current_date and monthly
class ExpenseCategorySummary(APIView):
    def get(self, request):
        current_date= datetime.now().date() # ORM query for fetching current date
        response_data={'today_total':0}
#   Today Expense
        current_expense = ExpenseModel.objects.filter(owner=request.user, created_at__date=current_date)
        if current_expense:
            # for getting current expense by category using values and annotate
            today_total=current_expense.aggregate(total=Sum('amount'))
            total_category=current_expense.values('category').annotate(total_amount=Sum('amount'))
            response_data['today_total']=today_total
            response_data['total_category']=total_category
#   Monthly Expense
        month = datetime.now().month  # ORM query for fetching current month
        year = datetime.now().year  # ORM query for fetching current year
        current_expense = ExpenseModel.objects.filter(owner=request.user, created_at__month=month,
                                                      created_at__year=year)

        if current_expense:
            monthly_total=current_expense.aggregate(total=Sum('amount'))
            monthly_category_summary=current_expense.values('category').annotate(total=Sum('amount'))

            response_data['monthly_total']=monthly_total
            response_data['monthly_category_summary']=monthly_category_summary
        return Response(response_data)

from spending.ai_services import budget_plan
class ExpenseBudgetPlan(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        response_data={
            'monthly_total':0
        }
        year=datetime.now().year
        month=datetime.now().month
        monthly_expense=ExpenseModel.objects.filter(owner=request.user,created_at__year=year,
                                                    created_at__month=month)
        if monthly_expense:
            monthly_total=monthly_expense.aggregate(total=Sum('amount'))
            category_total=monthly_expense.values('category').annotate(total=Sum('amount'))

            response_data['monthly_total']=monthly_total
            response_data['category_total']=category_total

            plan=budget_plan(response_data)
            print(plan)

        response_data['budgetplan']=plan
        return Response(response_data)

