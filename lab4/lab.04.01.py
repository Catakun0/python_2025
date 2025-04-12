varsta = 21
inaltimea = 1.76
greutatea_actuala = 74
sexul = "M"

greutatea_ideala = -1

def caracteristiciile_actuale():
    print(f"Varsta ta: {varsta}")
    print(f"Inaltimea ta: {inaltimea}")
    print(f"Greutatea actuala: {greutatea_actuala}")
    print(f"Sexul: {sexul}")
#varsta
while True:
    try:
        varsta = int(input("Introducetiva varsta: \n"))
    except:
        print("Introduceti va rog o cifra corespunzatoare")
        continue

    if varsta <= 20 or 120 <= varsta:
        print("Varsta e nevoie sa fie mai mare de 20 si mai mica de 120")
        continue
    break
#inaltimea
while True:
    try:
        inaltimea = int(input("Introducetiva inaltimea: \n"))
    except:
        print("Introduceti va rog o cifra corespunzatoare")
        continue

    if inaltimea <= 150 or 220 <= inaltimea:
        print("Inaltimea e nevoie sa fie mai mare de 150 si mai mica de 220")
        continue
    break
#greutatea
while True:
    try:
        greutatea_actuala = int(input("Introducetiva greutatea: \n"))
    except:
        print("Introduceti va rog o cifra corespunzatoare")
        continue

    if  greutatea_actuala <= 45 or 300 <= greutatea_actuala:
        print("Greutatea e nevoie sa fie mai mare de 45 si mai mica de 300")
        continue
    break
#sexul
while True:
    try:
        while True:
            sexul = (input("Introducetiva sexul (M) - Masculin (F) - Femenin \n"))
            if sexul == "M" or sexul == "F": 
                next1 = True
                break
            else:
                print("Introduceti o optiune valida")
    except:
        print("Introduceti va rog o optiune corespunzatoare")
    if next1 == True:
        break

caracteristiciile_actuale()
input("Treceti mai departe")

a = 4 if sexul == "M" else 2.5
b = 4 if sexul == "M" else 6
gender_factor = (inaltimea - 150) / a + (varsta - 20) / b
greutatea_ideala = inaltimea - 100 - (gender_factor)

print(f"Greutatea ideala penrtru tine ar fi: {greutatea_ideala}")

if greutatea_actuala - greutatea_ideala > 0:
    print("Dute ba si slabeste ca esti mai gras de cat a ai crezut tu")
