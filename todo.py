import flet as ft
import sqlite3

class ToDo:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.bgcolor = ft.colors.WHITE
        self.page.window.width = 350
        self.page.window.height = 450
        #self.page.window.resizable = False
        #self.page.window_always_on_top = True
        self.page.title = 'ToDo App'
        self.exec_sql("CREATE TABLE IF NOT EXISTS tasks(nome, status)")
        # self.result = self.exec_sql("SELECT * FROM tasks")
        self.task = ''
        self.view = 'all'
        self.result = self.lista(self.view)

        self.main_page()

    def lista(self, view):
        if view == 'all':
            return self.exec_sql("SELECT * FROM tasks")
        elif view == 'conpletas':
            return self.exec_sql("SELECT * FROM tasks WHERE status='completa'")
        elif view == 'inconpletas':
            return self.exec_sql("SELECT * FROM tasks WHERE status='incompleta'")

    def exec_sql(self, sql, params=[]):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute(sql, params)
            con.commit()
            return cur.fetchall()
        
    def checada(self, e):
        esta_concluida = e.control.value
        nome = e.control.label
        
        if esta_concluida:
            # Opcao 1
            self.exec_sql('UPDATE tasks SET status = "completa" WHERE nome=?',[nome])
        else:
            # Opcao 2
            sql = f'UPDATE tasks SET status = "incompleta" WHERE nome = "{nome}"'
            self.exec_sql(sql)

        self.atualiza_lista()

    
    def tasks_container(self):
        self.result = self.exec_sql("SELECT * FROM tasks")
        return ft.Container(
            height = self.page.height * .8,
            content = ft.Column(
                controls = [
                    ft.Checkbox(
                        label = res[0],
                        value = False if res[1] == 'incompleta' else True,
                        on_change=self.checada
                    ) for res in self.result if res
                ]
            )
        )
    
    def valorCampo(self, e):
        self.task = e.control.value
        print(self.task)

    def ad_tarefa(self, e, fld_tarefa):
        nome = self.task
        status = 'incompleta'

        if nome:
            sql = "INSERT INTO tasks VALUES(?,?)"
            self.exec_sql(sql,params=[nome, status])
            fld_tarefa.value = ''
            self.atualiza_lista()

    def atualiza_lista(self):
        tarefas = self.tasks_container()
        self.page.controls.pop()
        self.page.add(tarefas)
        self.page.update()

    def trocaTab(self, e):
        tab = e.control.selected_index
        if tab == 0:
            self.result = self.lista('all')
        elif tab == 1:
            self.result = self.lista('completas')
        elif tab == 2:
            self.result = self.lista('incompletas')
    
    def main_page(self):
        fld_tarefa = ft.TextField(
            hint_text='Digite uma taefa',
            expand=True,
            on_change = self.valorCampo
        )

        input_bar = ft.Row(
            controls=[
                fld_tarefa,
                ft.FloatingActionButton(
                    icon=ft.icons.ADD,
                    on_click = lambda e: self.ad_tarefa(e, fld_tarefa)
                )
            ]
        )

        tabs = ft.Tabs(
            selected_index=0,
            on_change=self.trocaTab,
            tabs = [
                ft.Tab(text='Todas'),
                ft.Tab(text='Em andamento'),
                ft.Tab(text='Finalizado')
            ]
        )

        tasks = self.tasks_container()

        self.page.add(input_bar, tabs, tasks)

ft.app(target = ToDo)
