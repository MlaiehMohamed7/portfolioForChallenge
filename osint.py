bin/python3

"""
WARNING	this program is for challenge or LEGAL penetration testing only
	and we (the developers and distributors) are not responsible for any misusage

osint is not a python program. it is a python library
you can make a python program from scratch or you can type:
import osint

and then use premade prototypes for developing the osint program

content:
	now 					:	get the current date and time
	documentation			:	automatically used to document every activity used by this program
	get_geolocation 		: 	getting the geolocation of IP address
	ipToHost				:	convert IP to link
	hostToIp				:	convert link to IP
	lookupfor				:	get wide data about target
	whois					:	get info about target using whois program
	portscan				:	looking up for available open ports
	get_exif_data			:	get exif data from a picture
	extract_links			:	looking for links in a webpage
	rainbowAttack			:	looking for the password in a list of possible passwords that matches the hashed image of a target passowrd
	war_dial				:	looking for phone numbers that are used for modems
	phoneNumberToCountry	:	looking for the country that has the phone number
	countryToPhoneNumber	:	looking for the phone number of the mentioned country
"""

import socket
import urllib.request
import json
import subprocess
from PIL import Image
from PIL.ExifTags import TAGS
from urllib.parse import urlparse
from html.parser import HTMLParser
import hashlib
import os
import time
import random
import phonenumbers
from phonenumbers import geocoder, carrier
from ast import literal_eval

def now():
	return time.strftime("%Y-%m-%d_%H:%M:%S")

class documentation:
	logs = []
	fileW = open("documentation.json","a")
    fileR = open("documentation.json","r").read().split(",\n")
    fullList = []
    def __init__(self):
        for i in self.fileR:
            self.fullList.append(literal_eval(i))
	add(self,data):
		self.logs.append(data)
		self.file.write(str(data)+",\n")
        self.fullList.append(data)
	read(self,Number):
		return self.logs[Number]
    readAll(self,Number):
        return fullList[Number]
    def out(self):
        return self.logs
    def outAll(self):
        return self.fullList

document = documentation()


def get_geolocation(ip_address):
    try:
        # Resolve the IP address to a hostname
        hostname = socket.gethostbyaddr(ip_address)[0]
        print(f"Hostname: {hostname}")
        
        # Use an external API to get geolocation data
        url = f"https://ipinfo.io/{ip_address}/json"
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
        
        # Extract latitude and longitude
        loc = data.get("loc", "").split(",")
        latitude = loc[0] if len(loc) > 0 else None
        longitude = loc[1] if len(loc) > 1 else None
        get_geolocation_result = {
            "IP": data.get("ip"),
            "City": data.get("city"),
            "Region": data.get("region"),
            "Country": data.get("country"),
            "Latitude": latitude,
            "Longitude": longitude,
            "Hostname": hostname,
            "googleMapLink":f"google.com/maps/dir/{latitude},{longitude}"
        }
        document.add([now(), "get_geolocation" , ip_address , get_geolocation_result])
        return get_geolocation_result
    except Exception as e:
    	get_geolocation_result = {"error": str(e)}
    	document.add([now(), "get_geolocation" , ip_address , get_geolocation_result])
        return get_geolocation_result
def ipToHost(ipAdress):
	host , aliaslist, addresslist = socket.gethostbyaddr(ipAdress)
	document.add([now(), "ipToHost" , ipAddress , [host , aliaslist,addresslist]])
	return host

def hostToIp(hostAdress):
    try:
        # Get the IP address from the hostname
        hostToIp_result = socket.gethostbyname(hostname)
        document.add([now(),"hostToIp",hostAdress,hostToIp_result])
        return hostToIp_result
    except socket.gaierror:
    	document.add([now(),"hostToIp",hostAdress,"Hostname could not be resolved."])
        return "Hostname could not be resolved."
listOfBrowsers = (  "https://www.facebook.com/",
					"https://www.youtube.com/",
					"https://www.instagram.com/",
					"https://www.whatsapp.com/",
					"https://www.tiktok.com/",
					"https://www.wechat.com/",
					"https://www.messenger.com/",
					"https://telegram.org/",
					"https://www.snapchat.com/",
					"https://www.douyin.com/",
					"https://www.google.com/",
					"https://www.bing.com/",
					"https://www.yahoo.com/",
					"https://www.baidu.com/",
					"https://yandex.com/",
					"https://duckduckgo.com/",
					"https://search.brave.com/",
					"https://www.ecosia.org/",
					"https://www.qwant.com/",
					"https://search.aol.com/")
def lookupfor(target,limit=200,browsers=listOfBrowsers):
	output = []
	for i in browsers:
		output.append(subprocess.run(f"theharvester -d {target} -l {limit} -b {i}",shell=True,capture_output=True,text=True).stdout)
	document.add([now(),"lookupfor",[target,limit,browsers],output])
	return output

def whois(target):
	whois_result = subprocess.run(f"whois {target}",shell=True,capture_output=True,text=True).stdout
	document.add([now(),"whois",target,whois_result])
	return whois_result

def  portscan(target,start=0,end=1024):
    open_ports = []
    
    for port in range(start,end):
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Set a timeout for the connection attempt
        
        # Try to connect to the host and port
        result = sock.connect_ex((target, port))
        
        if result == 0:
            open_ports.append(port)
        
        sock.close()  # Close the socket
    document.add([now(),"portscan",(target,start,end),open_ports])
    return open_ports

def get_exif_data(image_path):

    image = Image.open(image_path)
    
    exif_data = image.getexif()
    

    exif_dict = {}

    for tag_id in exif_data:
        tag_name = TAGS.get(tag_id, tag_id)  # Get the tag name
        exif_dict[tag_name] = exif_data.get(tag_id)  # Store the value
    document.add([now(),"get_exif_data",image_path,exif_dict])
    return exif_dict


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    self.links.append(attr[1])

def extract_links(url):

    parsed_url = urlparse(url)
    connection = http.client.HTTPSConnection(parsed_url.netloc)

    connection.request("GET", parsed_url.path)
    response = connection.getresponse()
    
    html_content = response.read().decode('utf-8')

    parser = LinkParser()
    parser.feed(html_content)

    connection.close()
    document.add([now(),"extract_links",url,parser.links])
    return parser.links



class RainbowTable:
    def __init__(self):
        self.table = {}

    def hash_password(self, password):
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def generate_table(self, passwords):
        """Generate a rainbow table from a list of passwords."""
        for password in passwords:
            hashed = self.hash_password(password)
            self.table[hashed] = password

    def lookup(self, hashed_password):
        """Lookup a hashed password in the rainbow table."""
        return self.table.get(hashed_password, None)


def rainbowAttack(passwords,hashed):

    passwords = open(passwords,"r").read()

    rainbow_table = RainbowTable()
    rainbow_table.generate_table(passwords)
    found_password = rainbow_table.lookup(hashed)
    document.add([now(),"rainbowAttack",[passwords,hashed],found_password])
    return found_password



def war_dial(service_code, exchange_start, exchange_end, min_line, max_line,country_code = "+216"):
	lines = []
    for exchange in range(exchange_start, exchange_end + 1):
        for line in range(min_line, max_line + 1):
            phone_number = f"{country_code}{service_code}{exchange:03}{line:03}"
            try:
                # Parse the phone number
                parsed_number = phonenumbers.parse(phone_number)
                
                # Get the location and carrier
                location = geocoder.description_for_number(parsed_number, "en")
                network = carrier.name_for_number(parsed_number, "en")
                
                lines.append((parsed_number,location,network))
                
                time.sleep(random.uniform(0.5, 2))
                
                # Check if the number is valid
                if is_valid_number(parsed_number):
                    lines.append(parsed_number)
                
                time.sleep(random.uniform(0.5, 2))
                
            except phonenumbers.phonenumberutil.NumberParseException:
                pass

            time.sleep(random.uniform(1, 3))
    document.add([now(),"war_dial",[service_code, exchange_start, exchange_end, min_line, max_line,country_code],lines])
    return lines


countries_with_codes = (
    ("Afghanistan", "+93"),
    ("Albania", "+355"),
    ("Algeria", "+213"),
    ("Andorra", "+376"),
    ("Angola", "+244"),
    ("Antigua and Barbuda", "+1-268"),
    ("Argentina", "+54"),
    ("Armenia", "+374"),
    ("Australia", "+61"),
    ("Austria", "+43"),
    ("Azerbaijan", "+994"),
    ("Bahamas", "+1-242"),
    ("Bahrain", "+973"),
    ("Bangladesh", "+880"),
    ("Barbados", "+1-246"),
    ("Belarus", "+375"),
    ("Belgium", "+32"),
    ("Belize", "+501"),
    ("Benin", "+229"),
    ("Bhutan", "+975"),
    ("Bolivia", "+591"),
    ("Bosnia and Herzegovina", "+387"),
    ("Botswana", "+267"),
    ("Brazil", "+55"),
    ("Brunei", "+673"),
    ("Bulgaria", "+359"),
    ("Burkina Faso", "+226"),
    ("Burundi", "+257"),
    ("Cabo Verde", "+238"),
    ("Cambodia", "+855"),
    ("Cameroon", "+237"),
    ("Canada", "+1"),
    ("Central African Republic", "+236"),
    ("Chad", "+235"),
    ("Chile", "+56"),
    ("China", "+86"),
    ("Colombia", "+57"),
    ("Comoros", "+269"),
    ("Congo, Democratic Republic of the", "+243"),
    ("Congo, Republic of the", "+242"),
    ("Costa Rica", "+506"),
    ("Côte d'Ivoire", "+225"),
    ("Croatia", "+385"),
    ("Cuba", "+53"),
    ("Cyprus", "+357"),
    ("Czechia", "+420"),
    ("Denmark", "+45"),
    ("Djibouti", "+253"),
    ("Dominica", "+1-767"),
    ("Dominican Republic", "+1-809"),
    ("Ecuador", "+593"),
    ("Egypt", "+20"),
    ("El Salvador", "+503"),
    ("Equatorial Guinea", "+240"),
    ("Eritrea", "+291"),
    ("Estonia", "+372"),
    ("Eswatini", "+268"),
    ("Ethiopia", "+251"),
    ("Fiji", "+679"),
    ("Finland", "+358"),
    ("France", "+33"),
    ("Gabon", "+241"),
    ("Gambia", "+220"),
    ("Georgia", "+995"),
    ("Germany", "+49"),
    ("Ghana", "+233"),
    ("Greece", "+30"),
    ("Grenada", "+1-473"),
    ("Guatemala", "+502"),
    ("Guinea", "+224"),
    ("Guinea-Bissau", "+245"),
    ("Guyana", "+592"),
    ("Haiti", "+509"),
    ("Honduras", "+504"),
    ("Hungary", "+36"),
    ("Iceland", "+354"),
    ("India", "+91"),
    ("Indonesia", "+62"),
    ("Iran", "+98"),
    ("Iraq", "+964"),
    ("Ireland", "+353"),
    ("Israel", "+972"),
    ("Italy", "+39"),
    ("Jamaica", "+1-876"),
    ("Japan", "+81"),
    ("Jordan", "+962"),
    ("Kazakhstan", "+7"),
    ("Kenya", "+254"),
    ("Kiribati", "+686"),
    ("Kuwait", "+965"),
    ("Kyrgyzstan", "+996"),
    ("Laos", "+856"),
    ("Latvia", "+371"),
    ("Lebanon", "+961"),
    ("Lesotho", "+266"),
    ("Liberia", "+231"),
    ("Libya", "+218"),
    ("Liechtenstein", "+423"),
    ("Lithuania", "+370"),
    ("Luxembourg", "+352"),
    ("Madagascar", "+261"),
    ("Malawi", "+265"),
    ("Malaysia", "+60"),
    ("Maldives", "+960"),
    ("Mali", "+223"),
    ("Malta", "+356"),
    ("Marshall Islands", "+692"),
    ("Mauritania", "+222"),
    ("Mauritius", "+230"),
    ("Mexico", "+52"),
    ("Micronesia", "+691"),
    ("Moldova", "+373"),
    ("Monaco", "+377"),
    ("Mongolia", "+976"),
    ("Montenegro", "+382"),
    ("Morocco", "+212"),
    ("Mozambique", "+258"),
    ("Myanmar", "+95"),
    ("Namibia", "+264"),
    ("Nauru", "+674"),
    ("Nepal", "+977"),
    ("Netherlands", "+31"),
    ("New Zealand", "+64"),
    ("Nicaragua", "+505"),
    ("Niger", "+227"),
    ("Nigeria", "+234"),
    ("North Korea", "+850"),
    ("North Macedonia", "+389"),
    ("Norway", "+47"),
    ("Oman", "+968"),
    ("Pakistan", "+92"),
    ("Palau", "+680"),
    ("Palestine", "+970"),
    ("Panama", "+507"),
    ("Papua New Guinea", "+675"),
    ("Paraguay", "+595"),
    ("Peru", "+51"),
    ("Philippines", "+63"),
    ("Poland", "+48"),
    ("Portugal", "+351"),
    ("Qatar", "+974"),
    ("Romania", "+40"),
    ("Russia", "+7"),
    ("Rwanda", "+250"),
    ("Saint Kitts and Nevis", "+1-869"),
    ("Saint Lucia", "+1-758"),
    ("Saint Vincent and the Grenadines", "+1-784"),
    ("Samoa", "+685"),
    ("San Marino", "+378"),
    ("Sao Tome and Principe", "+239"),
    ("Saudi Arabia", "+966"),
    ("Senegal", "+221"),
    ("Serbia", "+381"),
    ("Seychelles", "+248"),
    ("Sierra Leone", "+232"),
    ("Singapore", "+65"),
    ("Slovakia", "+421"),
    ("Slovenia", "+386"),
    ("Solomon Islands", "+677"),
    ("Somalia", "+252"),
    ("South Africa", "+27"),
    ("South Korea", "+82"),
    ("South Sudan", "+211"),
    ("Spain", "+34"),
    ("Sri Lanka", "+94"),
    ("Sudan", "+249"),
    ("Suriname", "+597"),
    ("Sweden", "+46"),
    ("Switzerland", "+41"),
    ("Syria", "+963"),
    ("Taiwan", "+886"),
    ("Tajikistan", "+992"),
    ("Tanzania", "+255"),
    ("Thailand", "+66"),
    ("Timor-Leste", "+670"),
    ("Togo", "+228"),
    ("Tonga", "+676"),
    ("Trinidad and Tobago", "+1-868"),
    ("Tunisia", "+216"),
    ("Turkey", "+90"),
    ("Turkmenistan", "+993"),
    ("Tuvalu", "+688"),
    ("Uganda", "+256"),
    ("Ukraine", "+380"),
    ("United Arab Emirates", "+971"),
    ("United Kingdom", "+44"),
    ("United States", "+1"),
    ("Uruguay", "+598"),
    ("Uzbekistan", "+998"),
    ("Vanuatu", "+678"),
    ("Vatican City", "+39"),
    ("Venezuela", "+58"),
    ("Vietnam", "+84"),
    ("Yemen", "+967"),
    ("Zambia", "+260"),
    ("Zimbabwe", "+263")
)

def phoneNumberToCountry(number):
	for i in countries_with_codes:
		if [i][1] == number
		document.add([now(),"phoneNumberToCountry",number,i[0]])
		return i[0]
	document.add([now(),"phoneNumberToCountry",number,"invalid number"])
	return "invalid number"

def countryToPhoneNumber(country):
	for i in countries_with_codes:
		if [i][0] == country
		document.add([now(),"countryNumberToPhoneNumber",country,i[1]])
		return i[1]
	document.add([now(),"countryNumberToPhoneNumber",country,"invalid country"])
	return "invalid country"


