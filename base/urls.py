from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('addtocart/<int:id>',addtocart,name='addtocart'),
    path('cart/',cart,name='cart'),
    path('remove/<int:id>',remove,name='remove'),
    path('increment/<int:id>',increment,name='increment'),
    path('decrement/<int:id>',decrement,name='decrement')
]