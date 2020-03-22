from random import randint
from time import sleep, localtime, strftime


class ListaParaSeleccion():

    def __init__(self):

        self.personas = []


    def carga(self):

        print('\nIngrese un campo vacio para finalizar la carga de participantes\n')
        x = input('Ingrese un nombre: ')
        while x != '':
            self.personas.append(x.title())
            x = input('Ingrese un nombre: ')
        self.personas.sort()


    def seleccion(self):

        return self.personas[randint(0,len(self.personas)-1)]


    def __str__(self):

        text = '\nParticipantes:\n'
        for integrante in self.personas:
            text += f'\t\t-{integrante}\n'
        text += '\n'

        return text


    def __len__(self):

        return len(self.personas)
    

def get_time(time_format = "%A %d/%m/%y  %H:%M:%S"):
    '''
    Get current time using time.localtime method, default time format = 
    "day_of_week day/month/year hour:minute:second" accepts other format 
    as a str
    '''
    t = localtime()
    return strftime(time_format, t)


def new_screen():
    print('\n' * 50)


def reintentar():
    
    def invalid():
        new_screen()
        print('\tOpcion invalida!!\n\n')
        return reintentar()
        
    try:
        x = int(input('Ingrese 1 para reintentar o 0 para salir: '))
    except:
        x = invalid()
    finally:
        if x != 1 and x != 0:
            x = invalid()
        return x


def shift_finder():

    time = int(get_time('%H'))
    day = get_time('%A').lower()

    if time in range(9,17) and day != 'monday':
        return 'Turno Mañana'
    elif ((time in range(17,24) or time == 0) and day != 'monday') or (time == 1 and day == 'monday'):
        return 'Turno Tarde'
    return 'Fuera de turno'


def valid_entry(personas, elegido, log):

    log.write(f"\n\n\n{('-' * 10)}  entry time:   {get_time()}   |   {shift_finder()}  {('-' * 15)}\n\nSelection list:\n")
    for persona in personas:
        if persona != elegido:          
            log.write(f'\t\t-{persona}\n')
        else:
            log.write(f'\t\t-{persona}*\n')
    log.write('\n' + ('-' * (81 + len(get_time('%A')))))


def invalid_entry(log):

    log.write(f'''\n\n\n{('-' * 10)}  entry time:   {get_time()}   |   {shift_finder()}  {('-' * 15)}\n\n   > "less than 2 options" error :/\n\n{('-' * (83 + len(get_time('%A'))))}''')


def selection_screen(selected):

    print(f'time:    {get_time("%D  %H:%M")}' + ('\n' * 7))
    print(('\t' * 2) + '+' + '-' * (len(selected) + 29) + '+')
    print(('\t' * 2) + f'|     El seleccionado es {selected}     |')
    print(('\t' * 2) + '+' + '-' * (len(selected) + 29) + '+')
    print('\n' * 5)
    
    
def main():

    new_screen()
    print('Marico el que lo lea.' + ('\n' * 10))
    sleep(0.5)
    
    while True:
        new_screen()
        lista = ListaParaSeleccion()
        print('\n\nSeleccion de un participante al azar')
        print('=' * 60 + ('\n' * 9))
        lista.carga()
        new_screen()
        log = open('seleccion2_log.txt', 'a+')

        if len(lista) > 1:
            print(lista)
            input('Presione enter para hacer el sorteo')
            new_screen()
            elegido = lista.seleccion()
            selection_screen(elegido)
            valid_entry(lista.personas, elegido, log)

        else:
            print('\nCantidad de participantes insuficiente :/\n')
            print('\n'*5)
            invalid_entry(log)

        log.close()
        del lista

        if reintentar():
            continue
        else:
            break

    new_screen()
    print('\t\t\tGracias jalabola' + ('\n' * 10) + 'made with love, by Diego.')
    sleep(1)


if __name__ == '__main__':
    main()
