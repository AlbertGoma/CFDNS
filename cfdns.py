#!/usr/bin/python
import json, httplib, urllib, urllib2, string

host_url	=	'https://api.cloudflare.com/host-gw.html'
user_url	=	'https://api.cloudflare.com/client/v4/'
host_key	=	''
user_key	=	''
email		=	''
zone		=	''
record		=	''
headers		=	{'X-Auth-Email'	: '',
           		'X-Auth-Key'	: '',
           		'Content-Type'	: 'application/json' }
           
values		=	{'act'				: 'user_lookup',
          		'host_key'			: '',
          		'cloudflare_email'	: '' }
zones 		=	{}
records		=	{}


def post(url, data, *arg):
	if len(arg) > 0:
		req = urllib2.Request(url, data, arg[0])
	else:
		req = urllib2.Request(url, data)
	res = json.loads(urllib2.urlopen(req).read())
	if res['result'] == 'success':
		return res['response']
	elif res['success'] == False:
		raise SystemExit(1)
	else:
		return res['result']


def get(url, data, headers):
	res = json.loads(urllib2.urlopen(urllib2.Request(url + '?' + urllib.urlencode(data), None, headers)).read())
	if not res['success']:
		raise SystemExit(1)
	return res['result']


def put(url, data, headers):
	opener = urllib2.build_opener(urllib2.HTTPSHandler)
	request = urllib2.Request(url, data, headers)
	request.get_method = lambda: 'PUT'
	res = json.loads(opener.open(request).read())
	return res['result']


def delete(url, data, headers):
	opener = urllib2.build_opener(urllib2.HTTPSHandler)
	request = urllib2.Request(url, data, headers)
	request.get_method = lambda: 'DELETE'
	res = json.loads(opener.open(request).read())
	return res['result']



def edit_record(isnew):
	values = {}
	while 1:
		values['type'] = raw_input("Type (A, AAAA, CNAME, TXT, SRV...): ")
		values['name'] = raw_input("Name: ")
		values['content'] = raw_input("Content: ")
		sel = raw_input("TTL: ")
		if sel:
			values['ttl'] = int(sel)
		elif 'ttl' in values:
			del values['ttl']
		sel = raw_input("Priority: ")
		if sel:
			values['priority'] = int(sel)
		elif 'priority' in values:
			del values['priority']
		sel = raw_input("Proxied (True/False): ")
		if sel:
			values['proxied'] = (sel == 'True')
		elif 'proxied' in values:
			del values['proxied']
		print("\nRecord:\n")
		for k, v in values.iteritems():
			print(k + ": " + str(v))
		sel = raw_input("OK? (Y/N/B/X):")
		if sel == 'Y':
			if isnew:
				post(user_url + 'zones/' + zone + '/dns_records', json.dumps(values), headers)
			else:
				put(user_url + 'zones/' + zone + '/dns_records/' + record, json.dumps(values), headers)
			break
		elif sel == 'B':
			break
		elif sel == 'X':
			raise SystemExit(0)



def menu_records():
	while 1:
		global records, record
		records = get(user_url + 'zones/' + zone + '/dns_records', '', headers)
		print('\n#\tRecord\t\t\tType\tContent\t\tProxied\tTTL\n---------------------------------------------------------------')
		for i, v in enumerate(records):
			print(str(i) + '\t' + v['name'] + '\t' + v['type'] + '\t' + v['content'] + '\t' + str(v['proxied']) + '\t' + str(v['ttl']))
		print("\nOptions:\nN\t(new)\nE\t(edit)\nD\t(delete)\nB\t(back)\nX\t(exit)")
		sel = raw_input("\nOption: ")
		if sel == 'B':
			break
		elif sel == 'X':
			raise SystemExit(0)
		elif sel == 'N':
			edit_record(True)
		elif sel == 'E':
			sel = raw_input("\nRecord #: ")
			if sel.isdigit() and len(records) > int(sel) and int(sel) >= 0:
				record = records[int(sel)]['id']
				edit_record(False)
		elif sel == 'D':
			sel = raw_input("\nRecord #: ")
			if sel.isdigit() and len(records) > int(sel) and int(sel) >= 0:
				record = records[int(sel)]['id']
				delete(user_url + 'zones/' + zone + '/dns_records/' + record, '', headers)


def menu_zones():
	while 1:
		global zones, zone
		zones = get(user_url + 'zones', '', headers)
		print('\n#\tStatus\t\tZone\n-----------------------------------------')
		for i, v in enumerate(zones):
			print(str(i) + '\t' + v['status'] + '\t\t' + v['name'])
		print("\nB\t(back)\nX\t(exit)")
		sel = raw_input("\nZone #: ")
		if sel == 'B':
			break
		elif sel == 'X':
			raise SystemExit(0)
		elif sel.isdigit() and len(zones) > int(sel) and int(sel) >= 0:
			zone = zones[int(sel)]['id']
			print("\nSelected Zone: " + zones[int(sel)]['name'] + "\nName Servers: " + zones[int(sel)]['name_servers'][0] + " " + zones[int(sel)]['name_servers'][1])
			menu_records()


def menu_mail():
	while 1:
		global email, values, user_key, headers, zones
		email = raw_input("Client Email: ")
		if email == 'B':
			break
		elif email == 'X':
			raise SystemExit(0)
		values['host_key'] = host_key
		values['cloudflare_email'] = email
		res = post(host_url, urllib.urlencode(values))
		user_key = res['user_api_key']
		headers['X-Auth-Email'] = email
		headers['X-Auth-Key'] = user_key
		menu_zones()



def menu():
	while 1:
		global host_key, values
		host_key = raw_input("API key: ")
		if not all(c in string.hexdigits for c in host_key):
			break
		menu_mail()

menu()
