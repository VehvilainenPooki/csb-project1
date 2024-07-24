from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import transaction
from .models import Account


@login_required
@csrf_exempt #Flaw 1: Failure of CSRF

#Flaw 3: 
#@transaction.atomic
def transferView(request):
	if request.method == 'POST':
		to = User.objects.get(username=request.POST.get('to'))
		amount = int(request.POST.get('amount'))
		
		#Flaw 2: A04:2021-Insecure Design
		#if request.user.account.balance >= amount and 0 < amount:
		request.user.account.balance -= amount
		to.account.balance += amount
		request.user.account.save()
		to.account.save()
	
	return redirect('/')



@login_required
def homePageView(request):
	accounts = Account.objects.exclude(user_id=request.user.id)
	return render(request, 'pages/index.html', {'accounts': accounts})
