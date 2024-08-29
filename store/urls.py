from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import dash_dashboard
from . import plotly_app


urlpatterns = [
    path('', views.home, name='home'),
    path('orderh', views.orderh, name='orderh'),

    path('about/', views.about, name='about'),
    path('personal/', views.personal, name='personal'),

    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_user/', views.update_user, name='update_user'),

    path('product/<int:pk>', views.product, name='product'),
    path('blog/<int:pk>', views.blog, name='blog'),
    path('order/<int:pk>/', views.order, name='order'),

    path('category/<str:foo>', views.category, name='category'),
    path('category_summary/', views.category_summary, name='category_summary'),
    path("reset_password/", auth_views.PasswordResetView.as_view(template_name='reset_password.html'), name="reset_password"),
    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name='reset_confirm.html'),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name="password_reset_complete",
    ),

    path('create_customer/', views.create_customer, name='create_customer'),

    path('enquiry/', views.enquiry, name='enquiry'),



    path('create_payment_link/', views.create_payment_link, name='create_payment_link'),
    path('create/', views.create_cproduct, name='create_cproduct'),

    path('scrape/', views.scrape_data, name='scrape_data'),
    path('gantt_chart/', views.gantt_chart, name='gantt_chart'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('dash_dashboard/', dash_dashboard, name='dash_dashboard'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('my_view/',  views.my_view, name='my_view'),
    path('services/', views.services, name='services'),



    #path('dash_view/', views.dash_view, name='dash_view'),

    #path('upload_and_analyze/', views.upload_and_analyze, name='upload_and_analyze'),

    #path('dash/', dash_app.app, name='dash'),

    



]
