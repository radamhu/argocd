mghk = ['a', 'e', 'i', 'o', 'u']
szoveg = input('Adjon meg egy szót/szöveget! ')

for mgh in mghk:
    szamlalo = 0
    poziciok = []

    for index, karakter in enumerate(szoveg):
        if mgh == karakter.lower():
            szamlalo += 1
            poziciok.append(str(index + 1))
    
    if szamlalo == 0:
        print(f'A szóban nincs "{mgh}" magánhangzó!')
    else:
        print(f'A szóban az "{mgh}" magánhangzó {szamlalo} alkalommal fordul elő az {"., ".join(poziciok)}. helyen!')

