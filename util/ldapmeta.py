import ldap

def get_user_metadata(username):
  try:
    ldap_conn = ldap.initialize('ldap://cluster.ldap.ccs.neu.edu/')
  except ldap.LDAPError, e:
    return {} 

  result = ldap_conn.search_s('ou=people,dc=ccs,dc=neu,dc=edu',
      ldap.SCOPE_ONELEVEL,
      '(uid=%s)' % username)

  if len(result):
    (dn, info) = result[0]
    email = info['mail'][0]
    name = info['displayName'][0].split(' ')
    first_name = name[0]
    last_name = name[-1]

  return { 'email'  : email,
           'fname'  : first_name,
           'lname'  : last_name, }

