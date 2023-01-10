import configparser


class Token:
    config = configparser.ConfigParser()

    try:
        config.read('settings.ini')
        VK = config['VKontakte']['vk_token']
        VK_VERSION = '5.131'
        YA = config['Yandex']['ya_token']
    except Exception as err:
        print('Отсутствует токен', err)
        VK = ''
        VK_VERSION = ''
        YA = ''

    # print(VK, VK_VERSION, YA)  # ----------------------------------

    if not (VK and YA):
        config['DEFAULT'] = {'vk_token': '', 'ya_token': ''}

        while not VK:
            VK = input('\nОтсутствует токен api VKontakte! Введите сервис-токен VK: ')
        config['VKontakte'] = {'vk_token': VK}

        while not YA:
            YA = input('\nОтсутствует токен api Yandex! Введите свой токен Yandex: ')
        config['Yandex'] = {'ya_token': YA}

        with open('settings.ini', 'w') as configfile:
            config.write(configfile)

