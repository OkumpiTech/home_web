from django import forms

from .models import ContactMessage, Newsletter


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'company', 'country',
                  'service_interest', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your full name', 'autocomplete': 'name'}),
            'email': forms.EmailInput(attrs={
                'placeholder': 'you@company.com', 'autocomplete': 'email'}),
            'phone': forms.TextInput(attrs={
                'placeholder': '+256 700 000 000', 'autocomplete': 'tel'}),
            'company': forms.TextInput(attrs={
                'placeholder': 'Organisation name'}),
            'message': forms.Textarea(attrs={
                'placeholder': 'Tell us about your project…', 'rows': 5}),
        }


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email', 'autocomplete': 'email',
                'aria-label': 'Email address'}),
        }

    def clean_email(self):
        return self.cleaned_data['email'].lower().strip()
