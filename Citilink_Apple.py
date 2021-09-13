import requests
import time,random
from bs4 import BeautifulSoup

def pars_citilink():
	dictOriginalMvideo={}
	kolvotelephonov=0
	agents=[{'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 RuxitSynthetic/1.0 v7139868079105931835 t8052286838287810618'},
		  {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94'},
		  {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94'},
		  {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.243'},
		  {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.243'},
		  {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123'}]
	head={
        'Connection':'keep-alive',


        'Upgrade-Insecure-Requests':'1',

        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.43 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94'
		}

	prox=[{'http':'http://217.29.53.64:33165', 'https':'https://217.29.53.64:33165'}, {'http':'socks5://20.182.253.244:11857','https': 'socks5://20.182.253.244:11857'}, {'http':'http://45.90.216.166:10001','https': 'https://45.90.216.166:10001'}]
	print("\n______________________CitiLink____________________")
	#for zalupe in range(0,6):
	for iter in range(1, 3):   
		print("page "+str(iter)+"-----------------------------2")
		xax=random.uniform(1,3)
		print(xax)
		time.sleep(xax)

		req=requests.get(f'https://www.citilink.ru/catalog/smartfony/?f=discount.any%2Crating.any%2Capple%2Chonor%2Csamsung%2Crating.any%2Capple%2Csamsung&p={iter}',headers=agents[2], timeout=35)
		#req=requests.get(f'https://2ip.ua/ru/',headers=agents[2], timeout=37)
		costAndTags = BeautifulSoup(req.text, "html.parser").find_all(attrs={'class': 'ipblockgradient'})

		print(req.status_code,'\n-----------', req.request.headers, req.headers )
		#print(costAndTags,'\n', '\n') 
		 

		b = BeautifulSoup(req.text, "html.parser")
		costAndTags = b.find_all(attrs={'class': 'ProductCardHorizontal__price_current-price js--ProductCardHorizontal__price_current-price'})
		print(costAndTags[0].text)
		ItemNameTags = b.find_all(attrs={"class": "ProductCardHorizontal__header-block"})
		print(len(ItemNameTags))

		for xx in range(len(costAndTags)):
			if ItemNameTags[xx].text.find('желтый')!=-1:
				continue
			realCost=''
			kolvotelephonov+=1

			realCost=''.join(costAndTags[xx].text.split())
			if int(realCost)<30000:
				continue

			realName=ItemNameTags[xx].text[0:ItemNameTags[xx].text.find('Gb')+2]
			realName=realName.replace('Gb','GB').replace('APPLE','Apple').replace('SAMSUNG','Samsung').replace('HONOR','Honor')
			
			print(f'{kolvotelephonov} {realName} {realCost}')
			dictOriginalMvideo[realName]=[realCost,'citilink']


	return dictOriginalMvideo