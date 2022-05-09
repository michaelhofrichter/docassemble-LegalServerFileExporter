import requests
import json
import docassemble.base.functions
from docassemble.base.util import log, DAFile 
import string

__all__ = ['get_file_list_from_legalserver', 'get_file_from_legalserver', 'search_matter_details']


def search_matter_details(legalserver_site_abbreviation, results='full', case_id=0, case_number='', cause_number='', client_email_address='', date_of_birth='', first='', intake_office='', intake_program='', last='', legal_problem_code='', case_disposition='', custom_fields=[]):
    apiuser = docassemble.base.functions.get_config('legalserver').get(legalserver_site_abbreviation).get('username')
    apipassword = docassemble.base.functions.get_config('legalserver').get(legalserver_site_abbreviation).get('password')
    url = "https://" + legalserver_site_abbreviation + ".legalserver.org/api/v1/matters" 
    header_content = {'Content-Type': 'application/json'}
    queryparam = {"results": results}
    pdata = {}
    if case_id != 0:
        pdata['case_id'] = case_id
    if case_number != '':
        pdata['case_number'] = case_number
    if cause_number != '':
        pdata['cause_number'] = cause_number
    if client_email_address != '':
        pdata['client_email_address'] = client_email_address
    if date_of_birth != '':
        pdata['date_of_birth'] = date_of_birth
    if first != '':
        pdata['first'] = first
    if intake_office != '':
        pdata['intake_office'] = intake_office
    if intake_program != '':
        pdata['intake_program'] = intake_program
    if last != '':
        pdata['last'] = last
    if legal_problem_code != '':
        pdata['legal_problem_code'] = legal_problem_code
    payload_data = json.dumps(pdata)
    if len(custom_fields) > 0:
        # note that custom_fields needs to be set up like "[\"good_story_text_4\"]"
        custom_fields_string = "["
        custom_fields_count = 0
        for item in custom_fields:
            custom_fields_string += "\\\"" + str(item) + "\\\""
            custom_fields_count += 1
            if custom_fields_count < len(custom_fields):
                custom_fields_string += ", "
        custom_fields_string += "]"
        payload_data = payload_data[:-1]
        if len(payload_data) > 1:
            payload_data + ", "
        payload_data = payload_data + "\"custom_fields\": \"" + custom_fields_string + "\" }"
        log("custom field string: " + custom_fields_string)
        
    
    try: 
        response = requests.get(url, data=payload_data, params=queryparam, headers=header_content, auth=(apiuser, apipassword))
    except: 
        log("Error searching LegalServer Matter data for " + payload_data + " on " + legalserver_site_abbreviation + ". Exception raised.")        
        return {'error': 'exception'}
    if response.status_code != 200:
        return_data = {'error': response.status_code}
        log("Error searching LegalServer Matter data for " + payload_data + " on " + legalserver_site_abbreviation + ". " + str(response.status_code) + ": " + str(response.json()))        
    else:
        log("Got LegalServer Search Matter data for " + payload_data + " on " + legalserver_site_abbreviation + ". Response " + str(response.status_code))
        return_data = response.json().get('data')
    return return_data


def get_file_list_from_legalserver(legalserver_site_abbreviation, case_uuid):
    apiuser = docassemble.base.functions.get_config('legalserver').get(legalserver_site_abbreviation).get('username')
    apipassword = docassemble.base.functions.get_config('legalserver').get(legalserver_site_abbreviation).get('password')
    url = "https://" + legalserver_site_abbreviation + ".legalserver.org/api/v1/matters/" + case_uuid + "/documents"
    header_content = {'Content-Type': 'application/json'}

    try: 
        response = requests.get(url, headers=header_content, auth=(apiuser, apipassword))
        if response.status_code != 200 and response.status_code != 201:
            log("Error getting LegalServer file list  for " + case_uuid + " on " + legalserver_site_abbreviation + ". Exception raised. " + str(response.status_code) + ": " + str(response.json()))           
            return {'error': 'exception'}
        log("Success getting LegalServer file list for " + case_uuid + " on + " + legalserver_site_abbreviation + ". " + str(response.status_code) + ": " + str(response.json()))
        return_data = response.json()
    except: 
        log("Error getting LegalServer file list  for " + case_uuid + " on " + legalserver_site_abbreviation + ". Exception raised. " + str(response.status_code))         
        return {'error': 'exception'}
    return return_data

def get_file_from_legalserver(legalserver_site_abbreviation, document_uuid, document_name):
    apiuser = docassemble.base.functions.get_config('legalserver').get(legalserver_site_abbreviation).get('username')
    apipassword = docassemble.base.functions.get_config('legalserver').get(legalserver_site_abbreviation).get('password')
    url = "https://" + legalserver_site_abbreviation + ".legalserver.org/modules/document/download.php"
    queryparams = {"unique_id": document_uuid }
    header_content = {'Content-Type': 'application/json'}
    for character in string.punctuation:
        if character != '_' and character != '-' and character != '(' and character != ')' and character != '.':
            document_name = document_name.replace(character, '')
    document_name = document_name.replace(' ', '_')
    the_file = DAFile()
    the_file.set_random_instance_name()
    the_file.initialize(filename=document_name)
    try: 
        response = requests.get(url, headers=header_content, params=queryparams, auth=(apiuser, apipassword))
        if response.status_code != 200 and response.status_code != 201:
            log("Error getting LegalServer file  for " + document_uuid + ", named " + document_name + " on " + legalserver_site_abbreviation + ". Exception raised. " + str(response.status_code) + ": " + str(response.json()))           
            return {'error': 'exception'}
        # if response.headers.get('content-length', None) != None:
        #    open(the_file.path(), 'wb').write(response.content)
        open(the_file.path(), 'wb').write(response.content)
        the_file.commit()
        return the_file
    except: 
        log("Error getting LegalServer file  for " + document_uuid + ", named " + document_name + " on " + legalserver_site_abbreviation + ". Exception raised. " + str(response.status_code))           
        return {'error': 'exception'}
    
