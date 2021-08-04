import requests
import csv

cards = []

def get_pagination():
	url='https://ekb.roscarservis.ru/catalog/legkovye/?form_id=catalog_filter_form&filter_mode=params&sort=asc&filter_type=tires&arCatalogFilter_415=&arCatalogFilter_416=&arCatalogFilter_417=&arCatalogFilter_431=&arCatalogFilter_433=&arCatalogFilter_440=&arCatalogFilter_430=&arCatalogFilter_432=&arCatalogFilter_434=&arCatalogFilter_438=&arCatalogFilter_439=&car_brand=&car_model=&car_year=&car_mod=&arCatalogFilter_458_1500340406=Y&set_filter=Y&isAjax=true&'
	headers={
		'Accept' : 'application/json, text/javascript, */*; q=0.01',
		'X-Requested-With': 'XMLHttpRequest',
		'X-Is-Ajax-Request': 'X-Is-Ajax-Request',
		'user-agent' : 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
	}

	response = requests.get(url, headers=headers)
	data = response.json()
	pagination = int(data['pageCount'])

	return pagination

def get_data(page):
	url = f'https://ekb.roscarservis.ru/catalog/legkovye/?form_id=catalog_filter_form&filter_mode=params&sort=asc&filter_type=tires&arCatalogFilter_415=&arCatalogFilter_416=&arCatalogFilter_417=&arCatalogFilter_431=&arCatalogFilter_433=&arCatalogFilter_440=&arCatalogFilter_430=&arCatalogFilter_432=&arCatalogFilter_434=&arCatalogFilter_438=&arCatalogFilter_439=&car_brand=&car_model=&car_year=&car_mod=&arCatalogFilter_458_1500340406=Y&set_filter=Y&isAjax=true&PAGEN_1={page}'
	headers={
		'Accept' : 'application/json, text/javascript, */*; q=0.01',
		'X-Requested-With': 'XMLHttpRequest',
		'X-Is-Ajax-Request': 'X-Is-Ajax-Request',
		'user-agent' : 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
	}

	response = requests.get(url, headers=headers)
	data = response.json()
	items = data['items']

	for item in items:
		# getting item information

		name = item['name']
		price = item['price']
		url = 'https://ekb.roscarservis.ru/catalog' + item['url']

		# fixing site trouble
		if int(item['amount']) == 0:
			try:
				amount = item['fortochkiStores'][0]['AMOUNT']
			except:
				amount = item['commonStores'][0]['AMOUNT']
		elif int(item['amount']) == 1000:
			try:
				amount = item['fortochkiStores'][0]['AMOUNT']
			except:
				amount = item['commonStores'][0]['AMOUNT']
		else:
			amount = item['amount']

		# adding item information to dict
		cards.append(
			{
				'Name'   : name,
				'Price'  : price,
				'Amount' : amount,
				'Url'    : url
			}
		)

def main():
	# creating csv headers
	with open('data.csv', 'w', newline = '') as file:
		writer = csv.writer(file, delimiter = ' ')
		writer.writerow(
			(
				'Name',
				'Price',
				'Amount',
				'Url'
			)
		)

	# parsing information
	max_pagination = get_pagination()
	for page in range(1, max_pagination + 1):
		get_data(page)
		print(f'[INFO] Processed page {page}')

	# writing items information in csv file
	with open('data.csv', 'a', newline = '', encoding='utf-8') as file:
		writer = csv.writer(file, delimiter = ' ')
		for card in cards:
			writer.writerow(
				(
					card['Name'],
					card['Price'],
					card['Amount'],
					card['Url']
				)
			)

if __name__=='__main__':
	main()