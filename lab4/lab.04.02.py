mai_mica_de_un_an = False
if input("Pisica este mai mica de un an? \n 1 - Yes \n 2 - No \n") == "1":
    mai_mica_de_un_an = True

# lookup table
varsta_pisic_om = {
    1: "6 luni",
    2: "10 luni",
    3: "2 ani",
    4: "5 ani",
    5: "8 ani",
    6: "14 ani",
    7: "15 ani",
    8: "16 ani",
    9: "16 ani",
    10: "16 ani",
    11: "16 ani",
}

if mai_mica_de_un_an:
    selector = 1
    while True:
        try:
            selector = int(input("Cate luni are pisoiul? \n 1 - 11 (luni) \n"))
        except ValueError:
            print("Introduceti va rog o cifra valida")
        if selector < 1 or selector > 11:
            print("Introduceti va rog o cifra intre 1 - 11!")
            continue
        break

    print(f"Pisica are {varsta_pisic_om[selector]} omenesti")

def calcularea_vasrtei(varsta_pisica: int) -> int:
    if varsta_pisica == 1:
        return 18
    elif varsta_pisica == 2:
        return 25 + 18
    elif 3 <= varsta_pisica <= 15:
        return 25 + 18 + (varsta_pisica - 2) * 4
    else: 
        return 25 + 18 + (13 * 4) + (varsta_pisica - 15) * 3
    

if mai_mica_de_un_an == False:
    while True:
        try:
            anii_pisicii = int(input("Cati ani are pisica? \n"))
            if anii_pisicii >= 1 and 35 >= anii_pisicii:
                print(f"In ani omenesti pisoiul are {calcularea_vasrtei(anii_pisicii)} ani omenesti")
                break
            else:
                print("Introduceti un an valid intre 1 - 35")
        except ValueError:
            print("Introduceti va rog o cifra valida")

