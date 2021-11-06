import PySimpleGUI as sg
import os
from Controller import Controller as Parent
import copy

# Alterações desejáveis:
# - Achar maneira melhor de colocar os headers dinamicamente usando o model
# - Achar outro jeito de reutilizar os layouts

## HEADERS (PARA TABLES) ##

class View(Parent):
    def __init__(self):
        senha = ''
        layout_temp = [[sg.Text("Favor inserir a senha do banco")],
                        [sg.Input("", key='senha')],
                       [sg.Button("Confirmar", key='confirmar')]]
        input_window = sg.Window('Inserir senha', layout_temp,
                               font='Arial 18',
                               element_justification='center',
                               auto_size_buttons=True,
                               auto_size_text=True)
        event, values = input_window.read()
        if event:
            senha = values['senha']
            input_window.close()
        else:
            input_window.close()
        super(View, self).__init__(senha)
        self.headers = ["ID", "Nome", "Departamento", "Data Contr.", "Treinamento"]

        ## LAYOUTS ##

        self.layout_main = [[sg.Text("Selecione a opção desejada")],
                       [sg.Button("i - Editar informações", key='edit')],
                       [sg.Button("ii - Treinamento médio - +5 Anos", key='mais5')],
                       [sg.Button("iii - Treinamento médio - -5 Anos", key='menos5')],
                       [sg.Button("iv - Consultar departamento", key='departamento')],
                       [sg.Button("v - Emitir Relatório", key='relatorio')]]

    def view_main(self):
        main_window = sg.Window('Exercicio 1 - OTES12', self.layout_main,
                                font='Arial 18',
                                element_justification='center',
                                auto_size_buttons=True,
                                auto_size_text=True)

        while True:
            event, values = main_window.read()
            main_window.disable()
            if event == 'edit':
                self.view_editar()
            elif event == 'mais5':
                self.view_mais5()
            elif event == 'menos5':
                self.view_menos5()
            elif event == 'departamento':
                self.view_departamento()
            elif event == 'relatorio':
                self.view_relatorio()
            else:
                main_window.close()
                break
            main_window.enable()
            main_window.force_focus()

    def view_editar(self):
        valores = super().controller_consultar_todos()
        layout_edit_main = [[sg.Table(valores, self.headers, key='table', enable_events=True, auto_size_columns=False, col_widths=[20], justification="left")],
                         [sg.Button("Adicionar", key='add'),
                          sg.Button("Editar", key='edit'),
                          sg.Button("Remover", key='remove'),
                          sg.Button("Fechar", key='fechar')]] # Update() pra atualizar valores
        edit_window_main = sg.Window('Editar entradas', layout_edit_main,
                               font='Arial 18',
                               element_justification='center',
                               auto_size_buttons=True,
                               auto_size_text=True)
        selected_row = None
        while True:
            event, values = edit_window_main.read()
            if event == 'add':
                edit_window_main.disable()
                layout_edit_specific = [[sg.Text("ID"), sg.Input("", key='id')],
                                        [sg.Text("Nome"), sg.Input("", key='nome')],
                                        [sg.Text("Departamento"), sg.Input("", key='departamento')],
                                        [sg.Text("Data de Contr."), sg.Input("", key='data_contratacao')],
                                        [sg.Text("Tempo de Treinamento"), sg.Input("", key='treinamento')],
                                        [sg.Button("Confirmar", key='ok'), sg.Button("Cancelar", key='cancel')]]
                edit_window_specific = sg.Window('Adicionar entradas', layout_edit_specific,
                               font='Arial 18',
                               element_justification='center',
                               auto_size_buttons=True,
                               auto_size_text=True)
                while True:
                    event_specific, values_specific = edit_window_specific.read()
                    if event_specific == 'ok':
                        valores_send = [values_specific['id'],
                                        values_specific['nome'],
                                        values_specific['departamento'],
                                        values_specific['data_contratacao'],
                                        values_specific['treinamento']]
                        if super().controller_editar('A', valores_send) == 1:
                            selected_row = None
                            edit_window_main.find_element('table').update(values=super().controller_consultar_todos())
                            sg.Popup("Adicionado com sucesso!")
                        else:
                            sg.Popup("Erro! Dado não adicionado...")
                        edit_window_main.enable()
                        edit_window_specific.close()
                        break
                    else:
                        edit_window_main.enable()
                        edit_window_specific.close()
                        break
            elif event == 'edit':
                valores = edit_window_main.find_element('table').get()[selected_row]
                edit_window_main.disable()
                layout_edit_specific = [[sg.Text("ID"), sg.Input(valores[0], key='id', disabled=True)],
                                        [sg.Text("Nome"), sg.Input(valores[1], key='nome')],
                                        [sg.Text("Departamento"), sg.Input(valores[2], key='departamento')],
                                        [sg.Text("Data de Contr."), sg.Input(valores[3], key='data_contratacao')],
                                        [sg.Text("Tempo de Treinamento"), sg.Input(valores[4], key='treinamento')],
                                        [sg.Button("Confirmar", key='ok'), sg.Button("Cancelar", key='cancel')]]
                edit_window_specific = sg.Window('Adicionar entradas', layout_edit_specific,
                                                 font='Arial 18',
                                                 element_justification='center',
                                                 auto_size_buttons=True,
                                                 auto_size_text=True)
                while True:
                    event_specific, values_specific = edit_window_specific.read()
                    if event_specific == 'ok':
                        valores_send = [values_specific['id'],
                                        values_specific['nome'],
                                        values_specific['departamento'],
                                        values_specific['data_contratacao'],
                                        values_specific['treinamento']]
                        if super().controller_editar('E', valores_send) == 1:
                            selected_row = 0
                            edit_window_main.find_element('table').update(values=super().controller_consultar_todos())
                            sg.Popup("Editado com sucesso!")
                        else:
                            sg.Popup("Erro! Dado não editado...")
                        edit_window_main.enable()
                        edit_window_specific.close()
                        break
                    else:
                        edit_window_main.enable()
                        edit_window_specific.close()
                        break
            elif event == 'remove':
                if super().controller_editar('R', edit_window_main.find_element('table').get()[selected_row]) == 1:
                    selected_row = 0
                    edit_window_main.find_element('table').update(values=super().controller_consultar_todos())
                    sg.Popup("Removido com sucesso!")
                else:
                    sg.Popup("Erro! Dado não removido...")
            elif event == 'fechar':
                edit_window_main.close()
            elif event == 'table':
                if len(values['table']) > 0:
                    selected_row = values['table'][0]
            else:
                edit_window_main.close()
                break

    def view_mais5(self):
        valores = super().controller_mais5()
        layout_temp = [[sg.Text("Resultado:")],
                       [sg.Text(str(valores))]]
        sg.Window('Adicionar entradas', layout_temp,
                  font='Arial 18',
                  element_justification='center',
                  auto_size_buttons=True,
                  auto_size_text=True).read()

    def view_menos5(self):
        valores = super().controller_menos5()
        layout_temp = [[sg.Text("Resultado:")],
                       [sg.Text(str(valores))]]
        sg.Window('Adicionar entradas', layout_temp,
                  font='Arial 18',
                  element_justification='center',
                  auto_size_buttons=True,
                  auto_size_text=True).read()

    def view_departamento(self):
        departamentos = super().controller_buscar_departamentos()
        layout_escolher = [[sg.Text("Favor escolher o departamento:")],
                           [sg.Combo(departamentos, key='combo', default_value=departamentos[0])],
                           [sg.Button("Confirmar", key='confirmar')]]
        window_escolher = sg.Window('Escolher departamento', layout_escolher,
                               font='Arial 18',
                               element_justification='center',
                               auto_size_buttons=True,
                               auto_size_text=True)
        event, values = window_escolher.read()
        if event == 'confirmar':
            valores = super().controller_departamentos(values['combo'])
            layout_departamento = [[sg.Table(valores, self.headers, auto_size_columns=False, col_widths=[20],
                       justification="left")],
             [sg.Button("Fechar", key='fechar')]]
            window_departamento = sg.Window('Inserir senha', layout_departamento,
                                   font='Arial 18',
                                   element_justification='center',
                                   auto_size_buttons=True,
                                   auto_size_text=True)
            window_departamento.read()
            window_departamento.close()
        else:
            window_escolher.close()
            return


    def view_relatorio(self):
        super().controller_relatorio()
        os.startfile('relatorio.txt')
