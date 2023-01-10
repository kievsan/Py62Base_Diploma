#

import configparser


class Token:
    configurator = configparser.ConfigParser()

    try:
        configurator.read('settings.ini')
        VK = configurator['VKontakte']['token']
        VK_VERSION = '5.131'
        YA = configurator['Yandex']['token']
    except Exception as err:
        print(err)
        VK = ''
        VK_VERSION = ''
        YA = ''

    if not (VK and YA):
        while not VK:
            VK = input('\nОтсутствует токен api VKontakte! Введите сервис-токен VK: ')
        configurator['VK'] = {'token': VK}

        while not YA:
            YA = input('\nОтсутствует токен api Yandex! Введите свой токен Yandex: ')
        configurator['YA'] = {'token': YA}

        with open('settings.ini', 'w') as config:
            configurator.write(config)

