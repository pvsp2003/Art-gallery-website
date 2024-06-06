"""registration URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('placeorder/',views.Placeorder,name='placeorder'),
    path('home/',views.HomePage,name='home'),
    path('logout/',views.LogoutPage,name='logout'),
    path('painterhome/',views.PainterHomePage,name='painterhome'),
    path('aboutus/',views.aboutus,name='aboutus'),
    path('viewfeedback/',views.Viewfeedback,name='viewfeedback'),
    path('viewcustomize/',views.Viewcustomize,name='viewcustomize'),
    path('contact/',views.contact,name='contact'),
    path('cartsave/',views.cartsave,name='cartsave'),
    path('customize/',views.Customize,name='customize'),
    path('uploadpainting/',views.Uploadpainting,name='uploadpainting'),
    path('remove-item-from-cart/', views.remove_item_from_cart, name='remove_item_from_cart'),
    path('payment/', views.payment_page, name='payment'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('vieworders/', views.Vieworders, name='vieworders'),
    path('deletequery/<qid>',views.Deletequery,name='deletequery'),
    path('deleteorder/<oid>',views.deleteorder,name='deleteorder'),
    path('deletepainting/<pid>',views.Deletepainting,name='deletepainting'),
    path('updaterating/<pid>,<str:prating>',views.updaterating,name='updaterating'),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="reset_password.html"),
         name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="reset.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"),
         name="password_reset_complete"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
