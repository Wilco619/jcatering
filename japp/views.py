from django.http import JsonResponse
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'japp/home.html')

@login_required
def dashboard(request):
    return render(request, 'japp/dashboard.html')

def about(request):
    return render(request, 'japp/about.html')

def services(request):
    return render(request, 'japp/services.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        # Send email
        try:
            send_mail(
                f'Contact Form Submission from {name}',
                f'Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}',
                email,
                ['your-email@jcatering.com'],  # Replace with your email
                fail_silently=False,
            )
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('japp:contact')
        except:
            messages.error(request, 'Sorry, there was an error sending your message. Please try again later.')
    
    return render(request, 'japp/contact.html')

def menu(request):
    return render(request, 'japp/menu.html')

def gallery(request):
    return render(request, 'japp/gallery.html')

def request_callback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        service_type = request.POST.get('service_type')
        
        # Send email notification
        try:
            message = f"""
            Callback Request Details:
            Name: {name}
            Phone: {phone}
            Service: {service_type}
            """
            
            send_mail(
                'New Callback Request',
                message,
                'noreply@jcatering.com',
                ['your-email@jcatering.com'],  # Replace with your email
                fail_silently=False,
            )
            
            messages.success(request, "Thank you! We'll call you back soon.")
        except:
            messages.error(request, "Sorry, there was an error processing your request.")
        
    return redirect(request.META.get('HTTP_REFERER', '/'))

def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            # Add email to your subscription list/database
            # Send welcome email
            send_mail(
                'Welcome to J Catering Newsletter',
                'Thank you for subscribing to our newsletter!',
                'noreply@jcatering.com',
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Successfully subscribed to our newsletter!')
        except:
            messages.error(request, 'There was an error processing your subscription.')
    
    return redirect(request.META.get('HTTP_REFERER', '/'))
