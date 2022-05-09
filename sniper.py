import json
import natsort
import streamlit as st
import time
from os import makedirs
from os.path import exists
from jpgstore_api import *

def create_listing(item, count2):
	ipfs = ''
	name = ''
	optimized = ''
	listing_id = ''
	price = ''
	asset_id = ''
	has_price = False
	was_created = False
	for key, value in item.items():
		if key == 'asset_id':
			asset_id = value
		elif key == 'source':
			ipfs = value
		elif key == 'display_name':
			name = value
		elif key == 'optimized_source':
			optimized = value
		elif key == 'listing_lovelace':
			if value != -1:
				has_price = True
			price = '{:.1f}'.format(int(value) * .000001) # convert lovelace to ADA & limit to 1 decimal
	if optimized != '' and optimized!= None and has_price == True:
		asset = get_asset(asset_id)
		listing_id = get_listing_id(json.loads(asset.text))
		create_container(count2, name, listing_id, price, optimized)
		was_created = True
	elif optimized == '' or optimized == None and has_price == True:
		asset = get_asset(asset_id)
		listing_id = get_listing_id(json.loads(asset.text))
		#create_container(count2, name, listing_id, price, f'https://ipfs.io/ipfs/{ipfs}')
		create_container(count2, name, listing_id, price, f'https://images.jpgstoreapis.com/ipfs/{ipfs}')
		was_created = True
	return was_created

def create_container(count2, name, listing_id, price, image):
	link = f'https://www.jpg.store/listing/{listing_id}'
	if f'containter_{count2}' in globals():
		with g[f'containter_{count2}'].container():
			st.image(image)#, caption=item['display_name'])
			st.markdown(f'[{name}]({link})')
			st.write(price)
	else:
		g[f'containter_{count2}'] = st.empty()
		with g[f'containter_{count2}'].container():
			st.image(image)#, caption=item['display_name'])
			st.markdown(f'[{name}]({link})')
			st.write(price)

def update_page(data, search_amount):
	col1, col2, col3, col4 = st.columns(4)
	count, count2, count3 = 0, 0, 0 # keep track of columns, total items, search amount
	for item in data['tokens']:
		if count3 <= (search_amount - 1): #-1 because 0 is counted
			if count == 0:
				with col1:
					# create listing needs to return a value to signify increment yes / no
					was_created = create_listing(item, count2)
					if was_created == True:
						count += 1
						count2 += 1

			elif count == 1:
				with col2:
					was_created = create_listing(item, count2)
					if was_created == True:
						count += 1
						count2 += 1

			elif count == 2:
				with col3:
					was_created = create_listing(item, count2)
					if was_created == True:
						count += 1
						count2 += 1

			elif count == 3:
				with col4:
					was_created = create_listing(item, count2)
					if was_created == True:
						count = 0 # reset column counter
						count2 += 1
			else:
				st.write('Error with Columns')
			
			count3 += 1 # increment search amount counter
		else:
			break

def create_choices():
	choices = {}
	for key, value in st.session_state.items():
		if 'menu' in key and value != []:
			compare = key[4:]
			for attr, elem in st.session_state.items():
				if attr == 'restore' + compare:
					for menu, options in elem.items():
						choices.update({menu: value})

def update_bool():
	st.session_state['run'] = False

st.set_page_config(layout="wide")
st.write('# cNFT Sniper')
st.session_state['run'] = False

policy_id = st.text_input('Policy ID')

col1, col2, col3 = st.columns(3)
with col1:
	interval = st.number_input('Update interval in Seconds', min_value=10, max_value=None, value=20)
with col2:
	search_amount = st.number_input('# of NFTs to Display', min_value=4, max_value=100, value=20)
with col3:
	search_type = st.selectbox('Search Type:', ['recently-listed', 'price-low-to-high', 'price-high-to-low'], index=0)

with st.expander('Filters'):
	create_button = True
	# check for previously created menus and choice selections:
	saved_menu_count = 0
	for key, value in natsort.natsorted(st.session_state.items()):
		if 'restore' in key:
			create_button = False
			snippet = key.replace('restore', 'menu')
			for element, attribute in value.items():
				st.multiselect(element, attribute, key=snippet)
			saved_menu_count += 1

	# Create Retrieve Filters Button
	# Initialization so extends beyond local
	filters = None
	# if create button true, then enable butotn
	if create_button == True:	
		filters = st.button('Retrieve Filters', disabled = False)
	
	# Retrieve Filters
	if filters:
		# Check for Policy ID
		if policy_id != '':
			# strip white space in case of typo / copy paste issue with leading or trailing whitespace
			# need to create a check for valid policy id so not to create empty files !!!!!!!!!!!! - TO DO
			policy_id = policy_id.strip()

			# check if filters directory exists, if not create it
			filters_dir = exists('filters')
			if filters_dir != True:
				makedirs('filters')

			# check if saved filter file exists
			file_exists = exists(f'filters/{policy_id}.json')
			if file_exists != True:
				# if filters file does not exist, create one
				# filters are static / unchanging, creating static file saves unnecessary api calls
				build_id = get_build_id()
				f = get_filters(policy_id, build_id)
				with open(f'filters/{policy_id}.json', 'w') as outfile:
					outfile.write(f.text)
				data = json.loads(f.text)
			else:
				with open(f'filters/{policy_id}.json', 'r') as infile:
					data = json.load(infile)
					
			# Organize Filters for Menus
			filters_list = []
			for key, value in data['pageProps']['collection']['traits'].items():
				filter = {key:[]}
				for item in value:
					filter[key].append(item)
				filters_list.append(filter)

			# Build Filter Menus
			menu_count = 0
			for item in filters_list:
				for key, value in item.items():
					#print(key, value)
					if 'menu'+str(menu_count) not in st.session_state:
						# create restore info for menus
						# need to do this because streamlit menu choice reloads page
						st.session_state['restore'+str(menu_count)] = {key: value}
						# create menu
						st.multiselect(key, value, key='menu'+str(menu_count))
						menu_count += 1
		else:
			st.write('Please Enter a Policy ID')

col1, col2, buf1, buf2 = st.columns(4)
with col1:
	start = st.button('Start')
with col2:
	stop = st.button('Stop', on_click=update_bool())

if start and policy_id != '':
	st.session_state['run'] = True
	g = globals()
	while st.session_state['run']== True:
		# need to get menu choices if exist
		choices = {}
		for key, value in st.session_state.items():
			if 'menu' in key and value != []:
				compare = key[4:]
				for attr, elem in st.session_state.items():
					if attr == 'restore' + compare:
						for menu, options in elem.items():
							choices.update({menu: value})
		
		r = get_tokens(policy_id, search_type, search_amount, choices)
		j = json.loads(r.text)
		update_page(j, search_amount)
		time.sleep(interval)

# TODO:
# clean up code / make more efficient (class objects etc.)
# find way to make stop / update_bool() more effective, doesn't always work
# print total amount of specific trait beside selection in filters
# find optimized source solution i.e. if optimized[0:4] != 'http' or something for images
# need to create a check for valid policy id so not to create empty files
# devise method to load more results if amount returned from /search/tokens contains -1 price listings