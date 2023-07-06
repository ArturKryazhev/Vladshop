from django.urls import path
from . import views

urlpatterns = [
    path('',views.mainPage,name='base'),
    path('notebooks/<str:post_slug>/',views.notebookView, name = 'notebook_detail'),
    path('smartphones/<str:post_slug>/',views.smartphoneView, name = 'smartphone_detail'),
    path('cart',views.CartView, name = 'cart'),
    path('AddToCart/<str:slug>/', views.AddToCartView, name='AddToCart'),
    path('AddToCartViewSmartphone/<str:slug>', views.AddToCartViewSmartphone, name = 'AddToCartViewSmartphone'),
    path('CartEditNotebook/<str:pk>',views.CartEditNotebook, name = 'CartEditNotebook'),
    path('CartEditSmartphone/<str:pk>', views.CartEditSmartphone, name = 'CartEditSmartphone'),
    path('checkout', views.CheckoutView, name = 'checkout'),
    path('make-order', views.MakeOrderView,name ='make-order')
]
