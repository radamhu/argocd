# 2023. május - Ütemezés
# https://dload-oktatas.educatio.hu/erettsegi/feladatok_2023tavasz_emelt/e_digkult_23maj_fl.pdf

from pprint import pprint
taborok = []
with open('taborok.txt') as forrasfajl:
    for sor in forrasfajl:
        adatok = sor.strip().split('\t')
        tabor = {}
        tabor['tol'] = (int(adatok[0]), int(adatok[1]))
        tabor['ig'] = (int(adatok[2]), int(adatok[3]))
        tabor['diakok'] = adatok[4]
        tabor['tema'] = adatok[5]
        taborok.append(tabor)
# pprint(taborok, sort_dicts=False)

print('2. feladat\n')
print(f'Az adatsorok száma: {len(taborok)}')
print(f'Az először rögzített tábor témája: {taborok[0]["tema"]}')
print(f'Az utoljára rögzített tábor témája: {taborok[-1]["tema"]}')

print('3. feladat\n')
zenei_tabor = False
for tabor in taborok:
    if tabor['tema'] == 'zenei':
        zenei_tabor = True
        print(f'Zenei tábor kezdődik {tabor["tol"][0]}. hó {tabor["tol"][1]}. napján.')
if not zenei_tabor:
    print('Nem volt zenei tábor.')

print('4. feladat\n')
max_resztvevok = 0
legnepszerubbek = []
for tabor in taborok:
    if len(tabor["diakok"]) > max_resztvevok:
        max_resztvevok = len(tabor["diakok"])
        legnepszerubbek = []

    if len(tabor["diakok"]) == max_resztvevok:
        legnepszerubbek.append(tabor)
print('Legnépszerűbbek: ')
for tabor in legnepszerubbek:
    print(f'{tabor["tol"][0]} {tabor["tol"][1]} {tabor["tema"]}')

print('5. feladat\n')
def sorszam(h, n):
    if h == 6:
        return n - 15
    elif h == 7:
        return n + 15
    else:
        return n + 46

print('6. feladat\n')
ho = int(input(('hó: ')))
nap = int(input(('nap: ')))
szamlalo = 0
for tabor in taborok:
    if sorszam(tabor["tol"][0], tabor["tol"][1]) <= sorszam(ho, nap) <= sorszam(tabor["ig"][0], tabor["ig"][1]):
        szamlalo += 1
print(f'Ekkor éppen {szamlalo} tábor tart.')

print('7. feladat\n')
tanulo = input('Adja meg egy tanuló betűjelét: ')
megjelolt = []
for tabor in taborok:
    if tanulo in tabor['diakok']:
        megjelolt.append(tabor)
megjelolt.sort(key=lambda tabor: sorszam(tabor['tol'][0], tabor['tol'][1]))
# pprint(megjelolt, sort_dicts=False)
with open('egytanulo,txt', "w") as celfajl:
    for tabor in megjelolt:
        print(f'{tabor["tol"][0]}, {tabor["tol"][1]}-{tabor["ig"][0]}.{tabor["ig"][1]} {tabor["tema"]}', file=celfajl)

utkozes = False
for index in range(len(megjelolt) -1):
    if sorszam(megjelolt[index]['ig'][0], megjelolt[index]['ig'][1]) \
            >= sorszam(megjelolt[index]['tol'][0], megjelolt[index]['tol'][1]):
        utkozes = True
if utkozes:
    print('Nem meleht el mindegiyk táborba.')
else:
    print('Elmehet mindegyik táborba.')
