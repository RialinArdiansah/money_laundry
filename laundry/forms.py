from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Customer, Order


User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username/Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Password')


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'address', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EmployeeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'role', 'phone']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'EMPLOYEE'
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'service_type', 'weight_kg', 'date_in', 'estimated_done', 'notes']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'weight_kg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date_in': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estimated_done': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned = super().clean()
        for f in ['customer', 'service_type', 'weight_kg', 'date_in', 'estimated_done']:
            if not cleaned.get(f):
                raise forms.ValidationError('Harap lengkapi semua data pesanan sebelum menyimpan.')
        return cleaned
