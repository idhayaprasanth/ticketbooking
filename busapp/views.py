
from busapp.models import create_bus
from django.shortcuts import render,redirect
from django.http import HttpResponse
import os
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from pyzbar.pyzbar import decode
from PIL import Image
from django.http import JsonResponse
from django.db.models import Q
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from razorpay import Client
from django.core.mail import send_mail
from django.template.loader import render_to_string
import datetime








class bus(forms.ModelForm):
    class Meta:
        model = create_bus
        fields = '__all__'

def front(request):
    return render(request,'front.html')


# Create your views here.
def busdetails(request):
   bus_data=create_bus.objects.all()
   context={'bus_list':bus_data}
   return render(request,'image.html',context)
def searchbar1(request):
    if request.method == 'GET':
        input1 = request.GET.get('input1')
        if input1:  # Check if the input1 value exists
            first_objects = create_bus.objects.filter(busname=input1)
            context = {'detail': first_objects}
            return render(request, 'front.html', context)
        else:
            return HttpResponse("Please enter a valid busname.")
    return HttpResponse("Invalid request method")

def searchbar(request):
    if request.method == 'GET':
        input1 = request.GET.get('input1')
        input2 = request.GET.get('input2')
        first_objects = create_bus.objects.all()
        for first_object in first_objects:
            if (first_object.stop1 == input1 and first_object.stop2 == input2) or (first_object.stop1 == input2 and first_object.stop2 == input1):
                r = first_object.ticket1
                busname = first_object.busname
                stop1 = input1
                stop2 = input2
                qr = first_object.qr_code
                amount = r 
                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                order = client.order.create({'amount': amount, 'currency': 'INR'})
                context = {'order_id': order['id'], 'amount': amount,'busname':busname,'stop1':stop1,'stop2':stop2,'qr':qr}
                return render(request, 'payment.html', context)
            elif (first_object.stop1 == input1 and first_object.stop3 == input2) or (first_object.stop1 == input2 and first_object.stop3 == input1):
                r = first_object.ticket2
                busname = first_object.busname
                stop1 = input1
                stop2 = input2
                qr = first_object.qr_code
                amount = r 
                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                order = client.order.create({'amount': amount, 'currency': 'INR'})
                context = {'order_id': order['id'], 'amount': amount,'busname':busname,'stop1':stop1,'stop2':stop2,'qr':qr}
                return render(request, 'payment.html', context)
                
            elif (first_object.stop1 == input1 and first_object.stop4 == input2) or (first_object.stop1 == input2 and first_object.stop4 == input1):
                r = first_object.ticket3
                busname = first_object.busname
                stop1 = input1
                stop2 = input2
                qr = first_object.qr_code
                amount = r 
                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                order = client.order.create({'amount': amount, 'currency': 'INR'})
                context = {'order_id': order['id'], 'amount': amount,'busname':busname,'stop1':stop1,'stop2':stop2,'qr':qr}
                return render(request, 'payment.html', context)
            elif (first_object.stop1 == input1 and first_object.stop5 == input2) or (first_object.stop1 == input2 and first_object.stop5 == input1):
                r = first_object.ticket4
                busname = first_object.busname
                stop1 = input1
                stop2 = input2
                qr = first_object.qr_code
                amount = r 
                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                order = client.order.create({'amount': amount, 'currency': 'INR'})
                context = {'order_id': order['id'], 'amount': amount,'busname':busname,'stop1':stop1,'stop2':stop2,'qr':qr}
                return render(request, 'payment.html', context)
               
            elif (first_object.stop2 == input1 and first_object.stop3 == input2) or (first_object.stop2 == input2 and first_object.stop3 == input1):
                r = first_object.ticket5
                busname = first_object.busname
                stop1 = input1
                stop2 = input2
                qr = first_object.qr_code
                amount = r 
                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                order = client.order.create({'amount': amount, 'currency': 'INR'})
                context = {'order_id': order['id'], 'amount': amount,'busname':busname,'stop1':stop1,'stop2':stop2,'qr':qr}
                return render(request, 'payment.html', context)
                
            elif (first_object.stop2 == input1 and first_object.stop4 == input2) or (first_object.stop2 == input2 and first_object.stop4 == input1):
                r = first_object.ticket6
                busname = first_object.busname
                stop1 = input1
                stop2 = input2
                qr = first_object.qr_code
                amount = r 
                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                order = client.order.create({'amount': amount, 'currency': 'INR'})
                context = {'order_id': order['id'], 'amount': amount,'busname':busname,'stop1':stop1,'stop2':stop2,'qr':qr}
                return render(request, 'payment.html', context)
                
            elif (first_object.stop2 == input1 and first_object.stop5 == input2) or (first_object.stop2 == input2 and first_object.stop5 == input1):
                r = first_object.ticket7
                busname = first_object.busname
                stop1 = input1
                stop2 = input2
                qr = first_object.qr_code
                amount = r 
                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                order = client.order.create({'amount': amount, 'currency': 'INR'})
                context = {'order_id': order['id'], 'amount': amount,'busname':busname,'stop1':stop1,'stop2':stop2,'qr':qr}
                return render(request, 'payment.html', context)
              
            elif (first_object.stop3 == input1 and first_object.stop4 == input2) or (first_object.stop3 == input2 and first_object.stop4 == input1):
                r = first_object.ticket8
                busname = first_object.busname
                stop1 = input1
                stop2 = input2
                qr = first_object.qr_code
                amount = r 
                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                order = client.order.create({'amount': amount, 'currency': 'INR'})
                context = {'order_id': order['id'], 'amount': amount,'busname':busname,'stop1':stop1,'stop2':stop2,'qr':qr}
                return render(request, 'payment.html', context)
               
            elif (first_object.stop3 == input1 and first_object.stop5 == input2) or (first_object.stop3 == input2 and first_object.stop5 == input1):
                r = first_object.ticket9
                busname = first_object.busname
                stop1 = input1
                stop2 = input2
                qr = first_object.qr_code
                amount = r 
                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                order = client.order.create({'amount': amount, 'currency': 'INR'})
                context = {'order_id': order['id'], 'amount': amount,'busname':busname,'stop1':stop1,'stop2':stop2,'qr':qr}
                return render(request, 'payment.html', context)
               
            elif (first_object.stop4 == input1 and first_object.stop5 == input2) or (first_object.stop4 == input2 and first_object.stop5 == input1):
                r = first_object.ticket10
                busname = first_object.busname
                stop1 = input1
                stop2 = input2
                qr = first_object.qr_code
                amount = r 
                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                order = client.order.create({'amount': amount, 'currency': 'INR'})
                context = {'order_id': order['id'], 'amount': amount,'busname':busname,'stop1':stop1,'stop2':stop2,'qr':qr}
                return render(request, 'payment.html', context)
              

        return render(request, 'front.html')
    return HttpResponse("Invalid request method")



def create(request):
    if request.method == 'POST':
        form = bus(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Success: Bus created!")
        else:
            print(form.errors)
            return HttpResponse("Error: Invalid form data")
    else:
        form = bus()
    
    return render(request, 'create.html', {'form': form})
    

def qrcode_decoder(request):
    return render(request, 'qrcode_decoder.html')


def register_request(request):
	...
def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/name")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="log in.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("/name")
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("/name")  # Use redirect here
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})



def payment_success(request):
    # Handle payment success logic here
    return render(request, 'success.html')

def payment_failure(request):
    # Handle payment failure logic here
    return render(request, 'failure.html')


def success(request):
    # This view will be called when the payment is successful
    if request.method == 'POST':
        # Retrieve the payment ID from the POST data
        payment_id = request.POST.get('razorpay_payment_id')

        # Call Razorpay API to fetch payment details
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment = client.payment.fetch(payment_id)

        # Check if the payment is successful
        if payment.get('status') == 'captured':
            # Payment successful, create a transfer
            amount = payment.get('amount')  # Amount in paise
            transfer_amount = int(amount * 0.8)  # Transfer 80% of the amount received
            
            # Replace 'RECIPIENT_ACCOUNT_ID' with the actual recipient's account ID in Razorpay
            recipient_account_id = 'acc_MGgAEqlGMRT1hN'
            
            transfer = client.transfer.create({
                'amount': transfer_amount,
                'currency': 'INR',
                'account': recipient_account_id,
                'receiver_type': 'bank_account',
                'receiver_details': {
                    'name': 'idhaya',
                    'account_number': '2323230020020075',
                    'ifsc': 'RATN0VAAPIS',
                },
                'transfer_mode': 'NEFT',  # Choose the appropriate transfer mode
            })

            # Check if the transfer is successful
            if transfer.get('status') == 'transferred':
                # You can handle further processing here, e.g., updating the database, sending email, etc.
                return HttpResponse("Payment successful. Transfer created and amount transferred!")

            else:
                # Handle transfer failure here
                return HttpResponse("Payment successful, but the transfer failed. Please contact support.")

        else:
            return HttpResponse("Payment unsuccessful!")

    return HttpResponse("Invalid request.")
def pay_id(request):
    if request.method == 'POST':
        # Retrieve the payment ID and amount from the POST data
        payment_id = request.POST.get('razorpay_payment_id')
        amount = request.POST.get('order_id')
        bus = request.POST.get('bus')
        stop1 = request.POST.get('stop1')
        stop2 = request.POST.get('stop2')
        qr = request.POST.get('qr')
        email = request.POST.get('email')
        x = datetime.datetime.now()
        date =x.strftime("%x")
        time = x.strftime("%X")
        context = {'id': payment_id, 'amo': amount,'bus':bus,'stop1':stop1,'stop2':stop2,'qr':qr,'date':date,'time':time}


        subject = 'Hello, Django Email'
        message = 'This is a test email sent from Django.'
        from_email = 'idhayaprasanth56@gmail.com'  # Your Gmail address
        recipient_list = [email] # List of recipient email addresses
        rendered_template = render_to_string('sucess.html', context)


        send_mail(subject, message, from_email, recipient_list,html_message=rendered_template)
        return render(request, 'sucess.html', {'id': payment_id, 'amo': amount,'bus':bus,'stop1':stop1,'stop2':stop2,'qr':qr,'date':date,'time':time})







   





