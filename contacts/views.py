from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact

def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email  = request.POST['realtor_email']

        #check if user has made already an inqury for same property
        if request.user.is_authenticated:
            user_id=request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id,user_id=user_id)
            if has_contacted:
                messages.error(request,'You have already made a request for this property.')
                return redirect('/listings/'+listing_id)

        contact = Contact(listing=listing,listing_id=listing_id,email=email,name=name,phone=phone,message=message,user_id=user_id)

        contact.save()

        #Send mail
        send_mail(
            'Property Inquiry',
            'There has been an inquiry related to ' + listing + '. Sign in to admin panel for more details',
            'singhroshandu@gmail.com',
            [realtor_email,'singhroshandu.rs@gmail.com'],
            fail_silently=False

        )

        messages.success(request,'You request has been submitted, our realtor will back to you soon.')
        return redirect('/listings/'+listing_id)
