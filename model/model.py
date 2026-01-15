import copy

from networkx.classes import neighbors

from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._G = nx.DiGraph()
        self._list_products = []
        self._dict_products = {} # map id -> product
        self._list_sales = []

        self._best_percorso = []
        self._max_costo = 0

    def get_date_range(self):
        return DAO.get_date_range()

    def get_categories(self):
        return DAO.read_categories()

    def get_sales(self):
        result = []
        for p1 in self._G.nodes():
            score = 0
            for e_out in self._G.out_edges(p1, data=True):
                score += e_out[2]['weight']
            for e_in in self._G.in_edges(p1, data=True):
                score -= e_in[2]['weight']

            result.append((p1, score))

        return result

    def get_nodes(self):
        return self._G.nodes()

    def build_graph(self, c, start, end):
        self._G.clear()
        self._list_products = DAO.read_products(c)
        self._G.add_nodes_from(self._list_products)

        for p in self._list_products:
            self._dict_products[p.id] = p

        self._list_sales = DAO.read_sales(self._list_products, self._dict_products, start, end)
        for i, s in enumerate(self._list_sales):
            for s1 in self._list_sales[i+1:]:
                weight = s.n_ordini + s1.n_ordini
                if s.n_ordini == s1.n_ordini:
                    self._G.add_edge(s.product, s1.product, weight=weight)
                    self._G.add_edge(s1.product, s.product, weight=weight)
                elif s.n_ordini > s1.n_ordini:
                    self._G.add_edge(s.product, s1.product, weight=weight)
                else :
                    self._G.add_edge(s1.product, s.product, weight=weight)

        return self._G.number_of_nodes(), self._G.number_of_edges()

    def get_percorso(self, start_id, end_id, l):
        start = self._dict_products[start_id]
        end = self._dict_products[end_id]
        parziale = [start]
        self._ricorsione(parziale, end, l)

        return self._best_percorso, self._max_costo

    def _ricorsione(self, parziale, end, l):
        if len(parziale) == l:
            if parziale[-1] == end:
                peso = self.calcola_peso(parziale)
                if peso > self._max_costo:
                    self._max_costo = peso
                    self._best_percorso = copy.deepcopy(parziale)
            return

        for p in self._G.successors(parziale[-1]):
            if p not in parziale:
                parziale.append(p)
                self._ricorsione(parziale, end, l)
                parziale.pop()

    def calcola_peso(self, parziale):
        peso = 0
        for i in range(len(parziale)-1):
            u = parziale[i]
            v = parziale[i+1]
            peso += self._G[u][v]['weight']

        return peso