from rest_framework import routers

from todo_app.base.views import UserViewSet
from todo_app.tasks.views import TaskViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, 'users')
router.register(r'tasks', TaskViewSet, 'tasks')
