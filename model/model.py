from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph() # grafo semplice e orientato (directed graph), non permette più archi tra
        # due nodi
        self.idMapFermate = {}
        for f in self._fermate:
            self.idMapFermate[f.id_fermata] = f
        # attenzione: se aggiungo archi tra nodi che non esistono mi crea nuovi nodi, fare attenzione
        # controllare prima e dopo di aggiungere i nodi se il numero rimane lo stesso


    # esploro il grafo per livelli, prima i vicini di source, poi i loro vicini, poi i loro vicini...
    def getBFSNodesFromEdges(self, source):
        archi = nx.bfs_edges(self._grafo, source) # saranno delle tuple
        nodiBFS = []
        for u, v in archi: # u partenza e v arrivo
            nodiBFS.append(v)
        return nodiBFS


    def getBFSNodesFromTree(self, source):
        tree = nx.bfs_tree(self._grafo, source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi # questo contiene anche il nodo source a differenza dell'altro metodo


    # esploro un nodo vicino a caso, poi un suo vicini, ... fino a che non ne posso visitare più allora faccio
    # un passo indietro e ricomincio fino a che li ho visitati tutti
    def getDFSNodesFromEdges(self, source):
        archi = nx.dfs_edges(self._grafo, source) # saranno delle tuple
        nodiDFS = []
        for u, v in archi: # u partenza e v arrivo
            nodiDFS.append(v)
        return nodiDFS


    def getDFSNodesFromTree(self, source):
        tree = nx.dfs_tree(self._grafo, source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi


    def buildGraph(self):
        self._grafo.clear() # prima mi assicuro che il grafo sia svuotato perchè se
        # schiaccio più volte potrei aggiungere i dati
        self._grafo.add_nodes_from(self._fermate) # mi fa aggiungere i nodi del grafo
        # che saranno le mie fermate
        self.addedges3()


    def buildGraphPesato(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        # per essere pesato cambia solo come aggiungo gli archi
        self.addedgesPesati()


    def addedges(self):
        # devo sapere se due fermate hanno una connessione, vado a prendere tutte le
        # possibili coppie di fermate e vedo se c'è una connessione tra loro
        self._grafo.clear_edges()
        for u in self._fermate:
            for v in self._fermate:
                if DAO.hasconn(u, v):
                    self._grafo.add_edge(u, v)  # aggiungo la coppia connessa
        # aggiungo un arco alla volta ma faccio una query ogni volta che lo devo aggiungere
        # ha senso farlo così se ho grafi piccoli perchè òa query è più facile


    def addedges2(self):
        self._grafo.clear_edges()
        for u in self._fermate:
            for conn in DAO.getVicini(u):
                v = self.idMapFermate[conn.id_stazA]
                self._grafo.add_edge(u, v)


    def addedges3(self):
        self._grafo.clear_edges()
        alledges = DAO.getAllEdges()
        for conn in alledges:
            u = self.idMapFermate[conn.id_stazP]
            v = self.idMapFermate[conn.id_stazA]
            self._grafo.add_edge(u, v)


    def addedgesPesati(self):
        # riutilizzo addedges3 contando quante volte provo ad aggiungere l'arco
        self._grafo.clear_edges()
        alledges = DAO.getAllEdges()
        for conn in alledges:
            u = self.idMapFermate[conn.id_stazP]
            v = self.idMapFermate[conn.id_stazA]
            if self._grafo.has_edge(u, v):
                self._grafo[u][v]["weight"] += 1 # accedo al grafo e aumento il suo peso dato che non e il primo
                # che incontro tra questi due nodi
            else:
                self._grafo.add_edge(u, v, weight = 1)


    def addedgesPesatiV2(self):
        # delega il calcolo del peso a query sql per semplificarci i calcoli in python
        self._grafo.clear_edges()
        alledges = DAO.getAllEdgesPesati()
        for conn in alledges:
            u = self.idMapFermate[conn[0]]
            v = self.idMapFermate[conn[1]]
            peso = conn[2]
            self._grafo.add_edge(u, v, weight = peso)


    def getArchiPesoMaggiore(self):
        edges = self._grafo.edges(data = True) # mi salvo così anche i pesi (tutti gli attributi)

        edgesMaggiori = []
        for e in edges:
            if self._grafo.get_edge_data(e[0], e[1])["weight"] > 1:
                # self._grafo[e[0]][e[1]]["weight"]
                edgesMaggiori.append(e)
        return edgesMaggiori


    @property
    def fermate(self):
        return self._fermate


    def get_numnodi(self):
        return len(self._grafo.nodes)


    def get_numarchi(self):
        return len(self._grafo.edges)

