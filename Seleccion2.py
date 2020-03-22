'''
Script fot the Seleccion2 program with a tkinter GUI
'''

from tkinter import Tk, Label, Button, Frame, IntVar, Radiobutton, ttk
from tkinter import Entry, messagebox, END, PhotoImage, LEFT
from random import randint
from time import localtime, strftime, sleep


class ListaParaSeleccion:
    '''
    Creates a list that can be charged, and can
    select a random participant from it
    '''

    def __init__(self):
        '''
        self.personas is the list in which everything will operate on
        '''

        self.personas = []

    def seleccion(self):
        '''
        Picks a random item from self.personas
        '''

        return self.personas[randint(0, len(self.personas) - 1)]

    def delete_last(self, event=None):
        '''
        Delete last item from the list using list.pop()
        '''
        if self.personas != []:
            self.personas.pop()
            list_update()
        else:
            start_screen()

    def __str__(self):
        '''
        returns all of the self.personas items listed
        '''

        text = '\nParticipantes:\n\n\n'
        for integrante in self.personas:
            text += f'\t- {integrante}\n'
        text += '\n'

        return text

    def __len__(self):
        '''
        returns len(self.personas)
        '''

        return len(self.personas)


class SetMode:
    '''
    Set the current color theme for the whole window
    available modes: Light (tkinter default), Dark blue
    '''

    def tab_set(self):
        '''
        Sets all tabs
        '''
        for tab in TABS:
            tab.configure(background=self.bg_style)

    def label_set(self):
        '''
        Sets all labels
        '''
        for label in LABELS:
            label.configure(bg=self.bg_style, fg=self.fg_style, activebackground=self.btn_style)

    def button_set(self):
        '''
        Sets all buttons
        '''
        for button in BUTTONS:
            button.configure(bg=self.btn_style, fg=self.btn_text, activebackground=self.btn_style)

    def output_set(self):
        '''
        Sets all output boxes
        '''

        for box in OUTPUT_BOXES:
            box.configure(bg=self.out_bg, fg=self.out_fg)

    def dark(self, event=None):
        '''
        Updates the init values and changes the
        window color mode to a dark color scheme
        '''

        # Palette from https://colorhunt.co/palette/25729

        dark_bg = '#222831'
        dark_fg = '#00fff5'
        dark_btn = '#00adb5'
        dark_btn_txt = '#222831'
        dark_out = '#393e46'
        dark_out_txt = 'white'

        # Palette from https://www.color-hex.com/color-palette/36646

        # dark_bg = '#4b5162'
        # dark_fg = '#5294e2'
        # dark_btn = '#383c4a'
        # dark_btn_txt = '#5294e2'
        # dark_out = '#7c818c'
        # dark_out_txt = 'white'

        self.bg_style = dark_bg
        self.fg_style = dark_fg
        self.btn_style = dark_btn
        self.btn_text = dark_btn_txt
        self.out_bg = dark_out
        self.out_fg = dark_out_txt

        self.update()

    def light(self, event=None):
        '''
        Updates the init values and changes the
        window color mode to a light color scheme
        '''

        light_bg = 'SystemButtonFace'
        light_fg = 'black'
        light_btn = 'SystemButtonFace'
        light_btn_txt = 'black'
        light_out = 'white'
        light_out_txt = 'black'

        self.bg_style = light_bg
        self.fg_style = light_fg
        self.btn_style = light_btn
        self.btn_text = light_btn_txt
        self.out_bg = light_out
        self.out_fg = light_out_txt

        self.update()

    def update(self):
        '''
        applies the init color values to the tabs,
        labels, buttons and output boxes
        '''
        self.tab_set()
        self.label_set()
        self.button_set()
        self.output_set()


class Registry:
    '''
    Object to manage the registry entries,
    as well as the display values
    '''

    def __init__(self):
        self.txt_file = None
        self.registry = None
        self.update_registry()
        self.counter = 0
        self.current_page = 0

    def update_registry(self):
        '''
        Updates the entries registry that's being used
        '''

        with open(REGISTRY_FILENAME, mode='r') as open_file:

            self.txt_file = open_file.read()
            self.registry = self.txt_file.split('\n\n\n')

    def update_reg_screen(self, direction=0):
        '''
        Updates the output screen of the registry tab
        takes in the direction to move as a param
        '''

        if self.txt_file.strip() == '':
            return self.nothing_to_see()

        self.counter += direction

        self.current_page = len(self.registry) - self.counter + 1

        if self.current_page > len(self.registry):
            self.current_page -= len(self.registry)
            self.counter += len(self.registry)
        elif self.current_page < 1:
            self.current_page += len(self.registry)
            self.counter = 1

        log_entry = self.registry[self.current_page - 1]

        entry_num.configure(text=f'entry {self.current_page} / {len(self.registry)}')

        return log_entry

    def nothing_to_see(self):
        '''
        sets registry screen for when no entries are found
        '''
        entry_num.configure(text='I would display the number of pages here... If there was at least one!')
        return 'Nothing to see here yet!!'

    def show_next(self, event=None):
        '''
        show next registry entry
        '''
        self.update_registry()
        registry_display.configure(text=self.update_reg_screen(1))

    def show_prev(self, event=None):
        '''
        show previous registry entry
        '''
        self.update_registry()
        registry_display.configure(text=self.update_reg_screen(-1))

    def delete_entry(self, event=None):
        '''
        deletes the displayed entry from the registry file
        '''

        try:
            del self.registry[self.current_page-1]
            new_reg = '\n\n\n'.join(self.registry)

            with open(REGISTRY_FILENAME, mode='w') as reg_txt_file:
                reg_txt_file.write(new_reg)

            if len(self.registry) >= 1:
                registry_display.configure(text=self.update_reg_screen())
            else:
                registry_display.configure(text=self.nothing_to_see())

        except IndexError:
            registry_display.configure(text='An error ocurred while deleting the entry!!\n:(')

    def __len__(self):
        return len(self.registry)


def pop_up_warning():
    '''
    Shows a popup info message
    '''
    messagebox.showinfo('Marico el que lo lea', 'Marico el que lo lea\n\nQue esperabas encontrar?')


def show_info():
    '''
    Contact info popup
    '''
    MESSAGE =  f'''
    Release version: {VERSION}\n
    Please report any bugs or make
    suggestions to: {CONTACT}\n
    Maybe even say hi :)
    '''
    messagebox.showinfo('Contact info', MESSAGE)


def near_miss(event=None):
    '''
    Easter egg I guess????
    '''
    MESSAGE = '''
    En este programa no existen los tickets fiscales :B\n
    yea this is an easter egg 420 69 lulz
    '''
    messagebox.showinfo('Presionaste F1', MESSAGE)


def close_program(event=None):
    '''
    Asks the user for confirmation to close the program
    and proceeds acordingly
    '''
    wanna_close = messagebox.askyesnocancel('Close program?', 'Are you sure you want to close Seleccion2?')

    if wanna_close:
        WINDOW.destroy()


def get_time(time_format="%A %d/%m/%y  %H:%M:%S"):
    '''
    Get current time using time.localtime method, default time format =
    "day_of_week day/month/year hour:minute:second" accepts other format
    as a str
    '''
    time_now = localtime()
    return strftime(time_format, time_now)


def shift_finder():
    '''
    Determine the current padre coffee and beer work shift
    '''

    time = int(get_time('%H'))
    day = get_time('%A').lower()

    if time in range(9, 17) and day != 'monday':
        return 'Turno Mañana'
    elif ((time in range(17, 24) or time == 0) and day != 'monday') or (time == 1 and day == 'monday'):
        return 'Turno Tarde'
    return 'Fuera de turno'


def valid_entry(personas, elegido):
    '''
    Writes a registry of the last round of selection to the log
    '''

    with open(REGISTRY_FILENAME, 'a+') as log:
        log.write(f"\n\n{('-' * 10)}  entry time:   {get_time()}   |   {shift_finder()}  {('-' * 15)}\n\nSelection list:\n")
        for persona in personas:
            if persona != elegido:
                log.write(f'\t\t-{persona}\n')
            else:
                log.write(f'\t\t-{persona}*\n')
        log.write('\n' + ('-' * (81 + len(get_time('%A')))) + '\n')


def invalid_entry():
    '''
    Writes a registry of the last failed round of selection to the log
    '''
    with open(REGISTRY_FILENAME, 'a+') as log:
        log.write(f'''\n\n{('-' * 10)}  entry time:   {get_time()}   |   {shift_finder()}  {('-' * 15)}\n\n   > "less than 2 options" error :/\n\n{('-' * (83 + len(get_time('%A'))))}\n''')


def selection_screen(selected):
    '''
    Returns the str of the selected item
    with a header of time, date and shift
    '''

    out_text = f'time:    {get_time("%D  %H:%M")}' + ('\n' * 5)
    out_text += f'     El seleccionado es: {selected}     \n\n\n\n\n\n'

    return out_text


def list_update(envent=None):
    '''
    Updates the selection screen output with the current items
    '''

    participants_output = PARTICIPANTS_LIST.__str__()
    selection_output.configure(text=participants_output)


def submit_entry(event=None):
    '''
    Append entry box text to the items list
    '''

    input_text = input_box.get()
    if input_text == '' and PARTICIPANTS_LIST.personas != []:
        return

    elif input_text == '':
        start_screen()
        return

    input_box.delete(0, END)

    PARTICIPANTS_LIST.personas.append(input_text.title())

    list_update()


def select(event=None):
    '''
    Make a random selection from the items list
    '''

    if len(PARTICIPANTS_LIST) > 1:
        PARTICIPANTS_LIST.personas.sort()
        selected = PARTICIPANTS_LIST.seleccion()
        out_text = selection_screen(selected)
        valid_entry(PARTICIPANTS_LIST.personas, selected)

    else:
        out_text = 'Cantidad de participantes insuficiente :/\n\n\n\nTry again!'
        invalid_entry()

    program_reg.show_next()
    program_reg.show_prev()
    selection_output.configure(text=out_text)
    PARTICIPANTS_LIST.personas = []


def backspace_key(event=None):
    '''
    determines if backspace keypress should delete las char or last item
    '''

    if input_box.get() != '' and PARTICIPANTS_LIST.personas != []:
        return
    PARTICIPANTS_LIST.delete_last()


def start_screen():
    '''
    Start screen for the selection tab
    '''
    selection_output.configure(text='\n\nType in the participants below!\n\n\n\n\n|\nv')


# --- Startup checks

REGISTRY_FILENAME = 'seleccion2_log.txt'

try:
    STARTUP_FILE = open(REGISTRY_FILENAME, mode='r')
except FileNotFoundError:
    STARTUP_FILE = open(REGISTRY_FILENAME, mode='a+')
finally:
    STARTUP_FILE.close()


# ------------- Window ----------------

WINDOW = Tk()
WINDOW.title('Seleccion2')
WINDOW.geometry('600x500')
try:
    WINDOW.iconbitmap('atom_logo.ico')
except:
    pass

mode = SetMode()

TAB_CONTROL = ttk.Notebook(WINDOW)
TAB_SELECTION = Frame(TAB_CONTROL)
TAB_REGISTRY = Frame(TAB_CONTROL)
TAB_COMMANDS = Frame(TAB_CONTROL)
TAB_ABOUT = Frame(TAB_CONTROL)

TAB_CONTROL.add(TAB_SELECTION, text='Selection')
TAB_CONTROL.add(TAB_REGISTRY, text='Registry')
TAB_CONTROL.add(TAB_COMMANDS, text='Commands')
TAB_CONTROL.add(TAB_ABOUT, text='About')

TAB_CONTROL.pack(expand=1, fill='both')


# ------ Tab seleccion

PARTICIPANTS_LIST = ListaParaSeleccion()

header_selec = Label(TAB_SELECTION, text='Seleccion2', font='none 20', height=2, width=37)
header_selec.grid(column=0, row=0)

dark_btn_state = IntVar()
dark_btn_state.set(1)

dark_mode_btn = Radiobutton(TAB_SELECTION, text='Dark Mode', value=1, command=mode.dark, var=dark_btn_state)
dark_mode_btn.grid(column=0, row=0, padx=37, sticky='E')

light_mode_btn = Radiobutton(TAB_SELECTION, text='Light Mode', value=0, command=mode.light, var=dark_btn_state)
light_mode_btn.grid(column=0, row=0, padx=35, sticky='SE')

selection_output = Label(TAB_SELECTION, font='none 15 bold', width=44, height=13, bg='white', relief='groove')
selection_output.grid(column=0, row=2, sticky='N')
start_screen()

input_box = Entry(TAB_SELECTION, width=45, font='none 10 bold')
input_box.grid(column=0, row=3, padx=90, pady=5, sticky='W')
input_box.focus()

submit_entry_button = Button(TAB_SELECTION, text='Submit ^', width=10, command=submit_entry)
submit_entry_button.grid(column=0, row=3, sticky='e', padx=100, pady=5)

select_button = Button(TAB_SELECTION, text='Select', width=10, command=select)
select_button.grid(column=0, row=4, padx=200, pady=5, sticky='W')

try:
    photo = PhotoImage(file='trash_can.png')
    delete_icon = photo.subsample(13)
    delete_button = Button(TAB_SELECTION, text='Delete', width=70, command=PARTICIPANTS_LIST.delete_last, image=delete_icon, compound=LEFT)
except:
    delete_button = Button(TAB_SELECTION, text='Delete', width=10, command=PARTICIPANTS_LIST.delete_last)
finally:
    delete_button.grid(column=0, row=4, padx=200, pady=5, sticky='E')


# ---- Registry tab

header_reg = Label(TAB_REGISTRY, text='Registry', font='none 20', height=2, width=37)
header_reg.grid(column=0, row=0)

entry_num = Label(TAB_REGISTRY, text='')
entry_num.grid(column=0, row=3)

program_reg = Registry()

registry_display = Label(TAB_REGISTRY, text=program_reg.update_reg_screen(1), height=20, width=65, font='none 10 bold', relief='groove')
registry_display.grid(column=0, row=2)

next_entry = Button(TAB_REGISTRY, text='Next >', width=9, command=program_reg.show_next)
next_entry.grid(column=0, row=4, sticky='E', padx=200)

prev_entry = Button(TAB_REGISTRY, text='< Previous', width=9, command=program_reg.show_prev)
prev_entry.grid(column=0, row=4, sticky='W', padx=200, pady=10)

try:
    delete_entry = Button(TAB_REGISTRY, width=30, image=delete_icon, command=program_reg.delete_entry)
except NameError:
    delete_entry = Button(TAB_REGISTRY, text='Delete Entry', command=program_reg.delete_entry)
finally:
    delete_entry.grid(column=0, row=4, padx=50, pady=5, sticky='E')


# ---- Commands tab

commands_list = '''
<Enter> = Submit entry

<Shift-Enter> = Make Selection

<Backspace> = Delete last participant

<Ctrl- , > = Dark mode  |  <Ctrl- . > = Light mode

<Left> = Previous Registry page

<Right> = Next Registry page

<Shift-Backspace> = Delete current registry entry

<Escape> = Close Program
'''

header_commands = Label(TAB_COMMANDS, text='Commands', font='none 20', height=2, width=37)
header_commands.grid(column=0, row=0)

commands_screen = Label(TAB_COMMANDS, text=commands_list, font='none 14', width=47, height=16, bg='white', relief='groove')
commands_screen.grid(column=0, row=1)


# ---- About tab

INFO = '''
Seleccion al azar

Este programa fue originalmente creado para el
sorteo de tareas no deseadas en Padre Coffee 
Roasters and Beer
:)
'''
VERSION = '2020.3.14'
CONTACT = 'diegoasanch@gmail.com'


header_about = Label(TAB_ABOUT, text='About', font='none 20', height=2, width=37)
header_about.grid(column=0, row=0)

about_info = Label(TAB_ABOUT, text=INFO, height=10, width=50, font='none 13', relief='groove')
about_info.grid(column=0, row=1, pady=5)

about_classic = Button(TAB_ABOUT, text='made with love, by Diego.', height=5, width=25, font='none 7', command=pop_up_warning)
about_classic.grid(column=0, row=2, pady=40)

about_version = Button(TAB_ABOUT, text=f'Latest version: {VERSION}', relief='flat', command=show_info)
about_version.grid(column=0, row=3)


# -------- Dark / Light mode management

TABS = [TAB_SELECTION, TAB_ABOUT, TAB_COMMANDS, TAB_REGISTRY]
LABELS = [dark_mode_btn, light_mode_btn, header_selec, header_reg, header_about, header_commands, entry_num, about_version]
BUTTONS = [submit_entry_button, delete_button, select_button, about_classic, next_entry, prev_entry, delete_entry]
OUTPUT_BOXES = [selection_output, registry_display, about_info, input_box, commands_screen]

mode.dark()

# -------- Binded Commands

input_box.bind('<Return>', submit_entry)
input_box.bind('<Shift-Return>', select)
input_box.bind('<BackSpace>', backspace_key)

WINDOW.bind('<Control-,>', mode.dark)
WINDOW.bind("<Control-.>", mode.light)
WINDOW.bind('<Left>', program_reg.show_prev)
WINDOW.bind('<Right>', program_reg.show_next)
WINDOW.bind('<Escape>', close_program)
WINDOW.bind('<Shift-BackSpace>', program_reg.delete_entry)
WINDOW.bind('<F1>', near_miss)

WINDOW.mainloop()
