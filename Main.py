import PySimpleGUI as sg
import sys
from View import View

# Liskov
# Abstração como controller como pai, pra facilitar comunicação
# Coloquei funções de print dentro de cada classe
# Talvez adicionar funções mais extensivas pra print de debug


sg.theme('DarkBlue2')

main_view = ""

def main(args):

    # Inicializando controller
    global main_view
    main_view = View()
    main_view.view_main()

main(sys.argv)