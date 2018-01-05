from django.conf.urls import url
from core.api.routers import PostHackedRouter
from . import views

router = PostHackedRouter()
router.include_root_view = False

# reverse('api:report-list'), reverse('api:report-detail', kwargs={'pk': 1})
router.register(r'report', views.MonthlyReportViewSet, base_name='report')

urlpatterns = [

]

urlpatterns += router.urls
