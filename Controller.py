from View import *
from Model import Model as Parent
from datetime import date

class Controller(Parent):
    def __init__(self, senha):
        super().__init__(senha)

    def controller_consultar_todos(self):
        return super().model_consult("SELECT * FROM Funcionario;", "")

    @staticmethod
    def controller_editar(self, modo, dado):
        if modo == 'A': # Add
            self.model_create_update("""INSERT INTO Funcionario VALUES (""" + dado[0] + """,
                 \'""" + dado[1] + """\',
                 \'""" + dado[2] + """\',
                 \'""" + dado[3] + """\',
                 """ + dado[4] + """);""", dado)
        elif modo == 'E': # Edit
            self.model_create_update("""UPDATE Funcionario SET id=""" + dado[0] + """,
                             nome=\'""" + dado[1] + """\',
                             departamento=\'""" + dado[2] + """\',
                             data_contratacao=\'""" + dado[3] + """\',
                             treinamento=""" + dado[4] + """ WHERE id=""" + dado[0], dado)
        elif modo == 'R': # Remove
            self.model_create_update("""DELETE FROM Funcionario WHERE id=""" + str(dado[0]), dado)
        else:
            return 0
        return 1

    # noinspection PyUnreachableCode
    def controller_mais5(self): # Função auxiliar pra formatar ids em strings
        data_hoje = date.today().strftime("%m/%d/%Y")
        query = """SELECT treinamento FROM Funcionario WHERE
                (Date_Part('year', \'""" + data_hoje + """\'::date) - Date_Part('year', data_contratacao::date)) > 5;"""
        dados = super().model_consult(query, "")
        total = 0
        for dado in dados:
            total = total + dado[0]
        return total/len(dados)

    # noinspection PyUnreachableCode
    def controller_menos5(self):
        data_hoje = date.today().strftime("%m/%d/%Y")
        query = """SELECT treinamento FROM Funcionario WHERE
                        (Date_Part('year', \'""" + data_hoje + """\'::date) - Date_Part('year', data_contratacao::date)) < 5;"""
        dados = super().model_consult(query, "")
        total = 0
        for dado in dados:
            total = total + dado[0]
        return total/len(dados)

    # noinspection PyUnreachableCode
    def controller_departamentos(self, departamento):
        query = "SELECT * FROM Funcionario WHERE departamento = \'" + departamento + "\' ORDER BY treinamento DESC;"
        return super().model_consult(query, "")

    def controller_relatorio(self):
        out = "\n"
        departamentos = self.controller_buscar_departamentos()
        total_treinamento_empresa = 0
        total_funcionarios = 0
        for dep in departamentos:
            out = out + "DEPARTAMENTO DE " + dep + "\n"
            out = out + "...ID || NOME || DEPARTAMENTO || DATA CONTR. || HRS. TREINAMENTO\n"
            query = "SELECT * FROM Funcionario WHERE departamento = \'" + dep + "\';"
            dado = super().model_consult(query, "") # Retorna todos os funcionários do departamento
            total_funcionarios = total_funcionarios + len(dado)
            media_dep = 0
            for func in dado:
                total_treinamento_empresa = total_treinamento_empresa + func[4] # Func[4] = treinamento
                media_dep = media_dep + func[4]
                out = out + "..." + str(func[0]) + " || " + func[1] + " || " + func[2] + " || " + str(func[3]) + " || " + str(func[4]) + "\n"
            out = out + "...MEDIA DE HORAS DE TREINO P/ O DEPARTAMENTO: " + str(media_dep/len(dado)) + "\n\n"
        out = out + "MEDIA DE HORAS DE TREINAMENTO DA EMPRESA: " + str(total_treinamento_empresa/total_funcionarios)
        print(out)
        try:
            f = open("relatorio.txt", 'w')
            f.write(out)
            f.close()
        except OSError as e:
            print(e)

    def controller_buscar_departamentos(self): # Auxiliar para retornar todos os departamentos do banco
        query = """select distinct departamento from Funcionario;"""
        dados = super().model_consult(query, "")
        out = []
        for dado in dados:
            out.append(dado[0])
        return out

    

