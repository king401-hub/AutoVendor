def dashboard(request):
    user = request.user
    context = {
        'user': user,
        'cars': getattr(user, 'cars', []),
        'chats': getattr(user, 'chats', []),
        'receipts': getattr(user, 'receipts', []),
        'notifications': getattr(user, 'notifications', []),
        'activities': getattr(user, 'activities', []),
    }
    return render(request, 'dashboard.html', context)

def my_cars(request):
    user = request.user
    context = {
        'user': user,
        'cars': getattr(user, 'cars', []),
    }
    return render(request, 'my_cars.html', context)

def chats(request):
    user = request.user
    context = {
        'user': user,
        'chats': getattr(user, 'chats', []),
    }
    return render(request, 'chats.html', context)

def receipts(request):
    user = request.user
    context = {
        'user': user,
        'receipts': getattr(user, 'receipts', []),
    }
    return render(request, 'receipts.html', context)

def settings(request):
    user = request.user
    return render(request, 'settings.html', {'user': user})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
# import openai, os
from .models import Car, CustomUser
from .forms import CarForm

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password1")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Login successful!")
            return redirect("index")
        else:
            messages.error(request, "Invalid email/username or password.")
    return render(request, "login.html")

def logout(request):
    auth.logout(request)
    messages.success(request, "Logout successful!")
    return redirect("index")

def about(request):
    return render(request, 'about.html')

def privacypolicy(request):
    return render(request, 'privacypolicy.html')

def termsandconditions(request):
    return render(request, 'termsandconditions.html')

def cars(request):
    return render(request, 'cars.html')

def service(request):
    return render(request, 'service.html')

def team(request):
    return render(request, 'team.html')

def feature(request):
    return render(request, 'feature.html')

def contact(request):
    return render(request, 'contact.html')

def blog(request):
    return render(request, 'blog.html')

def testimonial(request):
    return render(request, 'testimonial.html')

def password_reset(request):
    return render(request, 'password_reset.html')

def password_reset_confirm(request):
    return render(request, 'password_reset_confirm.html')

def password_reset_done(request):
    return render(request, 'password_reset_done.html')

def password_reset_complete(request):
    return render(request, 'password_reset_complete.html')

def inspect(request):
    return render(request, 'inspect.html')

def user_profile(request):
    user = request.user
    # Example: Replace with actual related_name or query for chats, receipts, notifications, activities, cars
    context = {
        'user': user,
        'chats': getattr(user, 'chats', []),
        'receipts': getattr(user, 'receipts', []),
        'notifications': getattr(user, 'notifications', []),
        'activities': getattr(user, 'activities', []),
        'cars': getattr(user, 'cars', []),
    }
    return render(request, 'user_profile.html', context)

def page_not_found(request):
    return render(request, '404.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('register')
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('register')
        user = CustomUser.objects.create_user(username=username, email=email, password=password1)
        user.save()
        user = authenticate(request, username=username, password=password1)
        if user is not None:
            auth.login(request, user)
            messages.success(request, f"Welcome {username}, your account has been created successfully!")
            return redirect('index')
    return render(request, 'register.html')

def sell_car(request):
    return render(request, 'sell_car.html')

def user_profile_update(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name  = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.bio = request.POST.get('bio')
        user.phone = request.POST.get('phone')
        user.address = request.POST.get('address')
        user.job_title = request.POST.get('job_title')
        if request.FILES.get('profile_image'):
            user.profile_image = request.FILES['profile_image']
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('user_profile')
    return render(request, 'user_profile.html')

@csrf_exempt
def stream_chat(request):
    if request.method == "POST":
        user_msg = request.POST.get("message")
        def event_stream():
            try:
                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": user_msg}],
                    stream=True
                )
                for chunk in response:
                    if "choices" in chunk:
                        delta = chunk["choices"][0]["delta"].get("content")
                        if delta:
                            yield f"data: {smart_str(delta)}\n\n"
            except Exception as e:
                yield f"data: [Error: {str(e)}]\n\n"
        return StreamingHttpResponse(event_stream(), content_type="text/event-stream")

def car_list(request):
    cars = Car.objects.all()
    return render(request, 'cars/car_list.html', {'cars': cars})

def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'cars/car_detail.html', {'car': car})

def car_upload(request):
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('car_list')
    else:
        form = CarForm()
    return render(request, 'cars/car_upload.html', {'form': form})


def service(request):
    return render(request, 'service.html')


def team(request):
    return render(request, 'team.html')

def car_list(request):
    cars = Car.objects.all()
    return render(request, 'car_list.html', {'cars': cars})


def feature(request):
    return render(request, 'feature.html')

def car_upload(request):
    return render(request, 'car_upload.html')
    cars = Car.objects.all()
    return render(request, 'car_list.html', {'cars': cars})


def contact(request):
    return render(request, 'contact.html')


def blog(request):
    return render(request, 'blog.html')


def testimonial(request):
    return render(request, 'testimonial.html')


def password_reset(request,):
    return render(request, 'password_reset.html')

def password_reset_confirm(request,):
    return render(request, 'password_reset_confirm.html')

def password_reset_done(request,):
    return render(request, 'password_reset_done.html')

def password_reset_complete(request,):
    return render(request, 'password_reset_complete.html')

def inspect(request):
        return render(request, 'inspect.html')
        
def service(request):
        return render(request, 'service.html')

def user_profile(request):
    return render(request, 'user_profile.html')

def page_not_found(request):
        return render(request, '404.html') 



        from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import authenticate

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Check passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('register')

        # Create user
        user = CustomUser.objects.create_user(username=email, email=email, password=password1)
        user.save()

        # Authenticate and log the user in
        user = authenticate(request, username=email, password=password1)
        if user is not None:
            auth.login(request, user)
            messages.success(request, f"Welcome {username}, your account has been created successfully!")
            return redirect('index')  # Change 'index' to your homepage name

    return render(request, 'register.html')

def sell_car(request):
    return render(request, 'sell_car.html')



from django.contrib import messages
from django.shortcuts import render, redirect

def user_profile_update(request):
    if request.method == 'POST':
        user = request.user

        # If you actually have a full_name field in your model
        user.first_name = request.POST.get('first_name')
        user.last_name  = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.bio = request.POST.get('bio')
        user.phone = request.POST.get('phone')
        user.address = request.POST.get('address')

        if request.FILES.get('profile_image'):
            user.profile_image = request.FILES['profile_image']

        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('user_profile')

    return render(request, 'user_profile.html')

from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
import openai, os



@csrf_exempt
def stream_chat(request):
    if request.method == "POST":
        user_msg = request.POST.get("message")

        def event_stream():
            try:
                # Use OpenAI streaming
                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": user_msg}],
                    stream=True
                )
                for chunk in response:
                    if "choices" in chunk:
                        delta = chunk["choices"][0]["delta"].get("content")
                        if delta:
                            yield f"data: {smart_str(delta)}\n\n"
            except Exception as e:
                yield f"data: [Error: {str(e)}]\n\n"

        return StreamingHttpResponse(event_stream(), content_type="text/event-stream")

from django.shortcuts import render, get_object_or_404, redirect
from .models import Car
from .forms import CarForm

def car_list(request):
    cars = Car.objects.all()
    return render(request, 'cars/car_list.html', {'cars': cars})

def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'cars/car_detail.html', {'car': car})

def car_upload(request):
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('car_list')
    else:
        form = CarForm()
    return render(request, 'cars/car_upload.html', {'form': form})

from django.db.models import Q

def car_list(request):
    query = request.GET.get('q')
    brand = request.GET.get('brand')
    year = request.GET.get('year')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    cars = Car.objects.all()

    if query:
        cars = cars.filter(
            Q(name__icontains=query) | 
            Q(brand__icontains=query) | 
            Q(description__icontains=query)
        )

    if brand:
        cars = cars.filter(brand__icontains=brand)

    if year:
        cars = cars.filter(year=year)

    if min_price:
        cars = cars.filter(price__gte=min_price)

    if max_price:
        cars = cars.filter(price__lte=max_price)

    return render(request, 'cars/car_list.html', {
        'cars': cars,
        'query': query,
        'brand': brand,
        'year': year,
        'min_price': min_price,
        'max_price': max_price,
    })

    from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib import messages
from django.http import JsonResponse
from .forms import (
    UserUpdateForm, 
    NotificationSettingsForm,
    PrivacySettingsForm,
    AccountSettingsForm,
    AppearanceSettingsForm,
    CarForm
)

User = get_user_model()

@login_required
def settings_view(request):
    # Get the active tab from the request
    active_tab = request.GET.get('tab', 'profile')
    
    # Initialize all forms
    user_form = UserUpdateForm(instance=request.user)
    notification_form = NotificationSettingsForm(instance=request.user)
    privacy_form = PrivacySettingsForm(instance=request.user)
    account_form = AccountSettingsForm(instance=request.user)
    appearance_form = AppearanceSettingsForm(instance=request.user)
    
    context = {
        'active_tab': active_tab,
        'user_form': user_form,
        'notification_form': notification_form,
        'privacy_form': privacy_form,
        'account_form': account_form,
        'appearance_form': appearance_form,
    }
    
    return render(request, 'settings/settings.html', context)

@login_required
def user_profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(
            request.POST, 
            request.FILES, 
            instance=request.user
        )
        
        if user_form.is_valid():
            user_form.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Profile updated successfully!'
                })
            else:
                messages.success(request, 'Your profile has been updated!')
                return redirect('settings')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Error updating profile. Please check your inputs.',
                    'errors': user_form.errors.get_json_data()
                })
            else:
                messages.error(request, 'Error updating profile. Please check your inputs.')
    
    return redirect('settings')

@login_required
def update_notification_settings(request):
    if request.method == 'POST':
        form = NotificationSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Notification settings updated successfully!'
                })
            else:
                messages.success(request, 'Notification settings updated!')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Error updating notification settings.'
                })
            else:
                messages.error(request, 'Error updating notification settings.')
    
    return redirect('settings')

@login_required
def update_privacy_settings(request):
    if request.method == 'POST':
        form = PrivacySettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Privacy settings updated successfully!'
                })
            else:
                messages.success(request, 'Privacy settings updated!')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Error updating privacy settings.'
                })
            else:
                messages.error(request, 'Error updating privacy settings.')
    
    return redirect('settings')

@login_required
def update_account_settings(request):
    if request.method == 'POST':
        form = AccountSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Account settings updated successfully!'
                })
            else:
                messages.success(request, 'Account settings updated!')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Error updating account settings.'
                })
            else:
                messages.error(request, 'Error updating account settings.')
    
    return redirect('settings')

@login_required
def update_appearance_settings(request):
    if request.method == 'POST':
        form = AppearanceSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Appearance settings updated successfully!'
                })
            else:
                messages.success(request, 'Appearance settings updated!')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Error updating appearance settings.'
                })
            else:
                messages.error(request, 'Error updating appearance settings.')
    
    return redirect('settings')

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Check if current password is correct
        if not request.user.check_password(current_password):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Current password is incorrect.'
                })
            else:
                messages.error(request, 'Current password is incorrect.')
            return redirect('settings')
        
        # Check if new passwords match
        if new_password != confirm_password:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'New passwords do not match.'
                })
            else:
                messages.error(request, 'New passwords do not match.')
            return redirect('settings')
        
        # Check password strength (optional)
        if len(new_password) < 8:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Password must be at least 8 characters long.'
                })
            else:
                messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('settings')
        
        # Change password
        request.user.set_password(new_password)
        request.user.save()
        
        # Update session to prevent logout
        update_session_auth_hash(request, request.user)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Password changed successfully!'
            })
        else:
            messages.success(request, 'Password changed successfully!')
            return redirect('settings')
    
    return redirect('settings')