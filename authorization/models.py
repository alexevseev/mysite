from django.contrib.auth.models import User


class MyUser(User):
    class Meta:
        proxy = True