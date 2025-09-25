def step1():
    print(
        'Утка-маляр 🦆 решила выпить зайти в бар. '
        'Взять ей зонтик? ☂️'
    )
    option = ''
    options = {'да': True, 'нет': False}
    while option not in options:
        print('Выберите: {}/{}'.format(*options))
        option = input()

    if options[option]:
        return step2_umbrella()
    return step2_no_umbrella()


def step2_umbrella():
    print(
        'Уточка решила подстраховаться. '
        'Какого цвета ей взять зонтик? '
        'У нее в коллекции есть красный 🔴, синий 🔵 и зеленый 🟢 зонтики. '
    )
    option = ''
    options = {'красный': 'сапоги', 'синий': 'шарф', 'зеленый': 'плащ'}
    while option not in options:
        print('Выберите: {}/{}/{}'.format(*options))
        option = input()

    accessory = options[option]
    print(
        f'Уточка взяла {option} зонтик и надела под его цвет {accessory}. \n'
        'Уточка не промокла под дождем по дороге в бар. '
        'Там она провела прекрасный вечер, собрав кучу комплиментов. '
    )


def step2_no_umbrella():
    print(
        'Уточка решила не брать зонтик. '
        'Она захотела промокнуть и почувствовать себя героиней фильма 🎥. \n'
        'Уточка провела прекрасный вечер в баре.'
    )


if __name__ == '__main__':
    step1()
