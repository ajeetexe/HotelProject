from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import User, ForgetPasswordVarify, Booking, UserMessage, PaymentDetail,Room
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .helper import vallidate_password
from django.conf import settings
from django.core.mail import send_mail
import uuid
from redmail import outlook
from django.urls import reverse
import datetime 
# Create your views here.


def mail_query_button(request):
    if request.method == 'POST' and 'mail-query-btn' in request.POST:
        full_name = request.POST.get('full-name')
        email = request.POST.get('email')
        message = request.POST.get('msg')
        try:
            msg_obj = UserMessage()
            msg_obj.full_name = full_name
            msg_obj.email = email
            msg_obj.message = message
            user_obj = User.objects.filter(email=email).first()
            if user_obj:
                msg_obj.is_registerd = True
            msg_obj.save()
            messages.success(request, 'Message sent successfully...')
            return redirect('/')
        except Exception as e:
            print(e)


def index(request):
    mail_query_button(request)
    if request.method == 'POST' and 'avail' in request.POST:
        check_in = request.POST.get('arival')
        check_out = request.POST.get('departure')
        adult = request.POST.get('adult')
        children = request.POST.get('children')
        return redirect(f'/roomview/{check_in}&{check_out}/')

    return render(request, 'index.html')


def register_user(request):
    mail_query_button(request)
    if request.method == 'POST' and 'btn' in request.POST:
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone Number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('Confirm password')
        gender = request.POST.get('gender')
        user = User.objects.filter(email=email).first()

        if user:
            messages.error(request, 'User already exist')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if password != confirm_password:
            messages.error(
                request, 'Password does not match with confirm password')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if vallidate_password(password)[0]:
            for x in vallidate_password(password)[1]:
                messages.error(request, x)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if len(phone) != 10 or not phone.isnumeric():
            messages.error(request, 'Invalid number')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user_obj = User.objects.create(
            first_name=first_name, last_name=last_name, email=email, phone=phone, gender=gender, password=password)
        user_obj.set_password(password)
        user_obj.save()
        messages.success(request, 'Successfully registered')
        return redirect('/')
    else:
        pass
    return render(request, 'registrationpage.html')


def login_user(request):
    mail_query_button(request)
    # if request.GET:  
    #     next = request.GET['next']

    if request.method == 'POST' and 'btn' in request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email == None or password == None:
            messages.error(request, 'Email or Password must not be empty.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        user = User.objects.filter(email=email).first()
        if user is None:
            messages.error(request, 'User not found')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user_obj = authenticate(email=email, password=password)
        if user_obj:
            login(request, user_obj)
            messages.success(request, 'Login Successfully.')
            return redirect('/')
        else:
            messages.error(request, 'Password or email is incorrect')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'Logout successfully')
    return redirect('/')


def send_mail(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user_obj = User.objects.filter(email=email).first()
            if user_obj is None:
                messages.error(request, 'User not found')
                return redirect('/forget-password/send-mail/')
            verify = ForgetPasswordVarify.objects.filter(user=user_obj).first()
            if verify:
                verify.delete()
            data = str(uuid.uuid4())
            varify_obj = ForgetPasswordVarify.objects.create(
                user=user_obj, data=data)
            varify_obj.save()
            send_mail_verify(email, data)

            messages.success(request, 'Reset mail sent to your email')
            response = HttpResponseRedirect(reverse('index'))
            response.set_cookie('data', data, 24*3600)
            response.set_cookie('email', email, 24*3600)
            return response
        except Exception as e:
            print(e)
    return render(request, 'forget-password/send-mail.html')


def check_mail(request, data):
    try:
        verify_obj = ForgetPasswordVarify.objects.filter(data=data).first()
        if verify_obj and 'data' in request.COOKIES and 'email' in request.COOKIES:
            verify_obj.is_varified = True
            verify_obj.save()
            return redirect('/forget-password/set-password/')
        else:
            messages.error(
                request, 'Your reset password expired, please try again.')
            return redirect('/')
    except Exception as e:
        print(e)


def send_mail_verify(email, data):
    outlook.username = 'Hrooms.com@outlook.com'
    outlook.password = 'Hrooms@123'

    subject = "Password reset"
    message = f"Hi please click or paste  the link to reset the account http://127.0.0.1:8000/forget-password/check-mail/{data}/"

    outlook.send(subject, receivers=email, text=message)


def set_password(request):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.COOKIES['email']
        try:
            user_obj = User.objects.filter(email=email).first()

            if password1 != password2:
                messages.error(
                    request, 'Password not matched with confirm passord')
                return redirect('/forget-password/set-password/')
            if vallidate_password(password1)[0]:
                for x in vallidate_password(password1)[1]:
                    messages.error(request, x)
                return redirect('/forget-password/set-password/')

            user_obj.set_password(password1)
            user_obj.save()
            messages.success(request, 'Password reset successfully')
            return redirect('/login/')
        except Exception as e:
            print(e)
    return render(request, 'forget-password/set-password.html')


def special_package(request):
    mail_query_button(request)
    return render(request, 'pacakages.html')


def about(request):
    mail_query_button(request)
    return render(request, 'about.html')


def contact(request):
    mail_query_button(request)
    return render(request, 'contact.html')

# @login_required(login_url='/login/')


def restraunt(request):
    mail_query_button(request)
    return render(request, 'restaurant.html')


@login_required(login_url='/login/')
def gallery_hotel(request):
    return render(request, 'hotel.html')


@login_required(login_url='/login/')
def gallery_rooms(request):
    return render(request, 'rooms.html')


@login_required(login_url='/login/')
def room_view(request,check_in,check_out):
    mail_query_button(request)

    book_obj = Booking.objects.all()
    check_in = datetime.datetime.strptime(check_in,"%Y-%m-%d").date()
    check_out = datetime.datetime.strptime(check_out,"%Y-%m-%d").date()
    ctx = {}
    ctx['checkin'] = check_in
    ctx['checkout'] = check_out
    room_list = []
    if book_obj:
        for x in book_obj:        
            if check_in > x.check_in and check_out > x.check_out:
                room_list.append(str(x.room))
            
        for y in Room.objects.all():
            if not y.is_booked:
                room_list.append(y.pk)
        ctx['room_obj'] = Room.objects.filter(pk__in = room_list)
    else:
        ctx['room_obj'] = Room.objects.all()
        
    return render(request, 'roomview.html',context=ctx)


@login_required(login_url='/login/')
def booking(request,room_id,checkin,checkout):
    mail_query_button(request)
    if request.method == 'POST' and 'btn' in request.POST:
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        phone_number = request.POST.get('pnumber')
        email = request.POST.get('email')
        check_in = request.POST.get('checkin')
        check_out = request.POST.get('checkout')
        guest = request.POST.get('guest')
        room_type = request.POST.get('type')
        try:
            room = Room.objects.get(pk=room_id)
            book = Booking()
            room.is_booked = True
            room.save()
            book.first_name = first_name
            book.last_name = last_name
            book.phone_number = phone_number
            book.email = request.user
            book.check_in = check_in
            book.check_out = check_out
            book.guests = guest
            book.room_type = room_type
            book.room = room
            book.save()

            pay_obj = PaymentDetail()
            pay_obj.booking_id = book
            pay_obj.save()
            return redirect(f'/payment/{book}/')
        except Exception as e:
            print(e)
    return render(request, 'booking.html', context={'in':checkin,'out':checkout})


@login_required(login_url='/login/')
def payment(request, booking_id):
    if request.method == 'POST':
        card_holder_name = request.POST.get('card-holder-name')
        card_type = request.POST.get('card-type')
        card_number = request.POST.get('card-number')
        card_name = request.POST.get('card-name')
        expiry = request.POST.get('expiry')
        cvv = request.POST.get('cvv')
        try:
            pay_obj = PaymentDetail.objects.filter(
                booking_id=booking_id).first()

            if pay_obj:
                pay_obj.card_holder_name = card_holder_name
                pay_obj.card_type = card_type
                pay_obj.card_number = card_number
                pay_obj.card_name = card_name
                pay_obj.expiry_date = expiry
                pay_obj.cvv = cvv
                pay_obj.save()
                return redirect(f'/payment/receipt/{pay_obj.payment_id}/success/')
            return redirect(f'/payment/receipt/{pay_obj.payment_id}/fail/')
        except Exception as e:
            print(e)
    return render(request, 'payment.html')

@login_required(login_url='/login/')
def payment_receipt(request,p_id,status):
    ctx = {}
    try:
        pay_obj = PaymentDetail.objects.filter(payment_id = p_id).first()
        book_obj = Booking.objects.filter(booking_id=uuid.UUID(str(pay_obj.booking_id))).first()
        room_obj = Room.objects.filter(pk=str(book_obj.room)).first()
        ctx['pay_obj'] = pay_obj
        ctx['book_obj'] = book_obj
        ctx['room_obj'] = room_obj
        ctx['status'] = status
        total_people = int(book_obj.guests)
        cost = room_obj.room_price 
        if book_obj.room_type =='Single Bed':
            cost = cost * total_people
        elif book_obj.room_type =='Single Bed with AC':
            cost = cost * total_people * 2
        elif book_obj.room_type =='Double Bed':
            cost = cost * (total_people // 2) * 2
        elif book_obj.room_type =='Double Bed with AC':
            cost = cost * (total_people // 2) * 2 * 2
        ctx['cost'] = cost
    except Exception as e:
        print(e)
    return render(request,'payment-receipt.html',context=ctx)


@login_required(login_url='/login/')
def term_condition(request):
    return render(request, 'terms-condition.html')


@login_required(login_url='/login/')
def profile(request):
    mail_query_button(request)
    try:

        user_obj = User.objects.filter(email=request.user).first()
        book_obj = Booking.objects.filter(email=request.user).all()
        context = {
            'user_obj': user_obj,
            'book_obj': book_obj
        }
    except Exception as e:
        print(e)
    return render(request, 'profile.html', context=context)


@login_required(login_url='/login/')
def know_more(request, booking_id):
    try:
        context = {
            'book_obj': Booking.objects.filter(booking_id=booking_id).first(),
            'payment_obj': PaymentDetail.objects.filter(booking_id=booking_id).first()
        }
    except Exception as e:
        print(e)

    return render(request, 'know-more.html',context=context)

def check_avaiblity(request):
    if request.method == 'POST' and 'avail' in request.POST:
        check_in = request.POST.get('arival')
        check_out = request.POST.get('departure')
        return redirect(f'/roomview/{check_in}&{check_out}/')
    return render(request,'check_rooms.html')