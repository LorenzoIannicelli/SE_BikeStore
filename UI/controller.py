from UI.view import View
from model.model import Model
import flet as ft
import datetime

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def set_dates(self):
        first, last = self._model.get_date_range()

        self._view.dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view.dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp2.current_date = datetime.date(last.year, last.month, last.day)

    def populate_dd(self):
        result = []
        categories_dict = self._model.get_categories()

        for c_id in categories_dict:
            result.append(ft.DropdownOption(key= c_id, text=categories_dict[c_id]))

        return result

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """
        category = int(self._view.dd_category.value)
        start_date = self._view.dp1.value
        end_date = self._view.dp2.value
        nodes, edges = self._model.build_graph(category, start_date, end_date)

        self._view.txt_risultato.controls.clear()

        self._view.txt_risultato.controls.append(ft.Text('Date selezionate:'))
        self._view.txt_risultato.controls.append(ft.Text(f'Start date: {start_date}'))
        self._view.txt_risultato.controls.append(ft.Text(f'End date: {end_date}'))

        txt1 = f'Numero di nodi: {nodes}'
        txt2 = f'Numero di archi: {edges}'
        self._view.txt_risultato.controls.append(ft.Text('Grafo correttamente creato:'))
        self._view.txt_risultato.controls.append(ft.Text(txt1))
        self._view.txt_risultato.controls.append(ft.Text(txt2))

        self._view.update()


    def handle_best_prodotti(self, e):
        """ Handler per gestire la ricerca dei prodotti migliori """
        sales = self._model.get_sales()
        sales.sort(key=lambda x: x[1], reverse=True)
        selected_sale = sales[:5]

        self._view.txt_risultato.controls.append(ft.Text('I cinque prodotti più venduti sono:'))
        for s in selected_sale:
            txt = f'{s[0]} with score {s[1]}'
            self._view.txt_risultato.controls.append(ft.Text(txt))
        self._view.update()

    def handle_cerca_cammino(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
