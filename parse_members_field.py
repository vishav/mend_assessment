from urllib.request import urlopen
from urllib.request import build_opener
from xml.etree import ElementTree as et
import json

def members_field_xml_to_json(url):
	'''
	 With the default opener, I was getting the following error message: 
	 urllib.error.HTTPError: HTTP Error 503: Service Unavailable
	 This is why I created a new opener.
	'''

	opener=build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	rootElement = None
	json_data={}
	with opener.open(url) as file:
		xmlDoc = et.parse(file)
		rootElement = xmlDoc.getroot()
	
	# loop over the 'member' tag within 'contact_information' tag
	# print all values
	for contact in rootElement.iter('contact_information'):
		for member in contact.iter('member'):
			json_data['firstName']=member.find('last_name').text
			json_data['lastName']=member.find('first_name').text
			json_data['fullName']=json_data['firstName'] + " " + json_data['lastName']
			json_data['chartId']=member.find('bioguide_id').text
			json_data['mobile']=member.find('phone').text
			address = member.find('address').text.split()

			# since the location is 'Washington DC', which has no state
			json_data['address']=[{
				"street":" ".join(address[:-3]),
				"city": " ".join(address[-3:-1]),
				"state": None,
				"postal": address[-1]
			}]
			print(json.dumps(json_data, indent=4, sort_keys=True))


if __name__=="__main__":
	url="https://www.senate.gov/general/contact_information/senators_cfm.xml"
	members_field_xml_to_json(url)
