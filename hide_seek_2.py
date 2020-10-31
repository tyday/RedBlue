# this method isn't going to work at all... duh. 
# The cell ownership is never shared via html only sockets
import requests, socketio
from bs4 import BeautifulSoup

page = requests.get('http://192.168.1.5:5001/seek/copper-dogfish')
soup = BeautifulSoup(page.text, 'html.parser')

print(soup)