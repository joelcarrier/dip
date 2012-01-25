from PIL import Image
import uuid
import os
import zipfile
import dicom
convert = local_import('convert')
import time
import subprocess
import sys
import traceback

# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
    redirect(URL(f='patient'))

def error():
    return dict()

@auth.requires_login()
def sequence():
    #form = SQLFORM.smartgrid(db.sequence,onupdate=auth.archive,paginate=None,columns=['patient','date','name','modality','protocol'],linked_tables=['sequence_image','sequence_report'])
    #form = SQLTABLE(db(db.sequence.id>0).select(db.sequence.ALL),columns=['sequence.modality','sequence.patient','sequence.name','sequence.protocol','sequence.date'],truncate=64,orderby=True)
    sequences = []
    if request.args(0):
      sequences = db(db.sequence.patient==request.args(0)).select()
    else:
      for m in db(db.permission.user==auth.user_id).select():
        for s in db(db.sequence.patient==m.patient).select():
          sequences.append(s)
    
    return locals()

@auth.requires_login()
def sequence_image_manage():
    form = SQLFORM.smartgrid(db.sequence_image,onupdate=auth.archive,linked_tables=['sequence'])
    return locals()

@auth.requires_login()
def manage_permission():
    form = SQLFORM.smartgrid(db.permission,onupdate=auth.archive,linked_tables=[])
    return locals()

@auth.requires_login()
def manage_user():
    form = SQLFORM.smartgrid(db.auth_user,onupdate=auth.archive,linked_tables=['permission','auth_membership'])
    return locals()

def body(row):
  return row
@auth.requires_login()
def patient():
#    patient_form = SQLFORM.grid(db.patient,editable=False,deletable=False,onupdate=auth.archive,columns=['patient.hid','patient.name','patient.sex','patient.date_of_birth','sequence.modality','sequence.name','sequence.protocol','sequence.date'],user_signature=False)#,links=[{'header':'LINK','body':body}])
#    if request.args(2):
#      sequence_form = SQLTABLE(db(db.sequence.patient==request.args(2)).select(),links=[{'header':'LINK','body':body}])
#    else:
#      sequence_form = None
    
    patients = []
    if (auth.has_membership(role="admin")):
      patients = db(db.patient.id>0).select()
    else:
      for m in db(db.permission.user==auth.user_id).select():
        patients.append(db.patient[m.patient])
    
    return locals()

@auth.requires_login()
def upload_manage():
    return dict()

@auth.requires_login()
def manage_data():
    form = SQLFORM.smartgrid(db.data,onupdate=auth.archive)
    return locals()

@auth.requires_login()
def view_sequence():
    sequence = db.sequence[request.args(0)]
    images = db(db.sequence_image.sequence==sequence).select()
    reports = db(db.sequence_report.sequence==sequence).select()
    return locals()
    
def process_data():
  try:
    workdir = os.path.join(request.folder,'scratch/'+str(uuid.uuid4()))
    datum = db.data(request.args(0)) or redirect(URL('error'))
    log = datum.log
    if log == None:
      log = ""
    file = datum.file
    z = zipfile.ZipFile(os.path.join(request.folder,'uploads/'+datum.file), 'r')
    names = z.namelist()
    for name in names:
      try:
       f = z.extract(name,workdir)
       filename = os.path.join(workdir,name)
       log = log + "\nprocessing "+filename
       ds = dicom.read_file(filename)
       patient_name = ds.get('PatientsName')
       patient_id = ds.PatientID
       patient_date_of_birth = ds.get('PatientsBirthDate')
       patient_gender = ds.get('PatientsSex')
       modality = ds.get('Modality')
       description = ds.StudyDescription
       protocol = ds.get('ProtocolName')
       study_date = ds.get('StudyDate')
       stream = open(filename,'rb')
       image_filename = filename+'.png'
       thumbnail_filename = filename+'.jpg'
       istream = None
       tstream = None
       try:
         log = log + "\n"+request.folder+"/dicom2/dicom2 -p1 "+filename
         subprocess.call(request.folder+"/dicom2/dicom2 -p1 \"" + filename+"\"",shell=True)
         subprocess.call("convert -resize 64x64 \"" + image_filename+'\" \"'+thumbnail_filename+"\"",shell=True)
         subprocess.call("convert -resize 512x512 \"" + image_filename+'\" \"'+image_filename+"\"",shell=True)
         istream = open(image_filename,'rb')
         tstream = open(thumbnail_filename,'rb')
       except Exception,e:
         log = log + "\n"+str(e)
         pass
       patient = db(db.patient.hid==patient_id).select().first()
       if patient == None:
         patient_id = db.patient.insert(name=patient_name,hid=patient_id,date_of_birth=patient_date_of_birth,sex=patient_gender)
         patient = db.patient(patient_id)
       sequence = db((db.sequence.name==description) & (db.sequence.protocol==protocol) & (db.sequence.date==study_date) & (db.sequence.patient==patient)).select().first()
       if sequence == None:
         sequence_id = db.sequence.insert(name=description,patient=patient,modality=modality,description=description,protocol=protocol,date=study_date)
         sequence = db.sequence(sequence_id)
       if istream == None:
        #id = db.sequence_image.insert(dicom_file=db.sequence_image.dicom_file.store(stream,filename),sequence=sequence)
        pass
       else:
        id = db.sequence_image.insert(image_full=db.sequence_image.image_full.store(istream,image_filename),image_thumbnail=db.sequence_image.image_thumbnail.store(tstream,thumbnail_filename),dicom_file=db.sequence_image.dicom_file.store(stream,filename),sequence=sequence,metadata=str(ds))
      except Exception,e:
        log = log + "\n"+ traceback.format_exc()
        pass
  except Exception,e:
       log = log + "\n"+str(e)
       return dict(e=e,t=traceback.format_exc())
  datum.update_record(log = log,processed=True)  
  redirect(URL('sequence_manage'))
