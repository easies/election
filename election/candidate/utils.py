import ldap
from django.conf import settings


def get_user_metadata(username):
    """
    Query LDAP for user information.
    :param username: The username.
    :returns: A dict containing email, first_name, last_name. If user is
        not found returns None.
    """
    conn = ldap.initialize(settings.LDAP_URI)
    result = conn.search_s(settings.LDAP_DN, ldap.SCOPE_ONELEVEL,
        '(uid=%s)' % username)
    if len(result):
        (dn, info) = result[0]
        email = info['mail'][0]
        name = info['displayName'][0].split(' ')
        first_name = name[0]
        last_name = ' '.join(name[1:])
        return {
            'email': email,
            'first_name': first_name,
            'last_name': last_name
        }
