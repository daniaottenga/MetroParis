# file che mi permette di fare delle prove per creare il grafo
from model.fermata import Fermata
from model.model import Model

model = Model()
model.buildGraphPesato()
print(f"Numero nodi: {model.get_numnodi()}")
print(f"Numero archi: {model.get_numarchi()}") # gli archi dovrebbero essere meno, ma ci sono fermate che sono
# gestite da più linee ma non vengono considerati, se aggiungoun arco tra due stazioni già collegate e non è un
# multigraph non lo aggiunge

source = Fermata(2, "Abbesses", 2.33855, 48.8843)
nodiBFS = model.getBFSNodesFromEdges(source)
nodiDFS = model.getDFSNodesFromEdges(source)
print(len(nodiDFS))
print(len(nodiBFS))
for i in range(10):
    print(nodiDFS[i])
print("_________________________________")
for i in range(10):
    print(nodiBFS[i])

print("=================================")
print("Archi con peso 2")
archiMaggiori = model.getArchiPesoMaggiore()
for a in archiMaggiori:
    print(a[0], "->", a[1], ":", a[2]["weight"])

