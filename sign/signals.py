from django.contrib.auth.models import Group
from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import social_account_added
from django.dispatch import receiver


# Add all new users (third-party or email) to the "common" group
@receiver(user_signed_up)
def add_user_to_common_group_on_signup(sender, request, user, **kwargs):
    """
    Assigns users to the 'common' group when they sign up.
    Triggered for both email/password and social signups.
    """
    common_group, created = Group.objects.get_or_create(name='common')
    if not user.groups.filter(name='common').exists():
        user.groups.add(common_group)
        user.save()


# Add third-party users to the 'common' group when social account is added
@receiver(social_account_added)
def add_social_user_to_common_group(sender, request, sociallogin, **kwargs):
    """
    Assigns third-party users to the 'common' group.
    Triggered when a social account is linked during registration.
    """
    user = sociallogin.user  # Get the social user
    common_group, created = Group.objects.get_or_create(name='common')
    if not user.groups.filter(name='common').exists():
        user.groups.add(common_group)
        user.save()
