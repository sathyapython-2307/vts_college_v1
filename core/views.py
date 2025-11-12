from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, JsonResponse
from django.conf import settings as django_settings
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
try:
    import razorpay
except Exception:
    razorpay = None
import json
import logging

# Ensure project root is on sys.path so we can reliably import razorpay_config
import sys
import os as _os
project_root = _os.path.dirname(_os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import razorpay_config.get_config robustly. We prefer importlib to give clearer errors
try:
    import importlib
    razorpay_cfg_mod = importlib.import_module('razorpay_config')
    get_config = getattr(razorpay_cfg_mod, 'get_config', None)
except Exception:
    # If import fails, set get_config to None so views will fall back to settings.
    get_config = None

logger = logging.getLogger(__name__)

from .models import (
    HeroBanner, Section, AboutPage, AboutSection, FeatureCard,
    HomeAboutSection, CourseCategory, CourseBrowser, Course,
    LearningBanner, WhyChoose, CertificateSection, Testimonial,
    TestimonialStrip, FAQQuestion, CourseBrochure,
    CoursePayment, CourseAccess, Certificate
)
from .models_brochure import BrochureDownload

from .models import (
    HeroBanner, Section, AboutPage, AboutSection, FeatureCard, 
    HomeAboutSection, CourseCategory, CourseBrowser, Course,
    LearningBanner, WhyChoose, CertificateSection, Testimonial, 
    TestimonialStrip, FAQQuestion, CourseBrochure
)


def home(request):
    """Render the home page with dynamic content managed from admin.

    Provides:
    - hero_banner: single active HeroBanner instance or None
    - sections: queryset of active Section instances (each gets .active_contents)
    - feature_cards: queryset of active FeatureCard instances
    - home_about: single active HomeAboutSection instance or None
    - course_categories: queryset of active CourseCategory instances
    - course_browsers: queryset of active CourseBrowser instances
    """
    hero_banner = HeroBanner.objects.filter(is_active=True).order_by('-updated_at').first()
    sections = Section.objects.filter(is_active=True).order_by('order')
    feature_cards = FeatureCard.objects.filter(is_active=True).order_by('order')
    home_about = HomeAboutSection.objects.filter(is_active=True).order_by('-updated_at').first()
    course_categories = CourseCategory.objects.filter(is_active=True).order_by('order')
    course_browsers = CourseBrowser.objects.filter(is_active=True).order_by('order')
    courses = Course.objects.filter(is_active=True).order_by('order')
    why_choose = WhyChoose.objects.filter(is_active=True).order_by('-updated_at').first()

    # If why_choose exists, split each item's text into label and description
    if why_choose:
        # Only include active items, ordered by 'order'
        items = why_choose.items.filter(is_active=True).order_by('order')
        for item in items:
            if item.text:
                # Split at first period, or first linebreak if no period
                if '.' in item.text:
                    label, desc = item.text.split('.', 1)
                    item.label = label.strip()
                    item.description = desc.strip()
                elif '\n' in item.text:
                    label, desc = item.text.split('\n', 1)
                    item.label = label.strip()
                    item.description = desc.strip()
                else:
                    item.label = item.text.strip()
                    item.description = ''
        why_choose.active_items = items

    # Attach active_contents to each section for template convenience
    for section in sections:
        section.active_contents = section.contents.filter(is_active=True).order_by('order')

    context = {
        'hero_banner': hero_banner,
        'sections': sections,
        'feature_cards': feature_cards,
        'home_about': home_about,
        'course_categories': course_categories,
        'course_browsers': course_browsers,
        'courses': courses,
        'learning_banner': LearningBanner.objects.filter(is_active=True).order_by('-updated_at').first(),
        'why_choose': why_choose,
        'certificate_section': CertificateSection.objects.filter(is_active=True).order_by('-updated_at').first(),
        'testimonials': Testimonial.objects.filter(is_active=True).order_by('order'),
        'faqs': FAQQuestion.objects.filter(is_active=True).order_by('order'),
    }

    # Add all active testimonial strips to the context
    testimonial_strips = TestimonialStrip.objects.filter(is_active=True).order_by('order')
    context['testimonial_strips'] = testimonial_strips

    return render(request, 'home.html', context)

def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('signup')
        
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.save()
        
        # Automatically authenticate and log the user in after successful signup
        authenticated_user = authenticate(request, username=user.username, password=password)
        if authenticated_user is not None:
            login(request, authenticated_user)
            messages.success(request, 'Account created successfully! You are now logged in.')
            return redirect('home')
        else:
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
    
    return render(request, 'registration/signup.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid password')
                return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email')
            return redirect('login')
    
    return render(request, 'registration/login.html')

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def my_purchase(request):
    """
    Display the user's purchased courses and achievements.
    Shows all active courses and certificates that the user has access to.
    """
    # Get the active tab from query parameters or default to 'courses'
    active_tab = request.GET.get('tab', 'courses')
    
    # Get all active course access records for the user with related data
    course_accesses = CourseAccess.objects.filter(
        user=request.user,
        is_active=True,
        course__is_active=True  # Only show active courses
    ).select_related(
        'course'  # Efficiently load course data
    ).prefetch_related(
        '_progress',  # Load progress data
        '_progress__certificate'  # Load certificate data
    )

    # Get all certificates earned by the user
    certificates = Certificate.objects.filter(
        course_progress__course_access__user=request.user,
        course_progress__is_completed=True
    ).select_related(
        'course_progress__course_access__course'
    ).order_by('-issue_date')
    
    # Include course purchase cards in the query
    course_accesses = course_accesses.prefetch_related('course__purchase_card')
    
    context = {
        'course_accesses': course_accesses,
        'certificates': certificates,
        'active_tab': active_tab
    }
    
    return render(request, 'my_purchase.html', context)

@login_required
def settings(request):
    return render(request, 'settings.html')

def about(request):
    """Render the about page with dynamic AboutPage and AboutSection content."""
    about_page = AboutPage.objects.filter(is_active=True).order_by('-updated_at').first()
    about_sections = AboutSection.objects.filter(is_active=True).order_by('order')

    context = {
        'about_page': about_page,
        'about_sections': about_sections,
    }

    return render(request, 'about.html', context)

def contact(request):
    return render(request, 'contact.html')

def privacy(request):
    return render(request, 'privacy.html')

def terms(request):
    return render(request, 'terms.html')

def team(request):
    return render(request, 'team.html')

def testimonials(request):
    return render(request, 'testimonials.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')

@login_required
def download_brochure(request, course_slug):
    """
    Handle downloading of course brochure with user information tracking.
    """
    course = get_object_or_404(Course, slug=course_slug, is_active=True)
    brochure = get_object_or_404(CourseBrochure, course=course, is_active=True)
    
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            # Create brochure download record
            BrochureDownload.objects.create(
                user_name=request.POST.get('user_name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                course=course,
                brochure=brochure,
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            return FileResponse(brochure.brochure_file, as_attachment=True, 
                             filename=f"{course.name}_brochure.pdf")
        except Exception as e:
            logger.error(f"Brochure download error: {str(e)}")
            return JsonResponse({'error': 'Failed to process download'}, status=500)
    else:
        messages.error(request, "Please fill out the form to download the brochure.")
        return redirect('course_detail', slug=course_slug)

def course_detail(request, slug):
    """
    Display the details of a specific course.
    """
    course = get_object_or_404(Course, slug=slug, is_active=True)
    related_courses = Course.objects.filter(
        category=course.category,
        is_active=True
    ).exclude(id=course.id)[:3]  # Get 3 related courses
    # Prepare instructor lists for the template to avoid calling queryset methods
    # inside the template (TemplateLanguage cannot parse chained calls with args).
    local_instructors = course.local_instructors.filter(is_active=True).order_by('order')
    course_instructors = course.courseinstructor_set.select_related('instructor').order_by('order')

    context = {
        'course': course,
        'related_courses': related_courses,
        'local_instructors': local_instructors,
        'course_instructors': course_instructors,
        'course_features': course.features.all(),
        'course_skills': course.skills.filter(is_active=True).order_by('order'),
        'course_tools': course.tools.filter(is_active=True).order_by('order'),
        'course_overviews': course.overviews.filter(is_active=True).order_by('order'),
        'brochure': CourseBrochure.objects.filter(course=course, is_active=True).first(),
    }
    # Determine if the current logged-in user already has access to this course
    try:
        has_access = False
        if request.user.is_authenticated:
            has_access = CourseAccess.objects.filter(user=request.user, course=course, is_active=True).exists()
    except Exception:
        # If anything goes wrong while checking access, default to False
        has_access = False

    context['has_access'] = has_access
    return render(request, 'course_detail.html', context)

def course_checkout(request, slug):
    """
    Display the checkout page for a course.
    """
    course = get_object_or_404(Course, slug=slug, is_active=True)
    # If the user is not authenticated, redirect them to the signup page
    # (non-logged-in users may browse product pages but must register to purchase)
    if not request.user.is_authenticated:
        return redirect('signup')
    context = {
        'course': course,
    }
    return render(request, 'checkout/checkout.html', context)

@login_required
def create_order(request, slug):
    """
    Create a Razorpay order for the course.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    course = get_object_or_404(Course, slug=slug, is_active=True)

    try:
        # Parse JSON data from request
        data = json.loads(request.body)

        # Save form data in session
        form_fields = {
            'first_name': 'checkout_first_name',
            'last_name': 'checkout_last_name',
            'email': 'checkout_email',
            'phone': 'checkout_phone',
            'address': 'checkout_address',
            'city': 'checkout_city',
            'state': 'checkout_state',
            'zip': 'checkout_zip'
        }
        for field, session_key in form_fields.items():
            request.session[session_key] = data.get(field)

        # Get configuration from settings - use direct references
        # Get configuration from settings using getattr for safety
        razorpay_settings = getattr(django_settings, 'RAZORPAY_SETTINGS', {})
        enabled = getattr(django_settings, 'RAZORPAY_ENABLED', False)
        key_id = getattr(django_settings, 'RAZORPAY_KEY_ID', '')
        key_secret = getattr(django_settings, 'RAZORPAY_KEY_SECRET', '')
        currency = getattr(django_settings, 'RAZORPAY_CURRENCY', 'INR')

        # Print debug info
        print("\nDEBUG: Razorpay Settings:")
        print("-" * 50)
        print(f"Settings dict = {razorpay_settings}")
        print(f"ENABLED = {enabled}")
        print(f"KEY_ID = {key_id}")
        print(f"KEY_SECRET length = {len(key_secret) if key_secret else 0}")
        print(f"CURRENCY = {currency}")
        print("-" * 50)

        # Debug logging for troubleshooting
        # Log configuration details
        logger.debug('Razorpay Configuration:')
        logger.debug(f'- Package Available: {razorpay is not None}')
        logger.debug(f'- Settings Enabled: {razorpay_settings.get("ENABLED", False)}')
        logger.debug(f'- Effective Enabled: {enabled}')
        logger.debug(f'- KEY_ID: {key_id}')
        logger.debug(f'- KEY_SECRET length: {len(key_secret) if key_secret else 0}')
        logger.debug(f'- Currency: {currency}')

        # Log the actual configuration being used
        logger.info(f"Using Razorpay config: ENABLED={enabled}, KEY_ID={key_id}, CURRENCY={currency}")
        if django_settings.DEBUG:
            print('DEBUG: create_order using config:', {
                'ENABLED': enabled,
                'KEY_ID': key_id,
                'SECRET': '*' * 4 if key_secret else None,
                'CURRENCY': currency
            })

        if razorpay is None:
            logger.error('Razorpay package not available')
            resp = {'error': 'Payment gateway not available'}
            if django_settings.DEBUG:
                resp['debug'] = {'reason': 'razorpay package not installed'}
            return JsonResponse(resp, status=500)

        razorpay_settings = getattr(django_settings, 'RAZORPAY_SETTINGS', {})
        if not razorpay_settings.get('ENABLED', False):
            logger.error('Razorpay is disabled in settings')
            resp = {'error': 'Payment gateway not configured'}
            if django_settings.DEBUG:
                resp['debug'] = {
                    'reason': 'razorpay is disabled in settings',
                    'settings': razorpay_settings
                }
            return JsonResponse(resp, status=500)

        if not key_id or not key_secret:
            logger.error('Razorpay credentials missing')
            resp = {'error': 'Payment gateway not configured'}
            if settings.DEBUG:
                resp['debug'] = {
                    'KEY_ID_present': bool(key_id),
                    'KEY_SECRET_present': bool(key_secret),
                    'reason': 'missing credentials'
                }
            return JsonResponse(resp, status=500)

        # Initialize Razorpay client
        try:
            if 'razorpay' not in globals() or razorpay is None:
                logger.error('Razorpay package not installed')
                return JsonResponse({'error': 'Payment gateway not available'}, status=500)

            # Log what we're using to init the client
            if getattr(settings, 'DEBUG', False):
                print('DEBUG: Initializing Razorpay client with:', {
                    'key_id': key_id,
                    'key_secret': '*' * 4 if key_secret else None
                })
            client = razorpay.Client(auth=(key_id, key_secret))
            
            # Test the client by fetching payments (lightweight API call)
            client.payment.all({'count': 1})
            logger.info('Razorpay client initialized and tested successfully')
            
        except Exception as e:
            logger.exception('Razorpay client initialization/test failed')
            resp = {'error': 'Payment gateway configuration error'}
            if getattr(settings, 'DEBUG', False):
                resp['debug'] = {
                    'exception': str(e),
                    'key_id': key_id,
                    'key_secret_present': bool(key_secret)
                }
            return JsonResponse(resp, status=500)

        # Convert price to paise (Razorpay expects amount in smallest currency unit)
        try:
            amount = int(float(course.discounted_price) * 100)
            if amount <= 0:
                raise ValueError('Course price must be greater than 0')
        except (ValueError, TypeError) as e:
            logger.error(f'Invalid course price: {str(e)}')
            return JsonResponse({'error': 'Invalid course price'}, status=400)

        # Create Razorpay order
        try:
            order_data = {
                'amount': amount,
                'currency': currency,
                'payment_capture': 1,
                'notes': {
                    'course_id': course.id,
                    'course_name': course.name,
                    'user_id': request.user.id,
                    'user_email': data.get('email'),
                    'user_phone': data.get('phone')
                }
            }
            order = client.order.create(data=order_data)
            logger.info(f'Razorpay order created: {order}')
            return JsonResponse({
                'id': order['id'],
                'amount': order['amount'],
                'currency': order['currency'],
                'key': key_id
            })
        except Exception as e:
            logger.exception('Error creating Razorpay order')
            resp = {'error': 'Failed to create payment order'}
            if getattr(settings, 'DEBUG', False):
                resp['debug'] = {'exception': str(e)}
            return JsonResponse(resp, status=500)

    except json.JSONDecodeError:
        logger.error('Invalid JSON data received')
        return JsonResponse({'error': 'Invalid form data'}, status=400)
    except Exception as e:
        logger.error(f'Unexpected error: {str(e)}')
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

@csrf_exempt
@login_required
def payment_callback(request, slug):
    """
    Handle Razorpay payment callback.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    course = get_object_or_404(Course, slug=slug, is_active=True)
    
    try:
        # Get configuration from settings using getattr for safety
        enabled = getattr(django_settings, 'RAZORPAY_ENABLED', False)
        key_id = getattr(django_settings, 'RAZORPAY_KEY_ID', '')
        key_secret = getattr(django_settings, 'RAZORPAY_KEY_SECRET', '')
        currency = getattr(django_settings, 'RAZORPAY_CURRENCY', 'INR')

        if razorpay is None:
            logger.error('Razorpay package not installed')
            return JsonResponse(
                {'error': 'Payment gateway not available', 'detail': 'razorpay package not installed'},
                status=500
            )

        if not enabled:
            logger.error('Razorpay is not enabled')
            return JsonResponse(
                {'error': 'Payment gateway not configured', 'detail': 'razorpay is disabled'},
                status=500
            )

        if not key_id or not key_secret:
            logger.error('Razorpay credentials missing')
            return JsonResponse(
                {'error': 'Payment gateway not configured', 'detail': 'missing credentials'},
                status=500
            )

        # Initialize Razorpay client
        client = razorpay.Client(auth=(key_id, key_secret))
        
        # Parse and validate request data
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            logger.error('Invalid JSON in request body')
            return JsonResponse(
                {'error': 'Invalid request format', 'detail': 'invalid JSON'},
                status=400
            )

        # Validate required parameters
        required_params = ['razorpay_payment_id', 'razorpay_order_id', 'razorpay_signature']
        missing_params = [param for param in required_params if not data.get(param)]
        if missing_params:
            logger.error(f'Missing required parameters: {missing_params}')
            return JsonResponse(
                {'error': 'Invalid request format', 'detail': f'missing parameters: {missing_params}'},
                status=400
            )
        
        params_dict = {
            'razorpay_payment_id': data.get('razorpay_payment_id'),
            'razorpay_order_id': data.get('razorpay_order_id'),
            'razorpay_signature': data.get('razorpay_signature')
        }
        
        try:
            logger.info(f'Verifying payment: order_id={params_dict["razorpay_order_id"]}, payment_id={params_dict["razorpay_payment_id"]}')
            
            # Verify payment signature
            client.utility.verify_payment_signature(params_dict)
            logger.info('Payment signature verified successfully')
            
            # Fetch payment details to verify status
            payment_details = client.payment.fetch(params_dict['razorpay_payment_id'])
            if payment_details.get('status') != 'captured':
                logger.error(f'Payment not captured. Status: {payment_details.get("status")}')
                return JsonResponse(
                    {'error': 'Payment not completed', 'detail': 'payment not captured'},
                    status=400
                )
            
            # Get or create payment record
            payment = CoursePayment.objects.filter(order_id=params_dict['razorpay_order_id']).first()
            if not payment:
                payment = CoursePayment(
                    user=request.user,
                    course=course,
                    order_id=params_dict['razorpay_order_id'],
                    payment_id=params_dict['razorpay_payment_id'],
                    amount=course.discounted_price,
                    currency='INR',
                    first_name=request.session.get('checkout_first_name', ''),
                    last_name=request.session.get('checkout_last_name', ''),
                    email=request.session.get('checkout_email', ''),
                    phone=request.session.get('checkout_phone', ''),
                    address=request.session.get('checkout_address', ''),
                    city=request.session.get('checkout_city', ''),
                    state=request.session.get('checkout_state', ''),
                    zip_code=request.session.get('checkout_zip', ''),
                    status='successful'
                )
                payment.save()
            
            # Grant course access
            CourseAccess.objects.get_or_create(
                user=request.user,
                course=course,
                defaults={
                    'payment': payment,
                    'is_active': True
                }
            )
            
            # Clear checkout session data
            checkout_fields = [
                'checkout_first_name', 'checkout_last_name', 'checkout_email',
                'checkout_phone', 'checkout_address', 'checkout_city',
                'checkout_state', 'checkout_zip'
            ]
            for field in checkout_fields:
                request.session.pop(field, None)
            
            messages.success(request, 'Payment successful! You now have access to the course.')
            return JsonResponse({
                'status': 'success',
                'redirect_url': reverse('my-purchase')  # Add URL to redirect to
            })
            
        except razorpay.errors.SignatureVerificationError as e:
            logger.error(f'Payment signature verification failed: {str(e)}')
            return JsonResponse(
                {'error': 'Payment verification failed', 'detail': 'invalid signature'},
                status=400
            )
        except Exception as e:
            logger.exception('Error processing payment verification')
            return JsonResponse(
                {'error': 'Payment verification failed', 'detail': str(e)},
                status=400
            )
    
    except Exception as e:
        logger.error(f'Unexpected error in payment callback: {str(e)}')
        return JsonResponse(
            {'error': 'An unexpected error occurred', 'detail': str(e)},
            status=500
        )

def payment_debug(request):
    """
    Development-only endpoint to view effective Razorpay configuration and auth state.
    Returns JSON indicating what the server sees for the current request.
    """
    # Only allow in DEBUG mode
    if not django_settings.DEBUG:
        return JsonResponse({'error': 'Not available in production'}, status=403)

    resp = {
        'request_user_authenticated': request.user.is_authenticated,
        'request_user_username': getattr(request.user, 'username', None) if request.user.is_authenticated else None,
        'DJANGO_SETTINGS_MODULE': __import__('os').environ.get('DJANGO_SETTINGS_MODULE'),
        'RAZORPAY_ENABLED': getattr(django_settings, 'RAZORPAY_ENABLED', False),
        'KEY_ID_present': bool(getattr(django_settings, 'RAZORPAY_KEY_ID', '')),
        'KEY_SECRET_present': bool(getattr(django_settings, 'RAZORPAY_KEY_SECRET', '')),
        'CURRENCY': getattr(django_settings, 'RAZORPAY_CURRENCY', 'INR'),
        'razorpay_package_importable': (razorpay is not None),
    }
    return JsonResponse(resp)