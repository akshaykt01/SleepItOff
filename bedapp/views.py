from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import *
import razorpay
from django.utils.crypto import get_random_string
from django.core.mail import send_mail


def index(re):
    return render(re, 'index.html')


def test(re):
    return render(re, 'test.html')


def contact(re):
    return render(re, 'complaints2.html')


def roomandbed(re):
    return render(re, 'roomandbed.html')


def about(re):
    return render(re, 'about.html')


def pr(re):
    return render(re, 'pr2.html')


def hostels(re):
    return render(re, 'hostels2.html')



def feedback(re):
    if re.method == 'POST':
        a = re.POST['n1']
        b = re.POST['n2']
        c = re.POST['n3']
        d = re.POST['n4']
        data = Contact.objects.create(name=a, email=b, phone=c, details=d)
        data.save()
        return render(re,'success_complaint.htmlv')
    else:
        return redirect(contact)


# user
def log(re):
    if re.method == 'POST':
        f = re.POST['n1']
        g = re.POST['n2']
        try:
            d = user.objects.get(email=f)
            if d.password == g:
                if d.status == '1':         # user
                    re.session['id1'] = f
                    print('101')
                    return redirect(home)
                else:                       # admin
                    re.session['id2'] = f
                    print('102')
                    return redirect(manage)
            else:
                messages.error(re, 'Incorrect Password')
                return redirect(log)
        except Exception:
            messages.error(re, 'Incorrect Email')
            return redirect(log)
    else:
        return render(re, 'login2.html')


def signup(request):
    if request.method == 'POST':
        email = request.POST.get('n2')  # Get the email from the form
        if user.objects.filter(email=email).exists():  # Check if the email already exists
            messages.error(request, 'User with this email already exists.')
            return render(request, 'signup.html')

        # If email doesn't exist, proceed with creating the user
        f = request.FILES['n6']
        a = request.POST['n1']
        b = email  # Use the email obtained from the form
        c = int(request.POST['n3'])
        d = request.POST['n4']
        e = request.POST['n5']
        data = user.objects.create(uname=a, email=b, phone=c, password=d, gender=e, uphoto=f, status=1,
                                   condition=1)  # status for defining admin/user, condition for any beds booked or not
        data.save()
        return redirect(log)
    else:
        return render(request, 'signup.html')


def logout(re):
    if 'id0' in re.session:
        re.session.flush()
        return redirect(index)
    if 'id1' in re.session:
        re.session.flush()
        return redirect(index)
    if 'id2' in re.session:
        re.session.flush()
        return redirect(index)
    else:
        re.session.flush()
        return redirect(index)


def profile(re):
    if 'id1' in re.session:
        x = re.session['id1']
        d1 = user.objects.filter(email=x)
        return render(re, 'profile2.html', {'r1': d1})
    else:
        return redirect(home)


# dp update
def prfimg(re):
    if re.method == 'POST':
        a = re.POST['n1']
        b = re.FILES['n2']
        data = user.objects.filter(email=a)
        data.update(uphoto=b)
        return redirect(profile)
    else:
        return redirect(profile)


def wprfimg(re):
    if re.method == 'POST':
        x = re.session['id0']
        b = re.FILES['n2']
        data = warden.objects.filter(email=x)
        data.update(wphoto=b)
        return redirect(wardenprofile)
    else:
        return redirect(wardenprofile)

# admin
def manage(request):
    if 'id2' in request.session:
        x = request.session['id2']
        data = user.objects.filter(email=x)
        return render(request, 'adminpage.html', {'r': data})
    else:
        return redirect(log)


# show pending users to admin
def pending(request):
    if request.method == 'GET':
        d = hostel.objects.filter(status='pending')
        return render(request, 'pending3.html', {'r': d})
    else:
        return redirect(manage)


# show all confirmed hostel to admin
def allhostels(request):
    if request.method == 'GET':
        d = hostel.objects.filter(status='confirm')
        return render(request, 'allhostels.html', {'r': d})
    else:
        return redirect(manage)


def allusers(request):
    if request.method == 'GET':
        d = user.objects.filter(status='1')
        return render(request, 'allusers.html', {'r': d})
    else:
        return redirect(manage)


def allbookings(request):
    if request.method == 'GET':
        d = Booking.objects.all()
        return render(request, 'allbookings.html', {'r': d})
    else:
        return redirect(manage)


def confirm(request):
    if request.method == 'POST':
        h = request.POST['n']
        d = hostel.objects.filter(hstlname=h)
        d.update(status='confirm')
        return redirect(pending)
    else:
        return HttpResponse('error')


def remove(request):
    if request.method == 'POST':
        h = request.POST['n']
        d = hostel.objects.filter(hstlname=h)
        d.update(status='rejected')
        return redirect(manage)
    else:
        return HttpResponse('error')


# warden
def wardenlog(re):
    if re.method == 'POST':
        a = re.POST['n1']
        b = re.POST['n2']
        try:
            d = warden.objects.get(email=a)
            if d.password == b:
                re.session['id0'] = a  # session created
                return redirect(wardenprofile)
            else:
                messages.error(re, 'Incorrect Password')
                return redirect(wardenlog)
        except Exception:
            messages.error(re, 'Incorrect Email')
            return redirect(wardenlog)
    else:
        return render(re, 'wardenlogin.html')


def wardensignup(re):
    if re.method == 'POST':
        email = re.POST.get('n3')  # Get the email from the form
        if warden.objects.filter(email=email).exists():  # Check if the email already exists
            messages.error(re, 'Warden with this email already exists.')
            return render(re, 'wardensignup4.html')
        b = re.POST['n2']
        c = email
        d = re.POST['n4']
        e = re.POST['n5']
        f = re.FILES['n6']
        d1 = warden.objects.create(wname=b, email=c, phone=d, password=e, wphoto=f)
        d1.save()
        d2 = hostel.objects.create(email=c, status='Not registered')
        d2.save()
        return redirect(wardenlog)
    else:
        return render(re, 'wardensignup4.html')


def wardenprofile(re):
    if 'id0' in re.session:
        x = re.session['id0']
        d1 = warden.objects.filter(email=x)
        d2 = hostel.objects.filter(email=x)
        return render(re, 'wardenprofile3.html', {'r1': d1,'r2':d2})
    else:
        return redirect(wardenlog)


def hostelupdate(re):
    if re.method == 'POST':
        x = re.POST['n']
        a = re.POST['n1']
        b = re.POST['n2']
        d = re.POST['n4']
        e = re.FILES['n5']
        f = re.FILES['n6']
        g = re.FILES['n7']
        h = re.FILES['n8']
        i = re.FILES['n9']
        j = re.POST['n10']
        k = re.POST['n11']
        l = re.POST['n12']
        m = re.FILES['n13']
        n = re.FILES['n14']
        data = hostel.objects.filter(email=x)
        data.update(hstlname=a, hstltype=b, loc=d, img1=e, img2=f, img3=g, img4=h, img5=i, details=j, wifi=k,
                    price=l, status='pending', hostel_license=m, building_permit=n)
        return redirect(roomandbed)
    else:
        e = re.session['id0']
        data = hostel.objects.filter(email=e)
        return render(re, 'hostelupdate2.html', {'r': data})

def hostelupdatetrue(re):
    if re.method == 'POST':
        x = re.POST['n']
        a = re.POST['n1']
        b = re.POST['n2']
        d = re.POST['n4']
        e = re.FILES['n5']
        f = re.FILES['n6']
        g = re.FILES['n7']
        h = re.FILES['n8']
        i = re.FILES['n9']
        j = re.POST['n10']
        k = re.POST['n11']
        l = re.POST['n12']
        m = re.FILES['n13']
        n = re.FILES['n14']
        data = hostel.objects.filter(email=x)
        data.update(hstlname=a, hstltype=b, loc=d, img1=e, img2=f, img3=g, img4=h, img5=i, details=j, wifi=k,
                    price=l, status='pending', hostel_license=m, building_permit=n)
        return render(re, 'hostelupdatetrue.html',{'r': data})
    else:
        e = re.session['id0']
        data = hostel.objects.filter(email=e)
        return render(re, 'hostelupdatetrue.html', {'r': data})



def home(re):
    if 'id1' in re.session:
        x = re.session['id1']
        d = hostel.objects.filter(status='confirm')
        s = set()
        for i in d:
            s.add(i.loc)
            l = list(s)
        return render(re, 'home.html', {'r': l})
    else:
        return redirect(log)


def wardenhstl(re):
    if 'id0' in re.session:
        x = re.session['id0']
        data = warden.objects.filter(email=x)
        return render(re, 'hostelupdate2.html', {'r': data})
    else:
        return render(re, 'hostelupdate2.html')


def passwordreset(re):
    if re.method == 'POST':
        a = re.POST['n1']
        c = re.POST['n3']
        dt = user.objects.filter(email=a)
        dt.update(password=c)
        return redirect(log)
    else:
        return redirect(profile)

def wardenpasswordreset(re):
    if re.method == 'POST':
        a = re.POST['n1']
        c = re.POST['n3']
        dt = warden.objects.filter(email=a)
        dt.update(password=c)
        return redirect(wardenlog)
    else:
        return render(re,'wardenpr.html')


def wardenbookings(re):
    if re.method == 'POST':
        x = re.POST['n1']
        d = user.object.get(email=x)
    return render(re, 'wardenbookings.html', {'r': d})


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user1 = user.objects.get(email=email)
        except:
            messages.info(request, "Email id not registered")
            return redirect(forgot_password)
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(user=user1, token=token)
        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/reset/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}',
                      'settings.EMAIL_HOST_USER', [email], fail_silently=False)
        except:
            messages.info(request, "Network connection failed")
            return redirect(forgot_password)
    return render(request, 'forget.html')


def reset_password(request, token):
    # Verify token and reset the password
    print(token)
    password_reset = PasswordReset.objects.get(token=token)
    # usr = user.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            u = password_reset.user.uname
            print(u)
            user.objects.filter(uname=u).update(password=new_password)
            # password_reset.user.password(new_password)
            # password_reset.user.save()
            # password_reset.delete()
            return redirect(log)
    return render(request, 'reset.html', {'token': token})


def process_input(request):
    if request.method == 'POST':
        try:
            email = request.session.get('id0')
            if email is None:
                return HttpResponse("Email not found in session.")
            h = hostel.objects.filter(email=email).first()
            if h is None:
                return HttpResponse("No hostels available in the database.")

            # Get the number of rooms
            num_rooms = int(request.POST.get('num_rooms'))
            room_data = {}

            # Loop through each room
            for i in range(num_rooms):
                # Create a room instance and save it to the database
                room_number = request.POST.get('room_' + str(i))
                room = Room.objects.create(hostel=h, room_number=room_number)
                # Get the number of beds for this room
                num_beds = int(request.POST.get('num_beds_' + str(i)))
                bed_data = {}

                # Loop through each bed
                for j in range(num_beds):
                    # Create a bed instance and save it to the database
                    bed_number = request.POST.get('bed_' + str(i) + '_' + str(j))
                    bed_price = request.POST.get('rate_' + str(i) + '_' + str(j))  # Get the bed rate from the form
                    bed_status = 'available'  # Assuming all beds are initially available
                    bed = Bed.objects.create(room=room, bed_number=bed_number, bed_price=bed_price, status=bed_status)
                    bed_data[bed.id] = bed_status
                room_data[room.id] = bed_data
            h.room_data = room_data
            h.save()
            return render(request, 'success_hosteladd.html')
        except Exception as e:
            print(e)
            return HttpResponse("An error occurred during form submission. Please try again later.")
    else:
        return HttpResponse("Invalid request method. Please use POST.")


def user_bookings(re):
    if re.method == 'GET':
        email = re.session.get('id1')
        d = Booking.objects.filter(user_email=email)
        return render(re, 'user_bookings.html', {'r': d})
    else:
        return redirect(home)


def warden_bookings(request):
    if request.method == 'GET':
        e = request.session.get('id0')
        w = hostel.objects.filter(email=e).first()
        if w:
            hostel_name = w.hstlname  # Assuming hostel_name field exists in the Warden model
            bookings = Booking.objects.filter(hostel_name=hostel_name)
            return render(request, 'warden_bookings.html', {'r': bookings})
        else:
            return redirect('home')  # Redirect to home page or handle accordingly
    else:
        return redirect('home')


def warden_cancelled_bookings(request):
    if request.method == 'GET':
        e = request.session.get('id0')
        w = hostel.objects.filter(email=e).first()
        if w:
            hostel_name = w.hstlname  # Assuming hostel_name field exists in the Warden model
            bookings = Booking_Archive.objects.filter(hostel_name=hostel_name)
            return render(request, 'warden_bookings.html', {'r': bookings})
        else:
            return redirect('home')  # Redirect to home page or handle accordingly
    else:
        return redirect('home')

def locselect(re):
    if re.method == 'POST':
        x = re.POST['n']
        y = re.POST['n1']
        d = hostel.objects.filter(loc=x, hstltype=y, status='confirm')
        return render(re, 'hostels2.html', {'r': d})
    else:
        return redirect(home)


def hstldescription(re, a):
    re.session['si'] = a
    d = hostel.objects.filter(hstlname=a)
    return render(re, 'hstldescription.html', {'r': d})


def show_rooms(request, a):
    try:
        h = get_object_or_404(hostel, hstlname=a)
        rooms = Room.objects.filter(hostel=h)
        available_beds_counts = {}
        for room in rooms:
            available_beds_count = room.bed_set.filter(status='Available').count()
            available_beds_counts[room.id] = available_beds_count
        context = {
            'rooms': rooms,
            'available_beds_counts': available_beds_counts
        }
        return render(request, 'room_list.html', context)
    except hostel.DoesNotExist:
        return render(request, 'error.html', {'message': 'Hostel not found'})


def save_room_to_session(request):
    if request.method == 'POST':
        room_number = request.POST.get('room_number')
        request.session['a3'] = room_number
        a3_session = request.session.get('a3')
        print(a3_session)
        return redirect('show_beds', room_number=room_number)  # Pass room_number as argument
    else:
        return HttpResponse('Invalid request method')


def show_beds(request, room_number):
    try:
        beds = Bed.objects.filter(room__room_number=room_number)  # Filter beds based on room_number
        e = request.session.get('id1')
        if e:
            try:
                x = user.objects.get(email=e)
                condition = x.condition
                print(condition)
                # Render different templates based on condition
                if condition == '1':
                    return render(request, 'bed_list.html', {'beds': beds})
                else:
                    return render(request, 'duplicate_booking.html', {'beds': beds})
            except user.DoesNotExist:
                pass

        # If user is not found or condition is not fetched, render the default template
        return render(request, 'bed_list.html', {'beds': beds})
    except Bed.DoesNotExist:
        return HttpResponse("Beds not found.")


def select_bed(request, room_id):
    if request.method == 'POST':
        selected_bed_number = request.POST.get('selected_bed_number')
        request.session['a4'] = selected_bed_number
        return redirect('payment', room_id=room_id)
    else:
        room = get_object_or_404(Room, pk=room_id)
        beds = room.bed_set.filter(status='available')
        return render(request, 'select_bed.html', {'room': room, 'beds': beds})


def payment(request, bed_number, room_id):
    try:
        beds = Bed.objects.filter(bed_number=bed_number)
        if beds.exists():
            bed = beds.first()  # Retrieve the first matching bed
            bed_price = bed.bed_price
            request.session['bd1'] = bed_number
            hostel_name = request.session.get('si')
            return render(request, 'payment3.html', {
                'bed_number': bed_number,
                'room_id': room_id,
                'bed_price': bed_price,
                'hostel_name': hostel_name,
            })
        else:
            return HttpResponse("Bed not found.")
    except Bed.DoesNotExist:
        return HttpResponse("Bed not found.")


def pay(request, id):
    if request.method == 'POST':
        checkin_date = request.POST.get('checkin_date')
        checkout_date = request.POST.get('checkout_date')
        request.session['cknd1'] = checkin_date
        request.session['cktd2'] = checkout_date
        total_amount = request.POST.get('total_amount')
        request.session['ttl'] = total_amount
    # razorpay!!, dont touch
        price = id * 100
        order_currency = 'INR'
        client = razorpay.Client(
            auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
        return render(request, "pay.html", {'r': price})
    else:
        return render(request, "pay.html")


def success(request):
    bed_number = request.session.get('bd1')
    room_id = request.session.get('a3')
    hostel_name = request.session.get('si')
    user_email = request.session.get('id1')
    checkin_date = request.session.get('cknd1')
    checkout_date = request.session.get('cktd2')
    try:
        # Retrieve user information
        user_info = user.objects.get(email=user_email)
        user_name = user_info.uname
        user_phone = user_info.phone
    except user.DoesNotExist:
        return HttpResponse("User not found.")
    except Exception as e:
        print(e)
        return HttpResponse("An error occurred while retrieving user information.")
    if not all([bed_number, room_id, hostel_name, user_name, user_email, user_phone]):
        return HttpResponse("Missing required data for booking.")
    try:
        bed = Bed.objects.get(room__room_number=room_id, bed_number=bed_number, room__hostel__hstlname=hostel_name)
        bed_price = bed.bed_price
        print(bed_price)
        total_amount = request.session.get('ttl')
        booking = Booking.objects.create(
            user_name=user_name,
            user_email=user_email,
            user_phone=user_phone,
            hostel_name=hostel_name,
            room_id=room_id,
            bed_id=bed_number,
            bed_price_per_day=bed_price,
            total_amount=total_amount,
            checkin_date=checkin_date,
            checkout_date=checkout_date
        )
        bed.status = 'Booked'
        bed.save()
        data = user.objects.filter(email=user_email)
        data.update(condition=0)
        return render(request, 'success.html')
    except Bed.DoesNotExist:
        return HttpResponse("Bed not found.")
    except Exception as e:
        print(e)
        return HttpResponse("An error occurred while processing the booking/Duplicate booking")


def delete_and_archive_bookings(request):
    if request.method == 'POST':
        if 'id1' in request.session:
            user_email = request.session['id1']
            bed_number = request.session.get('bd1')
            room_id = request.session.get('a3')
            hostel_name = request.session.get('si')
            try:
                bed = Bed.objects.get(room__room_number=room_id, bed_number=bed_number,
                                      room__hostel__hstlname=hostel_name)

                # Get all bookings associated with the user's email
                bookings_to_archive = Booking.objects.filter(user_email=user_email)
                for booking in bookings_to_archive:
                    # Move data to Booking_Archive
                    Booking_Archive.objects.create(
                        user_name=booking.user_name,
                        user_email=booking.user_email,
                        user_phone=booking.user_phone,
                        hostel_name=booking.hostel_name,
                        room_id=booking.room_id,
                        bed_id=booking.bed_id,
                        bed_price_per_day=booking.bed_price_per_day,
                        total_amount=booking.total_amount,
                        checkin_date=booking.checkin_date,
                        checkout_date=booking.checkout_date
                    )
                # Delete all bookings associated with the user's email
                bookings_to_archive.delete()

                # Update the status of the bed to 'Available'
                bed.status = 'Available'
                bed.save()

                # Update the user's condition to 1
                user.objects.filter(email=user_email).update(condition=1)

                return render(request,'success_bookingcancel.html')
            except Exception as e:
                messages.error(request, f'Error archiving bookings: {e}')
        else:
            messages.error(request, 'User email not found in session.')
        return redirect(home)
    else:
        return redirect(user_bookings)  # Redirect to the user bookings page if not a POST request
