import requests
from bs4 import BeautifulSoup
url = "https://tcyangmis.herokuapp.com/about"
Data = requests.get(url)
#print(Data.text)
sp = BeautifulSoup(Data.text, "html.parser")
result=sp.select("td")
#print(result)
info = ""
for item in result:
	info += item.text + "\n\n"
print(info)