from django.conf.urls import include, url
from rest_framework.authtoken.views import obtain_auth_token
from board.urls import router
from django.contrib import admin

from board import views
urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^post/',views.insertRecords),
    url(r'^crawler/', views.web_crawler),
    url(r'^$',views.index),
    url(r'^api/token/', obtain_auth_token, name='api-token'),
    url(r'^api/', include(router.urls)),
]
