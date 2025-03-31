
from busapp.models import create_bus,Payment
import qrcode
from django.core.files.base import ContentFile
from io import BytesIO
from django.shortcuts import render,redirect
from django.http import HttpResponse
import os
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.core.mail import EmailMultiAlternatives
from django.core.files.base import ContentFile
from django.utils.html import escape
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
from django.db.models import Sum, Count
from django_user_agents.utils import get_user_agent





def bus_data_analysis(request):
    user_email=request.user.email
    bus = create_bus.objects.filter(email=user_email).first()  # Get the first matching bus
    bus = bus.busname if bus else None  # Ensure bus exists before accessing busname
    date_filter = request.GET.get('date', '')  # Optional date filter
    month_filter = request.GET.get('month', '')  # Optional month filter

    payments = Payment.objects.filter(bus_name=bus) if bus else Payment.objects.none()
    
    if bus and not payments.exists():
        context = {'error': f"No payments found for bus: {bus}"}
        return render(request, 'payment_analysis.html', context)
    
    # Apply date and month filters
    if date_filter:
        payments = payments.filter(bus_name = bus,date=date_filter)
    if month_filter:
        payments = payments.filter(bus_name = bus,date__startswith=month_filter)  # Assuming date format is YYYY-MM-DD
    
    if not payments.exists():
        context = {'error': "No matching payment records found for the given filters."}
        return render(request, 'payment_analysis.html', context)

    # Aggregate Data
    total_passengers = payments.aggregate(total=Sum('passengers'))['total'] or 0
    total_amount = payments.aggregate(total=Sum('amount'))['total'] or 0
    weekly_data = payments.values('date').annotate(total_passengers=Sum('passengers'), total_amount=Sum('amount'))

    context = {
        'payments': payments,
        'total_passengers': total_passengers,
        'total_amount': total_amount,
        'weekly_data': weekly_data,
    }
    return render(request, 'payment_analysis.html', context)


class bus(forms.ModelForm):
    class Meta:
        model = create_bus
        fields = '__all__'

def front(request):
    return render(request,'front.html')

def timetable(request):
    return render(request,'timetable.html')

# Create your views here.
@login_required
def busdetails(request):
    user_agent = get_user_agent(request)
    if user_agent.is_mobile:
        return render(request, 'index.html')

    elif create_bus.objects.filter(email=request.user.email).exists():
        return redirect("/analysis")  # Page for users who created a bus
    else:
        return render(request, 'desktop.html')  # Page for users who haven't created a bus
def searchbar1(request):
    if request.method == 'GET':
        input1 = request.GET.get('input1')
       

        # Get all stops from the database
        all_buses = create_bus.objects.filter(busname = input1)

        # Create a list of unique stops (removing duplicates)
        stops = set()
        for bus in all_buses:
            stops.update([bus.stop1, bus.stop2, bus.stop3, bus.stop4, bus.stop5])

        stops = list(stops)  # Convert the set to a list for template use

        # Filter the buses by input1 (starting point) if provided
        if input1:
            filtered_buses = create_bus.objects.filter(busname=input1).first()
            context = {
                'detail': filtered_buses,
                'stops': stops,
            }
            return render(request, 'front1.html', context)
        else:
            context = {'stops': stops}
            return render(request, 'front1.html', context)

    return HttpResponse("Invalid request method")
def searchbar(request):
    if request.method == 'GET':
        input1 = request.GET.get('input1')
        input2 = request.GET.get('input2')
        passenger = int(request.GET.get('passenger', 1))  # Fix passenger key
        busname = request.GET.get('busname')

        first_objects = create_bus.objects.filter(busname=busname)

        stop_combinations = [
            (["stop1", "stop2"], "ticket1"),
            (["stop1", "stop3"], "ticket2"),
            (["stop1", "stop4"], "ticket3"),
            (["stop1", "stop5"], "ticket4"),
            (["stop2", "stop3"], "ticket5"),
            (["stop2", "stop4"], "ticket6"),
            (["stop2", "stop5"], "ticket7"),
            (["stop3", "stop4"], "ticket8"),
            (["stop3", "stop5"], "ticket9"),
            (["stop4", "stop5"], "ticket10"),
        ]

        for first_object in first_objects:
            for stops, ticket_attr in stop_combinations:
                stop_a, stop_b = stops
                if (getattr(first_object, stop_a) == input1 and getattr(first_object, stop_b) == input2) or \
                   (getattr(first_object, stop_a) == input2 and getattr(first_object, stop_b) == input1):

                    ticket_price = getattr(first_object, ticket_attr, 0)
                    total_amount = ticket_price * passenger  # Fix multiplication

                    if total_amount <= 0:
                        return HttpResponse("Invalid ticket price or passenger count.")

                    # Convert to paise (Razorpay requirement)
                    amount_paise = total_amount

                    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                    order = client.order.create({'amount': amount_paise, 'currency': 'INR'})

                    context = {
                        'order_id': order['id'],
                        'amount': total_amount,  # Show in rupees
                        'busname': first_object.busname,
                        'stop1': input1,
                        'stop2': input2,
                        'qr': first_object.qr_code,
                        'passenger': passenger
                    }
                    return render(request, 'payment.html', context)

        return HttpResponse("No matching bus route found.")

    return HttpResponse("Invalid request method")



def create(request):
    if request.method == 'POST':
        form = bus(request.POST)

        if form.is_valid():
            bus_instance = form.save(commit=False)  # Don't save yet

            # Convert all string fields to uppercase except email
            for field in form.fields:
                if field != 'email':  # Skip email field
                    value = getattr(bus_instance, field, None)
                    if isinstance(value, str):  # Only process string fields
                        setattr(bus_instance, field, value.upper())

            # Format ticket fields to Indian Rupee format
            ticket_fields = [f'ticket{i}' for i in range(1, 11)]  # ticket1 to ticket10
            for field in ticket_fields:
                value = getattr(bus_instance, field, None)
                if value:  # If there's a value
                    try:
                        formatted_value = f"{float(value):.2f}"  # Convert to float and format as `xx.00`
                        setattr(bus_instance, field, formatted_value)
                    except ValueError:
                        pass  # Skip if invalid number input

            bus_instance.save()  # Save the processed data

            return redirect("/name")
        else:
            print(form.errors)
            return HttpResponse("Error: Invalid form data")
    else:
        form = bus()
        email = request.user.email

    return render(request, 'create.html', {'form': form, 'email': email})
    

def qrcode_decoder(request):
    return render(request, 'qrcode_decoder.html')


# Registration View
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("/name")  # Redirect after successful signup
        
        #  If form is NOT valid (e.g., username/email already exists), return the form with errors
        return render(request, 'signup.html', {'form': form})

    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

# Login View
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                return redirect("name")  # ✅ Redirect after successful login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()
    return render(request, "login.html", {"login_form": form})

# Logout View
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect("name")

# Sign Up Form
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

# Change Password View
@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, "Your password has been successfully changed!")
            return redirect("name")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "change_password.html", {"form": form})

# Change Email View
class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

@login_required
def change_email(request):
    if request.method == "POST":
        form = EmailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your email address has been updated!")
            return redirect("name")
    else:
        form = EmailChangeForm(instance=request.user)
    return render(request, "change_email.html", {"form": form})

# Change Username View
class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

@login_required
def change_username(request):
    if request.method == "POST":
        form = UsernameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your username has been updated!")
            return redirect("name")
    else:
        form = UsernameChangeForm(instance=request.user)
    return render(request, "change_username.html", {"form": form})



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
        payment_id = request.POST.get('razorpay_payment_id')
        amount = request.POST.get('order_id')

        if amount:
            amount = int(amount) / 100  # Convert paise to rupees
            amount = "{:.2f}".format(amount)

        bus = request.POST.get('bus')
        stop1 = request.POST.get('stop1')
        stop2 = request.POST.get('stop2')
        email = request.POST.get('email')
        passenger = request.POST.get('passenger')

        x = datetime.datetime.now()
        date = x.strftime("%x")
        time = x.strftime("%X")

        # ✅ Generate QR Code for Payment ID
        qr = qrcode.make(payment_id)
        qr_io = BytesIO()
        qr.save(qr_io, format='PNG')
        qr_image = ContentFile(qr_io.getvalue(), f"qr_codes/{payment_id}.png")

        # ✅ Save data to model (Assuming you have a model Payment)
        from .models import Payment
        payment = Payment.objects.create(
            payment_id=payment_id,passengers=passenger, amount=amount, bus_name=bus,
            stop1=stop1, stop2=stop2, qr_code=qr_image, email=email,
            date=date, time=time
        )
        
        context = {
            'id': payment_id, 'amo': amount, 'busname': bus,'passenger':passenger, 'stop1': stop1, 
            'stop2': stop2, 'qr': payment.qr_code.url, 'email': email, 'date': date, 'time': time
        }

        # ✅ Send Email
        subject = 'Payment Confirmation'
        message = 'Your payment was successful!'
        from_email = 'idhayaprasanth56@gmail.com'
        recipient_list = [email]
        rendered_template = render_to_string('sucess.html', context)
        send_mail(subject, message, from_email, recipient_list, html_message=rendered_template)

        return render(request, 'sucess.html', context)

@login_required
def get_payments(request):
    email = request.user.email  # Automatically get logged-in user's email
    payments = Payment.objects.filter(email=email).order_by('-date', '-time')  # Order by most recent first
    
    if payments.exists():
        data = [
            {
                "payment_id": payment.payment_id,
                "amount": payment.amount,
                "bus_name": payment.bus_name,
                "passengers": payment.passengers,
                "stop1": payment.stop1,
                "stop2": payment.stop2,
                "qr_code": payment.qr_code.url if payment.qr_code else None,
                "email": payment.email,
                "date": payment.date,
                "time": payment.time,
            }
            for payment in payments
        ]
        return render(request, "payment_history.html", {"payments": data, "email": email})
    else:
        return render(request, "payment_history.html", {"message": "No payments found for this email.", "email": email})






