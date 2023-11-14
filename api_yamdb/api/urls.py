from django.urls import include, path

urlpatterns = [
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.jwt')),
    path('api/v1/auth/singup/',),
    path('api/v1/auth/token',),
    path('api/v1/users/me/',),
]
