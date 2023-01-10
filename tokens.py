import configparser


class Token:
    config = configparser.ConfigParser()

    try:
        config.read('settings.ini')
        VK = config['VKontakte']['token']
        VK_VERSION = '5.131'
        YA = config['Yandex']['token']
    except Exception as err:
        print(err)
        VK = ''
        VK_VERSION = ''
        YA = ''

    # print(VK, VK_VERSION, YA)  # ----------------------------------

    if not (VK and YA):
        while not VK:
            VK = input('\nОтсутствует токен api VKontakte! Введите сервис-токен VK: ')
        config['VKontakte'] = {'token': VK}

        while not YA:
            YA = input('\nОтсутствует токен api Yandex! Введите свой токен Yandex: ')
        config['Yandex'] = {'token': YA}

        with open('settings.ini', 'w') as configfile:
            config.write(configfile)

