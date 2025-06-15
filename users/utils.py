from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_welcome_email(user):
    subject = 'Welcome to JAWAKA Catering'
    html_content = render_to_string('users/email/welcome.html', {
        'user': user
    })
    text_content = strip_tags(html_content)
    
    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

def send_callback_confirmation(request_data):
    # Send to company
    company_subject = 'New Callback Request'
    company_html = render_to_string('japp/email/callback_request_company.html', {
        'request': request_data
    })
    company_text = strip_tags(company_html)
    
    company_email = EmailMultiAlternatives(
        company_subject,
        company_text,
        settings.DEFAULT_FROM_EMAIL,
        [settings.COMPANY_EMAIL]
    )
    company_email.attach_alternative(company_html, "text/html")
    company_email.send()

    # Send to customer
    customer_subject = 'Callback Request Confirmation'
    customer_html = render_to_string('japp/email/callback_request_customer.html', {
        'request': request_data
    })
    customer_text = strip_tags(customer_html)
    
    customer_email = EmailMultiAlternatives(
        customer_subject,
        customer_text,
        settings.DEFAULT_FROM_EMAIL,
        [request_data['email']]
    )
    customer_email.attach_alternative(customer_html, "text/html")
    customer_email.send()