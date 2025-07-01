from django.shortcuts import render,redirect,HttpResponse
from .forms import RegisterForm,transactionForm,goalForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import transactions,Goal
from .admin import tranImportExport
from django.contrib import messages

# Create your views here.
# def home(request):
#     return render(request,'finance/home.html')

def registerView(request):
    if(request.method=="POST"):
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            #this logins and sends it to 127.0.0.1/8000/accounts/profile after login, but we want
            #it to be redirected to the dashboard page, hence in settings we make login_redirect_url to be '/'
            login(request,user)
            messages.success(request,"Account created successfully !")
            return redirect('dashboardView')

    else:
        form=RegisterForm()
    return render(request,'finance/register.html',{'form':form})

@login_required
def dashboardView(request):
    if(request.method=="GET"):
        all_transactions=transactions.objects.filter(user=request.user)
        all_goals=Goal.objects.filter(user=request.user)
        total_income=transactions.objects.filter(user=request.user,transaction_type="Income")
        income_amount=0
        for income in total_income:
            income_amount=income_amount+income.amount

        total_expense=transactions.objects.filter(user=request.user,transaction_type="Expense")
        expense_amount=0
        for expense in total_expense:
            expense_amount=expense_amount+expense.amount    

        netSavings=income_amount-expense_amount
        remainingSavings=netSavings    

        goalProgress=[]
        for goal in all_goals:
            if remainingSavings>=goal.target_amount:
                goalProgress.append({'goal':goal, 'progress':100})
                remainingSavings=remainingSavings-goal.target_amount
            elif remainingSavings>0:
                progress=(remainingSavings/goal.target_amount)*100
                goalProgress.append({'goal':goal, 'progress':progress})
                remainingSavings=0
            else:
                goalProgress.append({'goal':goal, 'progress':0})

            
        passingValues={
            'all_transactions':all_transactions,
            'all_goals':all_goals,
            'netSavings':netSavings,
            'income_amount':income_amount,
            'expense_amount':expense_amount,
            'goalProgress':goalProgress,
        }

    return render(request,'finance/dashboard.html',passingValues)

@login_required
def addTransaction(request):
    if(request.method=='POST'):
        form=transactionForm(request.POST)
        if form.is_valid():
            transaction=form.save(commit=False)
            transaction.user=request.user
            transaction.save()
            messages.success(request,"Transaction created successfully !")
            return redirect('dashboardView')
    else:
        form=transactionForm()
    return render(request,'finance/transaction_form.html',{'form':form})
    
@login_required
def transactionList(request):
    transaction_list=None
    if request.method=="GET":
        transaction_list=transactions.objects.filter(user=request.user)
    return render(request,'finance/transaction_list.html',{'transaction_list':transaction_list})

@login_required
def goalView(request):
    if(request.method=='POST'):
        form=goalForm(request.POST)
        if form.is_valid():
            goal=form.save(commit=False)
            goal.user=request.user
            goal.save()
            messages.success(request,"Goal created successfully !")
            return redirect('dashboardView')
        else:
            print("FORM ERRORS:", form.errors)
    else:
        form=goalForm()
    return render(request,'finance/goal_form.html',{'form':form})


def export_transaction(request):
    user_transactions=transactions.objects.filter(user=request.user)
    tranResource=tranImportExport()
    dataset=tranResource.export(queryset=user_transactions)
    excel_data=dataset.export('csv')
    response=HttpResponse(excel_data,content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition']='attachment;filename=transactions_report.xlsx'
    messages.success(request,"Download Started successfully !")
    return response

