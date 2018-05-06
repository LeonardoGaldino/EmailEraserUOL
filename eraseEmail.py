# built-in imports
import json
from os import getenv

# external imports
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = getenv('API_URL')

COOKIE_STR = getenv('COOKIE_STR')

json_get_100_str = '{"commands":[{"command_name":"mail:list","command_id":"svi","params":{"accountId":"0","folder_name":"INBOX","page":"1","limit":100,"sort_terms":"ARRIVAL","order":"DESC","search_terms":"","flag":false},"account_id":"0"}]}'
json_get_100_obj = json.loads(json_get_100_str)

cookie_dict = {
	'_webmail_session_id': COOKIE_STR
}

req_session = requests.Session()

def fetch_next_100_emails():
	try:
		emails_req = req_session.get(API_URL, cookies=cookie_dict, json=json_get_100_obj)
		emails_json = json.loads(emails_req.content)
	except Exception as e:
		raise e

	if emails_json.get('message') != 'ok':
		raise ValueError('Fetch e-mails request not successful!')

	return emails_json

def erase_emails(email_id_list):
	json_erase_100_obj = {
		'commands': [{
			'command_name': 'mail:delete',
			'command_id': 'ali',
			'params': {
				'folders': [{'name': 'INBOX', 'uids': email_id_list}],
				'accountId': '0',
			},
			'accountId': '0'
		}]
	}
	try:
		erase_req = req_session.post(API_URL, cookies=cookie_dict, json=json_erase_100_obj)
		erase_json = json.loads(erase_req.content)
	except Exception as e:
		raise e

	if erase_json.get('message') != 'ok':
		raise ValueError('Erase e-mails request not successful!')

def erase_inbox_uol():
	while True:
		try:
			emails_json = fetch_next_100_emails()
		except Exception as e:
			print 'Error occurred when fetching next emails:'
			print e
			break

		num_emails = int(emails_json.get('results')[0].get('result').get('properties').get('totalMessages'))
		print(str(num_emails) + ' emails left')

		if(num_emails == 0):
			print 'No more emails, ending script.'
			break

		emails = emails_json.get('results')[0].get('result').get('items')
		ids = [email.get('id') for email in emails]
		try:
			erase_emails(ids)
			print(str(num_emails) + ' erased successfully')
		except Exception as e:
			print 'Error occurred when deleting next emails:'
			print e
			break

if __name__ == '__main__':
	erase_inbox_uol()