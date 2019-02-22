# Repurposed from https://github.com/Nitrogen-DCPPC/FAIRshake/blob/master/scripts/dockstore_assessment.py

import os
import re
import sys
import json
import itertools
from pyswaggerclient import SwaggerClient
from pyswaggerclient.fetch import fetch_spec, parse_spec
from merging import prompt_select_dups

# Configure API credentials for FAIRshake
#  FAIRshake allows you to get your API_KEY with your USERNAME
#  EMAIL, and PASSWORD if you don't know it currently.
# This script will find it if it isn't provided.

ENV_FILE = os.environ.get('ENV_FILE')
if ENV_FILE is not None:
  for line in open(ENV_FILE, 'r'):
    line_split = line.split('=')
    var = line_split[0]
    val = '='.join(line_split[1:])
    os.environ[var] = val

FAIRSHAKE_API_KEY = os.environ.get('FAIRSHAKE_API_KEY')
FAIRSHAKE_USERNAME = os.environ.get('FAIRSHAKE_USERNAME')
FAIRSHAKE_EMAIL = os.environ.get('FAIRSHAKE_EMAIL')
FAIRSHAKE_PASSWORD = os.environ.get('FAIRSHAKE_PASSWORD')

def get_fairshake_client(api_key=None, username=None, email=None, password=None):
  ''' Using either the api_key directly, or with fairshake
  user credentials, create an authenticated swagger client to fairshake.
  '''
  fairshake = SwaggerClient(
    'https://fairshake.cloud/swagger?format=openapi',
  )
  if not api_key:
    fairshake_auth = fairshake.actions.auth_login_create.call(data=dict({
      'username': username,
      'password': password,
    }, **({'email': email} if email else {})))
    api_key = fairshake_auth['key']
  # FAIRshake expects a Token in the Authorization request header for
  #  authenticated calls
  fairshake.update(
    headers={
      'Authorization': 'Token ' + api_key,
    }
  )
  return fairshake

def register_fairshake_obj_if_not_exists(fairshake, fairshake_obj):
  ''' Register the FAIRshake object, first checking to see if it
  exists in the database. To do this we query the title and url separately
  and present any results to the user. The user is responsible for
  visually inspecting the entry and determining whether or not to add
  the object into FAIRShake.

  We prompt the user (defaulting to NOT add the object) and call the
  FAIRShake digital_object_create api endpoint if they do choose to register
  the object.
  '''
  try:
    existing = fairshake.actions.digital_object_list.call(
      title=fairshake_obj['title'],
    )['results'] + fairshake.actions.digital_object_list.call(
      url=fairshake_obj['url'],
    )['results']
  except:
    existing = []

  for result in prompt_select_dups(*existing, fairshake_obj):
    if result.get('id') is not None:
      print('Updating %s...' % (str(result['id'])))
      id = result['id']
      del result['id']
      try:
        obj = fairshake.actions.digital_object_update.call(id=id, data=result)
      except Exception as e:
        print(e)
    else:
      print('Creating...')
      obj = fairshake.actions.digital_object_create.call(data=result)
      id = obj['id']
  return id

def register_fairshake_assessment(fairshake, answers=None, project=None, rubric=None, target=None):
  ''' Register the assessment if it hasn't yet been registered.
  '''
  print('Registering assessment...', answers)
  try:
    assessment = fairshake.actions.assessment_list.call(
      project=project,
      target=target,
      rubric=rubric,
      methodology='auto',
    )['results'][0]
  except Exception as e:
    print(e)
    assessment = None

  if assessment:
    print('Updating assessment...')
    try:
      assessment = fairshake.actions.assessment_update.call(
        id=assessment['id'],
        data=dict(assessment, answers=answers),
      )
    except Exception as e:
      print(e)
      pass
  else:
    print('Creating assessment...')
    assessment = fairshake.actions.assessment_create.call(
      data=dict(
        project=project,
        target=target,
        rubric=rubric,
        answers=answers,
        methodology='auto',
      )
    )

  return assessment

def register_and_assess_all_objects(fairshake=None):
  ''' Gather all objects passed via stdin.
  Register them in FAIRshake and then assess them.
  '''
  for f in sys.argv[1:]:
    fh = open(f, 'r')
    print('Processing {f}'.format(f=f))
    for obj in map(json.loads, fh.readlines()):
      fairshake_obj = obj['target']
      fairshake_obj_id = register_fairshake_obj_if_not_exists(fairshake, fairshake_obj)
      fairshake_assessment = obj['assessment']
      assessment_result = register_fairshake_assessment(fairshake,
        target=fairshake_obj_id,
        **fairshake_assessment,
      )
      print(assessment_result)

def main():
  ''' Main function of this script. Establish connections to FAIRshake
  and to github with the api keys, if necessary, and then send evaluate
  the github objects with FAIRshake
  '''
  fairshake = get_fairshake_client(
    username=FAIRSHAKE_USERNAME,
    email=FAIRSHAKE_EMAIL,
    password=FAIRSHAKE_PASSWORD,
    api_key=FAIRSHAKE_API_KEY,
  )

  register_and_assess_all_objects(
    fairshake=fairshake,
  )

if __name__ == '__main__':
  main()
