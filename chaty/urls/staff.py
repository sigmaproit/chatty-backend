from rest_framework import routers

from chaty.views.staff import StaffMessageView

router = routers.SimpleRouter()
router.register(r'', StaffMessageView, '')
router.register(r'(?P<customer_user_id>[-\w]+)', StaffMessageView, '')
urlpatterns = router.urls
