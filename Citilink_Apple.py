import requests
from bs4 import BeautifulSoup

def pars_citilink():
    dictOriginalMvideo={}
    kolvotelephonov=0
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
    print("\n______________________CitiLink____________________")
    for iter in range(1, 3):   
        print("page "+str(iter)+"-----------------------------2")

        req=requests.get('https://www.citilink.ru/catalog/smartfony/APPLE/?p=%i'%iter,headers=headers)
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