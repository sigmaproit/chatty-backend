from rest_framework import routers

from chaty.views.customer import CustomerMessageView

router = routers.SimpleRouter()
router.register(r'', CustomerMessageView, '')
urlpatterns = router.urls
