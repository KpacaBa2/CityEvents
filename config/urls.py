from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('users/', include(('apps.users.urls', 'users'), namespace='users')),
    path('events/', include(('apps.events.urls', 'events'), namespace='events')),
    path('venues/', include(('apps.venues.urls', 'venues'), namespace='venues')),
    path('organizers/', include(('apps.organizers.urls', 'organizers'), namespace='organizers')),
    path('tickets/', include(('apps.tickets.urls', 'tickets'), namespace='tickets')),
    path('orders/', include(('apps.orders.urls', 'orders'), namespace='orders')),
    path('categories/', include(('apps.categories.urls', 'categories'), namespace='categories')),
    path('tags/', include(('apps.tags.urls', 'tags'), namespace='tags')),
    path('reviews/', include(('apps.reviews.urls', 'reviews'), namespace='reviews')),
    path('favorites/', include(('apps.favorites.urls', 'favorites'), namespace='favorites')),
    path('api/', include(('apps.api.urls', 'api'), namespace='api')),
    path('', include(('apps.pages.urls', 'pages'), namespace='pages')),
]

handler404 = 'apps.pages.views.page_not_found'
handler500 = 'apps.pages.views.server_error'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
