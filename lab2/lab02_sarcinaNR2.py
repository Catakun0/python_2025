preturi = [10, 15, 20]
produse = ["Mar", "Banana", "Portocala"]
for i in range(3):
    print("Produsul {} costa {} lei".format(produse[i], preturi[i]))

varsta = int(input("Introduceti varsta: "))
varsta_peste_5_ani = varsta + 5
print("In 5 ani veti avea " + str(varsta_peste_5_ani) + " ani")

if "Mar" in produse:
    print("Marul este in lista")

if "kiwi" not in produse:
    print("Kiwi nu este in lista")