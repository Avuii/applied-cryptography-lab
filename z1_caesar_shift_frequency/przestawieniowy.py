"""Musimy napisać szyfr przestawieniowy w pythonie, który działa w następujący sposób
1. Dane bierzemy z pliku .txt i wyrzucamy do pliku .txt
2. Użytkownik wybiera czy szyfrujemy/deszyfrujemy oraz przesunięcie
3. Nasz alfabet to litery + liczby 0-9
4. Znaki diakretyczne i polskie zostawiamy tak jak były bez zmian
"""
def szyfr():
    tryb = input("Szyfownie czy deszyfrowanie (s lub d)").strip().lower()
    przesuniecie = int(input("Przesunięcie: ").strip())

    alfabet = "abcdefghijklmnopqrstuvwxyz0123456789"

    if tryb == "d":
        przesuniecie = -przesuniecie

    with open("out.txt", "r", encoding="utf-8") as f:
        tekst = f.read()

    wynik = ""

    for znak in tekst:
        z = znak.lower()

        if z in alfabet:
            i = alfabet.index(z)
            nowy_i = (i + przesuniecie) % len(alfabet)
            wynik = wynik + alfabet[nowy_i]
        else:
            wynik = wynik + znak

    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(wynik)

    print("Zapisane do: output.txt")

szyfr()

"""
~~~~Druga część programu~~~~
1. Wcztuje tekst z pliku
2. Zlicza litery i cyfry
3. Dla każdej podaje jaką cześcią wszystkich jest
4. Dostajemy procenty, ale dzielimy przez liczbę liter a nie znaków, żeby nie wliczać spacji enterów itd.
5. Duże i małe litery zliczamy raz(chodzi o to aby nie rozróżniać jak poprzednio)
6. Znaleźć przesunięcie żeby odszyfrować tekst zaszyfrowany.
"""
def analiza():
    with open("out.txt", "r", encoding="utf-8") as f:
        tekst = f.read()

    alfabet = "abcdefghijklmnopqrstuvwxyz0123456789"

    liczniki = {}
    for znak in alfabet:
        liczniki[znak] = 0

    suma_liter_i_cyfr = 0

    for znak in tekst:
        z = znak.lower()
        if z in alfabet:
            liczniki[z] = liczniki[z] + 1
            suma_liter_i_cyfr = suma_liter_i_cyfr + 1

    print("Suma liter i cyfr (bez spacji/enterów itd.):", suma_liter_i_cyfr)

    for znak in alfabet:
        if suma_liter_i_cyfr == 0:
            procent = 0
        else:
            procent = (liczniki[znak] / suma_liter_i_cyfr) * 100

        print(znak, "->", liczniki[znak], "(", round(procent, 2), "% )")

analiza()
