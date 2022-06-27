import vk_api
import requests
import time
from bs4 import BeautifulSoup
from vk_api.longpoll import *
from Citilink_Apple import pars_citilink

token2 = 'cda923ac6d6cdbf05a2ba3b791f97869fc7f237f623c07bf93935e774ae23581fb35e7a8bba37dbf7e145'
vk = vk_api.VkApi(token=token2)
zxc = VkLongPoll(vk)


class VkBot:
    def __init__(self, user_id):

        print("Создан объект бота!")
        self._USER_ID = user_id
        try:
            self._USER_CITY = vk.method('users.get', {'user_ids': user_id, 'fields': 'city'})[0]['city']['title']
        except:
            self._USER_CITY = False

        self._USERNAME = vk.method('users.get', {'user_ids': user_id})[0]['first_name']
        self._COMMANDS = ["ПРИВЕТ", "ПОГОДА", "ПОКА", "СТАРТ"]
        print('Указанный город для id %i: ' % user_id, self._USER_CITY)

    def _clean_all_tag_from_str(self, string_line):  # приходит в формате Tag

        result = ""
        for i in string_line.text:  # now is string
            not_skip = True
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True
        return result

    # firstly we need to know what the command said user
    def new_message(self, message):

        # Привет
        if message.upper() == self._COMMANDS[0]:
            return 'Уи махуэ фlыуэ, %u' % self._USERNAME

        # Погода
        if message.upper().split()[0] == self._COMMANDS[1]:
            if message.upper() == self._COMMANDS[1]:
                if self._USER_CITY:
                    return self._get_weather(self._USER_CITY)
                else:
                    return 'Я не нашел твой город. Потому что ты, не указал его в профиле.. \n Напиши "Погода " и город в котором хочешь узнать погоду'
            else:
                return self._get_weather(message.upper().split()[1])

        # Пока
        elif message.upper() == self._COMMANDS[2]:
            return 'Гъуэгу махуэ, %u' % self._USERNAME

        # Parser
        elif message.upper() == self._COMMANDS[3]:

            return self.pars_mts(False)

        else:
            return "\nЧтобы узнать погоду напиши погода 'свой город'"

    # Weather
    def _get_weather(self, city):
        request = requests.get("https://sinoptik.com.ru/погода-" + city.lower())
        if request.status_code != 200:
            return "Я такого Залупосранска я не нахожу. Попробуй другой город или напиши этот без ошибок."
        b = BeautifulSoup(request.text, "html.parser")

        min_and_maxWeath = self._clean_all_tag_from_str(b.select_one('.weather__content_tab-temperature'))
        min_and_maxWeath = min_and_maxWeath.replace('макс.', 'Максимум днем')
        min_and_maxWeath = min_and_maxWeath.replace('мин.', 'Минимум днем')
        currentWeather = self._clean_all_tag_from_str(b.select('.table__col.current .table__felt')[0])
        return 'Сегодня в %t: %m \nСейчас ощущается как: %c' % (city.title(), min_and_maxWeath, currentWeather)

    # parsing
    def pars_eldorado(self, itsFirstCall):
        # try:
        # f=open('PhonesConstant.txt', 'w+',  encoding='utf-8')
        print("\n--------------------------------------Eldorado-------------------------------------- \n")

        if itsFirstCall == False:
            return 'тут будем сравнивать и обновлять в эльдорадо'

        dictOriginal = {}
        kolvotelephonov = 0
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.135 YaBrowser/21.6.3.757 Yowser/2.5 Safari/537.36'}

        for iter in range(1, 7):
            req = requests.get('https://www.eldorado.ru/c/smartfony/b/APPLE/?page=%i' % iter, headers=headers)

            b = BeautifulSoup(req.text, "html.parser")
            costAndTags = b.find_all(attrs={"data-pc": "offer_price"})
            ItemNameTags = b.find_all(attrs={"data-dy": "title"})
            EstbBonus = b.find_all(attrs={"data-dy": "bonusListBlock"})

            print("page %i--------------------------------------6" % iter)
            for xx in range(len(EstbBonus)):
                if ItemNameTags[xx].text.find('Apple iPhone') != -1 and ('Yellow') not in ItemNameTags[
                    xx].text:  # or ItemNameTags[xx].text.find('Xiaomi')!=-1  or ItemNameTags[xx].text.find('Samsung')!=-1:
                    kolvotelephonov += 1
                    # if itsFirstCall==True:
                    costNoSpaces = ''.join(costAndTags[xx].text.split()[:2])
                    clearName = ItemNameTags[xx].text.replace('Gb', 'GB')
                    clearName = clearName[:clearName.find('B') + 1].replace('Смартфон ', '').replace('\xa0',
                                                                                                     ' ').replace('Xr',
                                                                                                                  'XR').replace(
                        'Xs', 'XS')
                    dictOriginal[clearName] = costNoSpaces
                else:
                    continue

        return dictOriginal

    # self.pars(False)

    # mts
    def pars_mts(self, itsFirstCall):
        print("--------------------------------------MTS--------------------------------------\n")

        if itsFirstCall == False:
            return 'тут будем сравнивать и обновлять в эльдорадо'

        dictOriginalMts = {}
        kolvotelephonov = 0

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.135 YaBrowser/21.6.3.757 Yowser/2.5 Safari/537.36'}
        for iter in range(1, 5):
            print("page " + str(iter) + "-----------------------------4")

            req = requests.get('https://shop.mts.ru/catalog/smartfony/apple/%i/' % iter, headers=headers)
            b = BeautifulSoup(req.text, "html.parser")

            costAndTags = b.find_all(attrs={'class': 'hidden-price'})
            ItemNameTags = b.find_all(attrs={"class": "shaved-text__original-text"})

            for xx in range(len(costAndTags)):
                kolvotelephonov += 1
                realCost = costAndTags[xx].text.replace('Â â½', '').replace(' ₽', '')

                realName = ItemNameTags[xx].text.replace(' (Ð½Ð¾Ð²Ð°Ñ ÐºÐ¾Ð¼Ð¿Ð»ÐµÐºÑÐ°ÑÐ¸Ñ)',
                                                         ' (новая комплектация)')
                realName = realName.replace(' (новая комплектация)', '')
                realName = realName.replace('b', 'B')
                realName = realName.replace('Mini', 'mini')
                realName = realName.replace('Xr', 'XR')
                realName = realName.replace(' Apple', 'Apple')
                realName = realName[:realName.find('B') + 1]
                dictOriginalMts[realName] = realCost

        return dictOriginalMts


def differ(x, y):  # два словаря на входе
    global diff
    longest = x if len(x[0]) > len(y[0]) else y
    short = x if longest == y else y

    for k in longest[0]:
        if k in short[0]:
            if int(longest[0][k].split()[0]) >= int(short[0][k].split()[0]):
                tempX = int(longest[0][k].split()[0]) - int(short[0][k].split()[0])

                diff[k] = short[0][k].split()[0] + " {} {}".format(short[1], tempX)
            else:
                tempX = int(short[0][k].split()[0]) - int(longest[0][k].split()[0])
                diff[k] = longest[0][k].split()[0] + " {} {}".format(longest[1], tempX)
        else:
            diff[k] = longest[0][k].split()[0] + " {} 0".format(longest[1])


start_time = time.time()

print("Server started")

bot = VkBot(393369556)

eldorado_iphones = bot.pars_eldorado(True)
print('eldorado________________________________', eldorado_iphones, len(eldorado_iphones))

mts_iphones = bot.pars_mts(True)
print('mts________________________', mts_iphones, len(mts_iphones))

# --------------------------#1
diff = {}
differ([eldorado_iphones, 'eldorado'], [mts_iphones, 'mts'])

print('\n\n\neldor vs mts __________________________разница________________________________', diff, len(diff))

citilink_iphones = pars_citilink()
print('\nCitiLink________________________________', citilink_iphones, len(citilink_iphones))
differ([diff, 'oldd'], [citilink_iphones, 'citilink'])

##_____________#2
# for k in citilink_iphones:
#    if k in diff:
#        if int(diff[k].split()[0]) >= int(citilink_iphones[k]):  
#            tempX=int(diff[k].split()[0])-int(citilink_iphones[k])
#            diff[k]=citilink_iphones[k] + " citilink {}".format(tempX)
#    else:
#        diff[k]=citilink_iphones[k] + " citilink 0"

print('\n\n(eldor vs mts) vs citilink __________________________разница________________________________', diff,
      len(diff))

work_time = str(round(time.time() - start_time, 3))
vk.method('messages.send', {'user_id': 393369556, 'message': work_time, 'random_id': 0})
vk.method('messages.send', {'user_id': 393369556, 'message': diff.keys(), 'random_id': 0})
vk.method('messages.send', {'user_id': 393369556, 'message': len(diff), 'random_id': 0})

ids = []
myUsers = []
for event in zxc.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            UserName = vk.method('users.get', {'user_ids': event.user_id})[0]['first_name'] + ' ' + \
                       vk.method('users.get', {'user_ids': event.user_id})[0]['last_name']
            if ids.count(event.user_id) == 1:
                print(' old user. For me by:%u id:%i' % (UserName, event.user_id))
                print('| New message:', event.text)
                vk.method('messages.send',
                          {'user_id': bot._USER_ID, 'message': bot.new_message(event.text), 'random_id': 0})
            else:
                ids.append(event.user_id)
                bot = VkBot(event.user_id)
                myUsers.append(bot)  # решил по приколу сохранять юзеров
                print('new user. For me by:%u id:%i' % (UserName, event.user_id))
                print('| New message:', event.text)
                vk.method('messages.send',
                          {'user_id': event.user_id, 'message': bot.new_message(event.text), 'random_id': 0})
