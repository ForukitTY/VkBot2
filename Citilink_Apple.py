import requests
import time,random
from bs4 import BeautifulSoup

def pars_citilink():
	dictOriginalMvideo={}
	kolvotelephonov=0
	head=[{'User-Agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 YaBrowser/21.8.1.476 Yowser/2.5 Safari/537.36'},
		  {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94'},
		  {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94'},
		  {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.243'},
		  {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.243'},
		  {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123'}]
	prox=[{'http':'http://93.94.182.225:8080'},
	   {'http':'http://46.237.255.14:8080'},
	   {'http':'http://157.155.103.139:8080'},
	   {'http':'http://253.6.201.182:53281'},
	   {'http':'http://250.38.65.0:999'},
	   {'http':'http://105.123.68.183:8080'}]
	print("\n______________________CitiLink____________________")
	for zalupe in range(0,6):
		for iter in range(1, 3):   
			print("page "+str(iter)+"-----------------------------2")
			xax=random.uniform(2,5)
			print(xax)
			time.sleep(xax)

			req=requests.get('https://www.citilink.ru/catalog/smartfony/APPLE/?p=%i'%iter,headers=head[zalupe],proxies=prox[zalupe])
		
			print(req.status_code,'\n',req.headers, '\n') #req.cookies.get_dict() )
		
			b = BeautifulSoup(req.text, "html.parser")
			costAndTags = b.find_all(attrs={'class': 'ProductCardHorizontal__price_current-price'})
			ItemNameTags = b.find_all(attrs={"class": "ProductCardHorizontal__title Link js--Link Link_type_default"})

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