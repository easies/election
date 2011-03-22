from django.contrib.auth.models import User
from django.conf import settings
from .utils import get_user_metadata
import ldap


class LDAPAuthBackend(object):

    @staticmethod
    def ldap_match(username, password):
        try:
            # Connect to LDAP
            conn = ldap.initialize(settings.LDAP_URI)
            conn.start_tls_s()
            # Try to bind as the user.
            result = conn.simple_bind_s(settings.LDAP_BIND % username, password)
            # Check the result code (for 97).
            return result[0] == ldap.RES_BIND
        except ldap.LDAPError as e:
            return False

    def authenticate(self, username=None, password=None):
        if not username or not password:
            return
        info = get_user_metadata(username)
        if not info:
            return
        if self.ldap_match(username, password):
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_unusable_password()
                info = get_user_metadata(username)
                user.email = info['email']
                user.first_name = info['first_name']
                user.last_name = info['last_name']
                user.save()
            return user

    def get_user(self, user_id):
        return User.objects.get(pk=user_id)
