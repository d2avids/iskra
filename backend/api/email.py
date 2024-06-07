import os
from django.conf import settings
from djoser.email import PasswordResetEmail

class CustomPasswordReset(PasswordResetEmail):

  template_name = os.path.join(settings.BASE_DIR, 'templates', 'email', 'password_reset.html')

  def __init__(self, email, user, context=None, *args, **kwargs):
    site_url=(
      context.get('site_url', settings.DEFAULT_SITE_URL)
      if context else settings.DEFAULT_SITE_URL
    )
    self.email = email
    self.user = user
    self.context = context if context else{
      'user': self.user,
      'site_name': 'iskra',
      'site_url': site_url,
      'expiration_days': 1,
      'domain': site_url,
      'protocol': 'https',
    }