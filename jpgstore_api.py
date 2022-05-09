import requests
import json
from bs4 import BeautifulSoup

def get_collections(search, verified, size):
	url = 'https://server.jpgstoreapis.com/search/collections'
	payload = {
		'nameQuery': search,
		'verified': verified,
		'pagination': '{'+'}',
		'size': str(size)
	}
	response = requests.get(url, params=payload)
	return response

def get_transactions(policy_id, page, count):
	url = f'https://server.jpgstoreapis.com/collection/{policy_id}/transactions'
	payload = {
		'page': str(page),
		'count': str(count)
	}
	response = requests.get(url, params=payload)
	return response

def get_floor(policy_id):
	url = f'https://server.jpgstoreapis.com/collection/{policy_id}/floor'
	response = requests.get(url)
	return response

def get_sales(policy_id, sort, page):
	url = f'https://server.jpgstoreapis.com/policy/{policy_id}/sales'
	payload = {
		'sortBy': sort,
		'page': str(page)
	}
	response = requests.get(url, params=payload)
	return response

def get_listings(policy_id, sort, page):
	url = f'https://server.jpgstoreapis.com/policy/{policy_id}/listings'
	payload = {
		'sortBy': sort,
		'page': str(page)
	}
	response = requests.get(url, params=payload)
	return response

def get_tokens(policy_id, sort, amount, filters):
	url = 'https://server.jpgstoreapis.com/search/tokens'
	payload = {
		'policyIds':f'["{policy_id}"]',
		'saleType':'default',
		'sortBy':sort,
		'traits': json.dumps(filters),
		'nameQuery':'',
		'verified':'default',
		'pagination':'',
		'size':str(amount)
	}
	response = requests.get(url, params=payload)
	return response

def get_listing(listing_id):
	url = f'https://server.jpgstoreapis.com/listing/{listing_id}'
	response = requests.get(url)
	return response

def get_filters(policy_id, build_id):
	url = f'https://www.jpg.store/_next/data/{build_id}/en/collection/{policy_id}.json'
	response = requests.get(url)
	return response

def get_build_id():
	# required for get_filters()
	url = 'https://www.jpg.store/'
	response = requests.get(url)
	soup = BeautifulSoup(response.content, 'html.parser')
	results = soup.find(id="__NEXT_DATA__")
	j = json.loads(results.text)
	return j['buildId']

def get_asset(asset_id):
	url = f'https://server.jpgstoreapis.com/token/{asset_id}'
	response = requests.get(url)
	return response

def get_listing_id(data):
	# filters listing id from returned data.text of get_asset()
	for item in data['listings']:
		for key, value in item.items():
			if key == 'id':
				return value