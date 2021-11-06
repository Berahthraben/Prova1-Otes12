import psycopg2 as psy

class Model:
    def __init__(self, senha):
        self.cur = []
        self.con = []
        self.host = '127.0.0.1'
        self.dbname = 'Empresa'
        self.user = 'postgres'
        self.port = '5432'
        try:
            self.con = psy.connect(host=self.host, dbname=self.dbname, user=self.user, port=self.port, password=senha)
            self.cur = self.con.cursor()
            print('Conectado na database com sucesso!')
        except psy.Error as e:
            print(e.pgerror)

    def model_destroy(self):
        self.con.commit()
        self.con.close()
        self.cur.close()

    def model_create_update(self, query, data):
        if self.cur.closed != 0 or self.con.closed != 0:
            print("Conecte-se a uma database primeiro!")
            return 0
        try:
            self.cur.execute(query, data)
            self.con.commit()
            return 1
        except (psy.OperationalError, psy.ProgrammingError, psy.DatabaseError) as e:
            print(e.pgerror)
            return 0

    def model_consult(self, query, data):
        if self.cur.closed or self.con.closed:
            print("Conecte-se a uma database primeiro!")
            return 0
        try:
            self.cur.execute(query, '')
            return self.cur.fetchall()
        except psy.Error as e:
            print(e.pgerror)
            return 0
