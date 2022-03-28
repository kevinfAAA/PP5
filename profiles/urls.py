from django.urls import path
from .views import ProfileView, UpdateProfile, newsletter_signup, newsletter_unsubscribe

urlpatterns = [
    path('<int:pk>/', ProfileView.as_view(), name='profile'),
    path('<int:pk>/update/', UpdateProfile.as_view(), name='update-profile'),
    path('news-signup/', newsletter_signup, name='news_sign_up'),
    path('news-unsubscribe/', newsletter_unsubscribe, name='news_unsubscribe'),
]
