from urllib.request import urlopen
from urllib.request import build_opener
from xml.etree import ElementTree as et
import xml.etree.ElementTree as xmlParser
import pprint

def members_field_xml_to_json(url):
	opener=build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	rootElement = None
	json_data={}
	with opener.open(url) as file:
		xmlDoc = xmlParser.parse(file)
		rootElement = xmlDoc.getroot()
	
	for contact in rootElement.iter('contact_information'):
		for member in contact.iter('member'):
			json_data['firstName']=member.find('last_name').text
			json_data['lastName']=member.find('first_name').text
			json_data['fullName']=json_data['firstName'] + " " + json_data['lastName']
			json_data['chartId']=member.find('bioguide_id').text
			json_data['mobile']=member.find('phone').text
			address = member.find('address').text.split()
			json_data['address']=[{
				"street":" ".join(address[:-3]),
				"city": " ".join(address[-3:-1]),
				"state": None,
				"postal": address[-1]
			}]
			pp = pprint.PrettyPrinter(indent=4)
			pp.pprint(json_data)


if __name__=="__main__":
	url="https://www.senate.gov/general/contact_information/senators_cfm.xml"
	members_field_xml_to_json(url)
