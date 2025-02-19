import psycopg2 as pg
from psycopg2 import sql as sql_pg
from sqlalchemy import create_engine


class Connection(object):
    def __init__(self, my_host="", db_name="", my_user="", my_password="", port="5432"):
        self.db_name = db_name
        self.con = pg.connect(host=my_host, database=db_name, user=my_user, password=my_password)
        self.cur = self.con.cursor()
        self.connection_string = f'postgresql://{my_user}:{my_password}@{my_host}:{port}/{db_name}?client_encoding=utf8'
        self.engine = create_engine(self.connection_string)

    def teste_connect(self):
        try:
            execute = self.cur.execute(f""" SELECT * FROM {self.db_name} """)
            self.con.commit()
            return execute
        except pg.Error as e:
            return e

    def execute_pass_safe(self, sql):
        try:
            self.cur.execute(sql)
            self.con.commit()
            return "Executado com sucesso"
        except pg.Error as e:
            return e

    def read_db(self, schema, table):
        try:
            query = sql_pg.SQL("SELECT * FROM {}.{}").format(
                sql_pg.Identifier(schema),
                sql_pg.Identifier(table)
            )
            self.cur.execute(query)
            resposta = self.cur.fetchall()
            return resposta
        except pg.Error as e:
            return e

    def insert_into_table(self, schema, table, values):
        try:
            # Recuperar nomes das colunas
            self.cur.execute(sql_pg.SQL(
                "SELECT column_name FROM information_schema.columns WHERE table_schema = %s AND table_name = %s"),
                             (schema, table))
            columns = [row[0] for row in self.cur.fetchall()]

            # Construir a query de insert dinamicamente
            insert_query = sql_pg.SQL("INSERT INTO {}.{} ({}) VALUES ({})").format(
                sql_pg.Identifier(schema),
                sql_pg.Identifier(table),
                sql_pg.SQL(', ').join(map(sql_pg.Identifier, columns)),
                sql_pg.SQL(', ').join(sql_pg.Placeholder() * len(columns))
            )

            # Executar a query
            self.cur.execute(insert_query, values)
            self.con.commit()
            return "Inserção realizada com sucesso"
        except pg.Error as e:
            self.con.rollback()  # Em caso de erro, desfazer a transação
            return e

    def engine_to_sql(self, a: bool):
        if a is True:
            engine = self.engine
            return engine
