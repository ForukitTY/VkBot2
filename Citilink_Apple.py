import requests
import time,random
from bs4 import BeautifulSoup

def pars_citilink():
	dictOriginalMvideo={}
	kolvotelephonov=0
	headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.203'}
	prox=[{'http':'http://162.144.57.157:80'}, {'http':'http://94.230.35.108:80'}]
	print("\n______________________CitiLink____________________")
	for iter in range(1, 3):   
		print("page "+str(iter)+"-----------------------------2")
		xax=random.uniform(3,7)
		time.sleep(xax)
		print(xax)

		req=requests.get('https://www.citilink.ru/catalog/smartfony/APPLE/?p=%i'%iter,headers=headers,proxies=prox[iter-1])
		
		sad=requests.get('https://2ip.ru/', proxies=prox[iter-1])
		print(req.status_code,'\n',req.headers, '\n', req.cookies.get_dict() )
		
		b = BeautifulSoup(req.text, "html.parser")
		costAndTags = b.find_all(attrs={'class': 'ProductCardHorizontal__price_current-price'})
		ItemNameTags = b.find_all(attrs={"class": "ProductCardHorizontal__title Link js--Link Link_type_default"})
        
		#print(b.prettify())
		#print(ItemNameTags,end='\n')

		for xx in range(len(costAndTags)):
			if ItemNameTags[xx].text.find('желтый')!=-1:
				continue
			realCost=''
			kolvotelephonov+=1
			for index in costAndTags[xx].text:
				if index.isdigit():
					realCost+=index

			realName=ItemNameTags[xx].text.replace('Gb','GB').replace('APPLE',' Apple')
			realName=realName[realName.find('Apple'):realName.find('GB')+2]

			dictOriginalMvideo[realName]=[realCost,'citilink']

	return dictOriginalMvideo