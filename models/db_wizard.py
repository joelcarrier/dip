

########################################
db.define_table('patient',
    Field('hid', type='string',
          label=T('Hid')),
    Field('name', type='string',
          label=T('Name')),
    Field('sex', type='string',
          label=T('Sex')),
    Field('date_of_birth', type='string',
          label=T('Date Of Birth')),
    auth.signature,
    format='%(hid)s',
    migrate=settings.migrate)

db.define_table('patient_archive',db.patient,Field('current_record','reference patient',readable=False,writable=False))

db.define_table('permission',
    Field('patient',type='reference patient'),
    Field('user',type='reference auth_user'),
    auth.signature,
    migrate=settings.migrate)
db.define_table('permission_archive',db.permission,Field('current_record','reference permission',readable=False,writable=False))

########################################
db.define_table('sequence',
    Field('name', type='string',
          label=T('Name')),
    Field('description', type='string',
          label=T('Description')),
    Field('protocol', type='string',
          label=T('Protocol')),
    Field('modality', type='string',
          label=T('Modality')),
    Field('date', type='datetime',
          label=T('Date')),
    Field('patient', type='reference patient',
          label=T('Patient')),
    auth.signature,
    format='%(name)s',
    migrate=settings.migrate)

db.define_table('sequence_archive',db.sequence,Field('current_record','reference sequence',readable=False,writable=False))

########################################
db.define_table('sequence_note',
    Field('sequence', type='reference sequence',
          label=T('Scan')),
    Field('text', type='text'),
    auth.signature,
    format='%(sequence)s',
    migrate=settings.migrate)

db.define_table('sequence_note_archive',db.sequence_note,Field('current_record','reference sequence_note',readable=False,writable=False))
########################################
db.define_table('sequence_report',
    Field('sequence', type='reference sequence',
          label=T('Scan')),
    Field('file', type='upload',
          label=T('File')),
    auth.signature,
    format='%(sequence)s',
    migrate=settings.migrate)

db.define_table('sequence_report_archive',db.sequence_report,Field('current_record','reference sequence_report',readable=False,writable=False))

########################################
db.define_table('sequence_image',
    Field('sequence', type='reference sequence',
          label=T('Scan')),
    Field('dicom_file', type='upload',
          label=T('Dicom File')),
    Field('image_thumbnail', type='upload',
          label=T('Image Thumbnail')),
    Field('image_full', type='upload',
          label=T('Image Full')),
    Field('metadata', type='text',
          label=T('Meta Data')),
    auth.signature,
    format='%(sequence)s',
    migrate=settings.migrate)

db.define_table('sequence_image_archive',db.sequence_image,Field('current_record','reference sequence_image',readable=False,writable=False))

########################################
db.define_table('data',
    Field('file', type='upload',
          label=T('File')),
    Field('processed', type='boolean',
          label=T('Processed')),
    Field('log', type='text',
          label=T('Process Log')),
    auth.signature,
    format='%(file)s',
    migrate=settings.migrate)

db.define_table('data_archive',db.data,Field('current_record','reference data',readable=False,writable=False))
