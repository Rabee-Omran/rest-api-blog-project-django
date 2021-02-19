from django.contrib import admin
from django.urls import path,include
from blog import views
from django.conf.urls.static import static
from django.conf import settings


#doc 1
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='My Blog API' )

#doc 2,3
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view2 = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service=" ",
      contact=openapi.Contact(email="rabeeomran2@gnail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
  
    path('admin/', admin.site.urls),
 

    #api
    #############################3
    path('api/v1/', include('blog.api_urls')),

   # path('api/v1/auth/', include('rest_framework.urls'))
    path('api/v1/auth/login/', views.LoginView.as_view()),
    path('api/v1/auth/logout/', views.LogoutView.as_view()),

    #doc 1
    #bad docs :) -- need to fix (staticfiles) to (static) in /site-packages/rest_framework_swagger/templates/rest_framework_swagger/index.html, error at line 2
    path('api_docs/', schema_view),

    #doc 2,3
    path('', schema_view2.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api_docs3/', schema_view2.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
