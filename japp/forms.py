from django import forms
from .models import Contact, QuoteRequest, MenuItem, MenuCategory, GalleryImage
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-amber-500 focus:ring-amber-500',
                'placeholder': 'Your Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-amber-500 focus:ring-amber-500',
                'placeholder': 'Your Email'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-amber-500 focus:ring-amber-500',
                'placeholder': 'Subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-amber-500 focus:ring-amber-500',
                'placeholder': 'Your Message',
                'rows': 5
            })
        }

class QuoteRequestForm(forms.ModelForm):
    event_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full rounded-lg border-gray-300 focus:border-amber-500 focus:ring-amber-500',
            'min': date.today().isoformat()
        })
    )
    
    event_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'w-full rounded-lg border-gray-300 focus:border-amber-500 focus:ring-amber-500'
        })
    )
    
    guest_count = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'w-full rounded-lg border-gray-300 focus:border-amber-500 focus:ring-amber-500',
            'placeholder': 'Number of guests'
        })
    )

    class Meta:
        model = QuoteRequest
        exclude = ['user', 'status', 'created_at', 'updated_at']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-amber-500 focus:ring-amber-500',
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-amber-500 focus:ring-amber-500',
                'placeholder': 'Your email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-amber-500 focus:ring-amber-500',
                'placeholder': 'Your phone number'
            }),
            'event_type': forms.Select(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-amber-500 focus:ring-amber-500'
            }),
            'venue': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-amber-500 focus:ring-amber-500',
                'placeholder': 'Event venue/location'
            }),
            'dietary_restrictions': forms.Textarea(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-amber-500 focus:ring-amber-500',
                'rows': 3,
                'placeholder': 'Any dietary restrictions or allergies?'
            }),
            'preferred_menu_items': forms.Textarea(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-amber-500 focus:ring-amber-500',
                'rows': 3,
                'placeholder': 'Any specific menu items you would like?'
            }),
            'special_requests': forms.Textarea(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-amber-500 focus:ring-amber-500',
                'rows': 3,
                'placeholder': 'Any special requests or additional information?'
            }),
            'budget_range': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-amber-500 focus:ring-amber-500',
                'placeholder': 'Your budget range'
            }),
        }

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'category', 'description', 'price', 'image', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-amber-500 focus:ring-amber-500',
                'placeholder': 'Menu item name'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-amber-500 focus:ring-amber-500'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-amber-500 focus:ring-amber-500',
                'rows': 3,
                'placeholder': 'Item description'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-amber-500 focus:ring-amber-500',
                'placeholder': 'Price',
                'step': '0.01'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-amber-500 focus:ring-amber-500',
                'accept': 'image/*'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 rounded border-gray-300 text-amber-600 focus:ring-amber-500'
            })
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero")
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Image file too large ( > 5MB )")
            return image
        return image

class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['title', 'category', 'image', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-amber-500 focus:ring-amber-500',
                'placeholder': 'Image title'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-amber-500 focus:ring-amber-500'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-amber-500 focus:ring-amber-500',
                'rows': 3,
                'placeholder': 'Image description'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-amber-500 focus:ring-amber-500',
                'accept': 'image/*'
            })
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Image file too large ( > 5MB )")
        return image
