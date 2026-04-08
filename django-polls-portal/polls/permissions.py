from django.contrib.auth.models import Group


def user_has_role(user, role_name: str) -> bool:
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return Group.objects.filter(user=user, name=role_name).exists()


def is_creator(user) -> bool:
    return user_has_role(user, "creator")


def is_reviewer(user) -> bool:
    return user_has_role(user, "reviewer")
