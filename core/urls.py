from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('course/<slug:slug>/checkout/', views.course_checkout, name='course_checkout'),
    path('course/<slug:slug>/create-order/', views.create_order, name='create_order'),
    path('course/<slug:slug>/payment-callback/', views.payment_callback, name='payment_callback'),
    path('course/<slug:course_slug>/brochure/', views.download_brochure, name='download_brochure'),
    path('course/<slug:slug>/', views.course_detail, name='course_detail'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('my-purchase/', views.my_purchase, name='my-purchase'),
    path('settings/', views.settings, name='settings'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('team/', views.team, name='team'),
    path('testimonials/', views.testimonials, name='testimonials'),
    # Dev-only debug endpoint to inspect Razorpay settings during a browser session
    path('payment-debug/', views.payment_debug, name='payment_debug'),
]