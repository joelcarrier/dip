response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description
response.menu = []

patients = []

response.menu.append((T('Patient'),URL('default','patient')==URL(),URL('default','patient'),[]))

#response.menu.append((T('Sequence'),URL('default','sequence')==URL(),URL('default','sequence'),[]))

if (auth.has_membership(role="admin")):
  admin_menu_items = []
  admin_menu_items.append((T('Users'),URL('default','manage_user')==URL(),URL('default','manage_user'),[]))
  admin_menu_items.append((T('Permissions'),URL('default','manage_permission')==URL(),URL('default','manage_permission'),[]))
  admin_menu_items.append((T('Data'),URL('default','manage_data')==URL(),URL('default','manage_data'),[]))
  response.menu.append((T('Admin'),URL('default','admin')==URL(),URL('default','admin'),admin_menu_items))
