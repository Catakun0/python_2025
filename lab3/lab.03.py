greet_user = lambda name : print('Hello My Dear, ', name)
user_name = input("What is your name? ")
greet_user(greet_user)

def initializarea_numarului():
    while True:
        try:
            numarul = int(input("Introduceti un numar"))
            return numarul
        except:
            print("Introdu un numar valid")    


def void_ridicam_la_patrat(numarul_nostru):
    return ridicarea_la_patrat(numarul_nostru)

def adunarea_simpla(a = 10, b = 10):
    return a + b

def lambda_noastra(x):
    return x[1]

lista_noastra = [(3, 11), (1, 7), (7, 8), (16, 88), (23, 15)]
print(f"Lista initiala: {lista_noastra}")
lista_sortata = sorted(lista_noastra, key = lambda x : x[1])
print(f"Lista sortata: {lista_sortata}")

ridicarea_la_patrat = lambda numarul_nostru : numarul_nostru * numarul_nostru
numarul_nostru = initializarea_numarului()
print(f"Ridicarea la patrat a numarului {numarul_nostru} este: {void_ridicam_la_patrat(numarul_nostru)}")
print(f"Adunarea executata: {adunarea_simpla()}")
print(f"Adunarea executata: {adunarea_simpla(40, 50)}")


sfasf = lambda_noastra

def f():
    def g():
        print(8998)

    return g

f()
f()
