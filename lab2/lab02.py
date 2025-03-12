lista_mia = [20, 30, 50, 1000, -100, 1, 2]
print(f"prima valoare: {lista_mia[0]}, si a doua valoare {lista_mia[2]}")

lista_mia[2] = 2000

lista_extractata_mia = lista_mia[1 : 4]

lista_mia.append(-10)

lungimea_listei_mia = len(lista_mia)
print(lungimea_listei_mia)
suma_listei_mele = sum(lista_mia)
print(suma_listei_mele)

lista_mia[0] = lista_mia[0] * 2
number_exista = 30 in lista_mia
lista_mia_de_3_ori = lista_mia * 3

print(f"imultirea: {lista_mia[0]}, exista 30 in lista?: {number_exista}, \nLista dublicata de 3 ori:\n{lista_mia_de_3_ori}")

input("\napasa ori ce sa treci mai departe!")

tuple_ul_meu = (20, 50, 100, -100, 10, 300)
print(f"tipul de date: {type(tuple_ul_meu)}")
print(f"prima valoare {tuple_ul_meu[0]} si ultima valoare {tuple_ul_meu[-1]}")
taiturea_tuplului = tuple_ul_meu[2: 4]

lungimea_tuplului = len(tuple_ul_meu)
suma_tuplului_meu = sum(tuple_ul_meu)
valoarea_minimi_din_tuplu = min(tuple_ul_meu)

input("\napasa ori ce sa treci mai departe!")

setul_mieu = {20, 50, 100, -100, 30, 1000, 1000}

print(f"setul mieu:\n{setul_mieu}")
setul_mieu.add(10001)
print(f"lungimea setului: {len(setul_mieu)}")

input("\napasa ori ce sa treci mai departe!")

dictionarul_mieu = {"Numele romanului": "Taramul scufundat in lava", "Anul nasterii romanului": 2070, "Varsta minima": "-1+"}

print(f"\nNumele romanului mieu: {dictionarul_mieu['Numele romanului']} si anul publicarii: {dictionarul_mieu['Anul nasterii romanului']}")

del dictionarul_mieu['Anul nasterii romanului']
print(f"Numele tipului dictionarului: {type(dictionarul_mieu)}")

dictionarul_mieu["Varsta minima"] = 16

al_doilea_dictionar = {"Autorul": "Master Kufilaka"}

dictionarul_mieu.update(al_doilea_dictionar)
print(dictionarul_mieu)

avem_un_int = 1000
print(type(avem_un_int))
avem_un_int = "1k"
print(type(avem_un_int))



