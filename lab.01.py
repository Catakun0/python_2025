while True:
    numele_utilizatorului = input("Introduceti numele dv: ")
    if numele_utilizatorului:
        print(f"Salut {numele_utilizatorului}")
        break
    else:
        print("va rog sa introduceti un nume valid!")

numar_intreg = 2012
numar_real = 402.24567
string_simplu = "Hello"
string_pe_siruri = """Si am rons cu unghia pe tencuiala
pe un perete cu firida goala
pe intruneric in singuratate"""

formarea_textului = "\nNumarul intreg: {} numar_real: {} text simplu: {} text_cu siruri: {} marimea textului nr2: {}"
print(formarea_textului.format(numar_intreg, numar_real, 
                               string_simplu, string_pe_siruri, len(string_pe_siruri)))
                               
print(f"\nTipul de date al numarului intreg: {type(numar_intreg)} si tipul de date al stringului: {type(string_simplu)}")

print(f"\nText uper: {string_simplu.upper()}")

text_taiat = string_pe_siruri[5:50]
print(f"\nText taiat din strofa: {text_taiat}")
