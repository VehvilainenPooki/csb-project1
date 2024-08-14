from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import transaction, connection
from .models import Account

#Flaw 4: A01:2021 – Broken Access Control
#@login_required

@csrf_exempt #Flaw 1: Failure of CSRF

def transferView(request):
	if request.method == 'POST':
		to = User.objects.get(username=request.POST.get('to'))
		amount = int(request.POST.get('amount'))

		try:
			#Flaw 3: A03:2021-Injection
			#amount = int(amount)

			#Flaw 2: A04:2021-Insecure Design
			#if 0 >= amount:
			#	return redirect('/')

			with connection.cursor() as cursor:
				with transaction.atomic():
						#Flaw 2: A04:2021-Insecure Design
						#cursor.execute("SELECT balance FROM pages_account WHERE user_id = %s", [request.user.id])
						#sender_balance = cursor.fetchone()[0]
						#if sender_balance < amount:
						#	return redirect('/')


						cursor.execute("SELECT id FROM auth_user WHERE username = %s", [to.username])
						recipient = cursor.fetchone()
						if recipient is None:
							return HttpResponse("Recipient not found", status=404)
						recipient_id = recipient[0]

						#Flaw 3: A03:2021-Injection
						#cursor.execute("UPDATE pages_account SET balance = balance - %s WHERE user_id = %s", [amount, request.user.id])
						#cursor.execute("UPDATE pages_account SET balance = balance + %s WHERE user_id = %s", [amount, recipient_id])
						cursor.execute("UPDATE pages_account SET balance = balance - " + str(amount) + " WHERE user_id = %s", [request.user.id])
						cursor.execute("UPDATE pages_account SET balance = balance + " + str(amount) + " WHERE user_id = %s", [recipient_id])
				transaction.commit()

		except Exception as e:
			transaction.rollback()
			return HttpResponse(f"An error occurred: {str(e)}", status=500)

	return redirect('/')



@login_required
def homePageView(request):
	accounts = Account.objects.exclude(user_id=request.user.id)
	return render(request, 'pages/index.html', {'accounts': accounts})
