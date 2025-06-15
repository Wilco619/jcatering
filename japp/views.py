from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from users.utils import send_callback_confirmation
from .models import Subscriber, MenuCategory, MenuItem, GalleryImage, TeamMember, QuoteRequest, Contact
from .forms import ContactForm, QuoteRequestForm,MenuItemForm, GalleryImageForm
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from datetime import timedelta, datetime
import csv

def home(request):
    return render(request, 'japp/home.html')

@login_required
def dashboard_view(request):
    active_quotes = QuoteRequest.objects.filter(
        user=request.user,
        status__in=['pending', 'in_review', 'quoted']
    ).order_by('-created_at')[:5]
    
    quote_history = QuoteRequest.objects.filter(
        user=request.user
    ).order_by('-created_at')[:10]
    
    context = {
        'active_quotes': active_quotes,
        'quote_history': quote_history,
    }
    return render(request, 'japp/dashboard.html', context)

def about(request):
    team_members = TeamMember.objects.all()
    context = {
        'team_members': team_members
    }
    return render(request, 'japp/about.html', context)

def services(request):
    return render(request, 'japp/services.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            
            # Send email notification
            send_mail(
                f'New Contact Form Submission: {contact.subject}',
                f'Name: {contact.name}\nEmail: {contact.email}\nMessage: {contact.message}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.COMPANY_EMAIL],
                fail_silently=False,
            )
            
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('japp:contact')
    else:
        form = ContactForm()
    
    return render(request, 'japp/contact.html', {'form': form})

def menu(request):
    categories = MenuCategory.objects.all()
    menu_items = MenuItem.objects.filter(is_available=True)
    context = {
        'categories': categories,
        'menu_items': menu_items
    }
    return render(request, 'japp/menu.html', context)

def gallery(request):
    images = GalleryImage.objects.all().order_by('-created_at')
    context = {
        'images': images
    }
    return render(request, 'japp/gallery.html', context)

def request_callback(request):
    if request.method == 'POST':
        request_data = {
            'name': request.POST.get('name'),
            'phone': request.POST.get('phone'),
            'service_type': request.POST.get('service_type'),
            'email': request.POST.get('email')
        }
        send_callback_confirmation(request_data)
        messages.success(request, 'Your callback request has been received. We will contact you shortly.')
    return redirect('japp:home')

def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            # Add subscriber to database
            subscriber, created = Subscriber.objects.get_or_create(
                email=email,
                defaults={'subscribed_at': timezone.now()}
            )

            if created:
                # Send welcome email to subscriber
                subject = 'Welcome to JAWAKA Newsletter'
                html_content = render_to_string('japp/email/subscriber_welcome.html')
                text_content = strip_tags(html_content)
                
                msg = EmailMultiAlternatives(
                    subject,
                    text_content,
                    settings.DEFAULT_FROM_EMAIL,
                    [email]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                # Send notification to company
                company_subject = 'New Newsletter Subscriber'
                company_context = {
                    'email': email,
                    'subscribed_at': subscriber.subscribed_at
                }
                company_html = render_to_string(
                    'japp/email/new_subscriber_notification.html',
                    company_context
                )
                company_text = strip_tags(company_html)
                
                company_msg = EmailMultiAlternatives(
                    company_subject,
                    company_text,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.COMPANY_EMAIL]
                )
                company_msg.attach_alternative(company_html, "text/html")
                company_msg.send()

                messages.success(request, 'Successfully subscribed to our newsletter!')
            else:
                messages.info(request, 'You are already subscribed to our newsletter.')
                
        except Exception as e:
            messages.error(request, 'There was an error processing your subscription.')
    
    return redirect(request.META.get('HTTP_REFERER', '/'))

# def quote_request(request):
#     if request.method == 'POST':
#         form = QuoteRequestForm(request.POST)
#         if form.is_valid():
#             quote = form.save(commit=False)
#             if request.user.is_authenticated:
#                 quote.user = request.user
#             quote.save()
            
#             # Send email to company
#             context = {
#                 'quote': quote,
#             }
#             html_content = render_to_string('japp/email/quote_request_notification.html', context)
#             text_content = strip_tags(html_content)
            
#             email = EmailMultiAlternatives(
#                 f'New Quote Request - {quote.event_type}',
#                 text_content,
#                 settings.DEFAULT_FROM_EMAIL,
#                 [settings.COMPANY_EMAIL]
#             )
#             email.attach_alternative(html_content, "text/html")
#             email.send()
            
#             # Send confirmation email to customer
#             customer_context = {
#                 'quote': quote,
#             }
#             customer_html = render_to_string('japp/email/quote_request_confirmation.html', customer_context)
#             customer_text = strip_tags(customer_html)
            
#             customer_email = EmailMultiAlternatives(
#                 'Quote Request Received - JAWAKA Catering',
#                 customer_text,
#                 settings.DEFAULT_FROM_EMAIL,
#                 [quote.email]
#             )
#             customer_email.attach_alternative(customer_html, "text/html")
#             customer_email.send()
            
#             messages.success(request, 'Your quote request has been submitted successfully! We will contact you shortly.')
#             return redirect('japp:quote_request')
#     else:
#         form = QuoteRequestForm()
    
#     return render(request, 'japp/quote_request.html', {'form': form})

def quote_request_view(request):
    if request.method == 'POST':
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            quote = form.save()
            
            # Send email to company
            company_context = {
                'quote': quote,
                'is_company': True
            }
            company_html = render_to_string('japp/email/quote_notification.html', company_context)
            company_text = strip_tags(company_html)
            
            company_email = EmailMultiAlternatives(
                f'New Quote Request - {quote.event_type}',
                company_text,
                settings.DEFAULT_FROM_EMAIL,
                [settings.COMPANY_EMAIL]
            )
            company_email.attach_alternative(company_html, "text/html")
            company_email.send()
            
            # Send confirmation email to customer
            context = {
                'quote': quote,
                'company_email': settings.COMPANY_EMAIL,
                'company_phone': getattr(settings, 'COMPANY_PHONE', None)
            }
            # Send confirmation email
            send_mail(
                subject='Quote Request Confirmation - JAWAKA Catering',
                message='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[quote.email],
                html_message=render_to_string(
                    'japp/email/quote_confirmation.html',
                    context,
                    request=request
                )
            )
            
            messages.success(request, 'Your quote request has been submitted successfully! We will contact you shortly.')
            return redirect('japp:quote_request')
    else:
        form = QuoteRequestForm()
    
    return render(request, 'japp/quote_request.html', {'form': form})

@staff_member_required
def admin_dashboard(request):
    context = {
        'active_tab': 'dashboard',
        'pending_quotes_count': QuoteRequest.objects.filter(status='pending').count(),
        'unread_messages_count': Contact.objects.filter(is_read=False).count(),
        'total_menu_items': MenuItem.objects.count(),
        'total_gallery_items': GalleryImage.objects.count(),
        'recent_quotes': QuoteRequest.objects.all().order_by('-created_at')[:5],
        'recent_contacts': Contact.objects.all().order_by('-created_at')[:5],
    }
    return render(request, 'japp/admin/dashboard.html', context)

@staff_member_required
def admin_menu(request):
    menu_items = MenuItem.objects.all().order_by('category', 'name')
    context = {
        'active_tab': 'menu',
        'menu_items': menu_items
    }
    return render(request, 'japp/admin/menu.html', context)

@staff_member_required
def admin_menu_add(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu item added successfully!')
            return redirect('japp:admin_menu')
    else:
        form = MenuItemForm()
    
    return render(request, 'japp/admin/menu_form.html', {'form': form, 'action': 'Add'})

@staff_member_required
def admin_menu_edit(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=menu_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu item updated successfully!')
            return redirect('japp:admin_menu')
    else:
        form = MenuItemForm(instance=menu_item)
    
    context = {
        'form': form,
        'menu_item': menu_item,
        'action': 'Edit',
        'active_tab': 'menu'
    }
    return render(request, 'japp/admin/menu_form.html', context)

@staff_member_required
def admin_menu_delete(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    
    if request.method == 'POST':
        # Delete the associated image file if it exists
        if menu_item.image:
            menu_item.image.delete(save=False)
        
        menu_item.delete()
        messages.success(request, 'Menu item deleted successfully!')
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@staff_member_required
def admin_gallery(request):
    images = GalleryImage.objects.all().order_by('-created_at')
    context = {
        'active_tab': 'gallery',
        'images': images
    }
    return render(request, 'japp/admin/gallery.html', context)

@staff_member_required
def admin_gallery_add(request):
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gallery image added successfully!')
            return redirect('japp:admin_gallery')
    else:
        form = GalleryImageForm()
    
    context = {
        'form': form,
        'action': 'Add',
        'active_tab': 'gallery'
    }
    return render(request, 'japp/admin/gallery_form.html', context)

@staff_member_required
def admin_gallery_edit(request, pk):
    gallery_image = get_object_or_404(GalleryImage, pk=pk)
    
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES, instance=gallery_image)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gallery image updated successfully!')
            return redirect('japp:admin_gallery')
    else:
        form = GalleryImageForm(instance=gallery_image)
    
    context = {
        'form': form,
        'gallery_image': gallery_image,
        'action': 'Edit',
        'active_tab': 'gallery'
    }
    return render(request, 'japp/admin/gallery_form.html', context)

@staff_member_required
def admin_gallery_delete(request, pk):
    gallery_image = get_object_or_404(GalleryImage, pk=pk)
    
    if request.method == 'POST':
        # Delete the image file from storage
        if gallery_image.image:
            gallery_image.image.delete(save=False)
        
        gallery_image.delete()
        messages.success(request, 'Gallery image deleted successfully!')
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@staff_member_required
def admin_quotes(request):
    quotes = QuoteRequest.objects.all().order_by('-created_at')
    context = {
        'active_tab': 'quotes',
        'quotes': quotes,
        'pending_quotes_count': quotes.filter(status='pending').count()
    }
    return render(request, 'japp/admin/quotes.html', context)

@staff_member_required
def admin_quote_update_status(request, pk):
    if request.method == 'POST':
        quote = get_object_or_404(QuoteRequest, pk=pk)
        new_status = request.POST.get('status')
        if new_status in ['pending', 'reviewed', 'accepted', 'rejected']:
            quote.status = new_status
            quote.save()
            messages.success(request, f'Quote status updated to {new_status}')
        return redirect('japp:admin_quotes')

@staff_member_required
def admin_contacts(request):
    contacts = Contact.objects.all().order_by('-created_at')
    context = {
        'active_tab': 'contacts',
        'contacts': contacts,
        'unread_messages_count': contacts.filter(is_read=False).count()
    }
    return render(request, 'japp/admin/contacts.html', context)

@staff_member_required
def admin_subscribers(request):
    subscribers = Subscriber.objects.all().order_by('-created_at')
    context = {
        'active_tab': 'subscribers',
        'subscribers': subscribers
    }
    return render(request, 'japp/admin/subscribers.html', context)

@staff_member_required
def admin_subscribers_export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="subscribers_{datetime.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Email', 'Date Subscribed'])
    
    subscribers = Subscriber.objects.all().order_by('-created_at')
    for subscriber in subscribers:
        writer.writerow([subscriber.email, subscriber.created_at.strftime("%Y-%m-%d %H:%M:%S")])
    
    return response

def get_recent_activities():
    # Get activities from the last 7 days
    seven_days_ago = timezone.now() - timedelta(days=7)
    
    activities = []
    
    # Recent quotes
    recent_quotes = QuoteRequest.objects.filter(
        created_at__gte=seven_days_ago
    ).order_by('-created_at')[:5]
    for quote in recent_quotes:
        activities.append({
            'type': 'quote',
            'message': f'New quote request from {quote.name} for {quote.event_type}',
            'timestamp': quote.created_at
        })
    
    # Recent contacts
    recent_contacts = Contact.objects.filter(
        created_at__gte=seven_days_ago
    ).order_by('-created_at')[:5]
    for contact in recent_contacts:
        activities.append({
            'type': 'contact',
            'message': f'New contact message from {contact.name}',
            'timestamp': contact.created_at
        })
    
    # Recent subscribers
    recent_subscribers = Subscriber.objects.filter(
        subscribed_at__gte=seven_days_ago
    ).order_by('-subscribed_at')[:5]
    for subscriber in recent_subscribers:
        activities.append({
            'type': 'subscriber',
            'message': f'New subscriber: {subscriber.email}',
            'timestamp': subscriber.subscribed_at
        })
    
    # Sort all activities by timestamp
    return sorted(activities, key=lambda x: x['timestamp'], reverse=True)[:10]

from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import QuoteRequest

@staff_member_required
def admin_quote_detail(request, pk):
    quote = get_object_or_404(QuoteRequest, pk=pk)
    
    context = {
        'quote': quote,
        'active_tab': 'quotes',
        'status_choices': QuoteRequest.STATUS_CHOICES
    }
    return render(request, 'japp/admin/quote_detail.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Contact

@staff_member_required
def admin_contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    
    # Mark as read when viewing
    if not contact.is_read:
        contact.is_read = True
        contact.save()
        messages.success(request, 'Message marked as read')
    
    context = {
        'contact': contact,
        'active_tab': 'contacts',
    }
    return render(request, 'japp/admin/contact_detail.html', context)

@staff_member_required
def admin_contact_mark_read(request, pk):
    if request.method == 'POST':
        contact = get_object_or_404(Contact, pk=pk)
        contact.is_read = True
        contact.save()
        messages.success(request, 'Message marked as read')
        return redirect('japp:admin_contacts')
    return redirect('japp:admin_contact_detail', pk=pk)
