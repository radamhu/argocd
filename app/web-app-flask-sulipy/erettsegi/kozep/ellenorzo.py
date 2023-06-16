# Digitális kultúra érettségi 2023. május középszint idegen nyelvű feladat | Programozás | Python
taj_szam = input('Kérem a TAJ-számot: ')
ellenorzoszam = int(taj_szam[-1])

print(f'Az ellenőrzős zámjegy: {ellenorzoszam}')

osszeg = 0
for index in range(8):
    if (index + 1) % 2 != 0:
        osszeg += int(taj_szam[index]) * 3
    else:
        osszeg += int(taj_szam[index]) * 7

print(f'A szorzatok összege: {osszeg}')
if osszeg % 10 == ellenorzoszam:
    print('Helyes a szám')
else:
    print('Hibás a szám')
