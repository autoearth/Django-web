
from django.urls import path, include #(include เป็นการเชื่อมต่อ app กับ project เข้าด้วยครับ)
from .views import *


urlpatterns = [
    path('', Home, name = 'home-page'),
    path('about/', About, name = 'about-page'),
    path('contact/', Contact, name='contact-page'),
    path('zasumi/', Zasumi, name='zasumi-page'),
    path('addproduct/', Addproduct, name='addproduct-page'),
    path('allproduct/', Product, name='allproduct-page'),
    path('register/', Register, name='register-page'),
    path('addtocart/<int:pid>/', AddtoCart, name='addtocart-page'),
    path('mycart/', Mycart, name='mycart-page'),
    path('mycart/edit/', MycartEdit, name='mycartedit-page'),
    path('checkout/', Checkout, name='checkout-page'),
    path('orderlist/', OrderListPage, name='orderlist-page'),
    path('allorderlist/', AllOrderListPage, name='allorderlist-page'),
    path('uploadslip/<str:orderid>/', UploadSlip, name='uploadslip-page'),
    path('updatestatus/<str:orderid>/<str:status>/', UpdatePaid, name="updatestatus"),
    path('updatetracking/<str:orderid>/', UpdateTracking, name="updatetracking")
]
