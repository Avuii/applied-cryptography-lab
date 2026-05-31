'''
W = 10000
M = 100
D = 4
N = 1000
'''

import random
import string


def djb(tekst):
    h = 5381

    for znak in tekst:
        h = ((h << 5) + h) + ord(znak)
        h = h & 0xFFFFFFFF

    return h


def redukcja(hash_value, dlugosc, numer_iteracji=0):
    litery = string.ascii_lowercase
    tekst = ""

    hash_value = hash_value + numer_iteracji

    for i in range(dlugosc):
        indeks = hash_value % 26
        tekst += litery[indeks]
        hash_value //= 26

    return tekst


def losowy_tekst(dlugosc):
    return "".join(random.choice(string.ascii_lowercase) for _ in range(dlugosc))


def utworz_lancuch(start, liczba_iteracji, dlugosc):
    tekst = start

    for i in range(liczba_iteracji):
        h = djb(tekst)
        tekst = redukcja(h, dlugosc, i)

    return tekst


def utworz_tablice_hashow(liczba_wierszy, liczba_iteracji, dlugosc):
    tablica = {}

    for i in range(liczba_wierszy):
        start = losowy_tekst(dlugosc)
        koniec = utworz_lancuch(start, liczba_iteracji, dlugosc)

        tablica[koniec] = start

    return tablica


def szukaj_w_lancuchu(start, szukany_hash, liczba_iteracji, dlugosc):
    tekst = start

    for i in range(liczba_iteracji):
        h = djb(tekst)

        if h == szukany_hash:
            return tekst

        tekst = redukcja(h, dlugosc, i)

    return None


def szukaj_kolizji_dla_tekstu(tekst, tablica, liczba_iteracji, dlugosc):
    szukany_hash = djb(tekst)

    for pozycja in range(liczba_iteracji - 1, -1, -1):
        kandydat = tekst
        h = szukany_hash

        for i in range(pozycja, liczba_iteracji):
            kandydat = redukcja(h, dlugosc, i)
            h = djb(kandydat)

        koniec_lancucha = kandydat

        if koniec_lancucha in tablica:
            start = tablica[koniec_lancucha]

            znaleziony_tekst = szukaj_w_lancuchu(
                start,
                szukany_hash,
                liczba_iteracji,
                dlugosc
            )

            if znaleziony_tekst is not None and znaleziony_tekst != tekst:
                return znaleziony_tekst, szukany_hash

    return None, szukany_hash


def testuj_kolizje():
    W = int(input("Podaj liczbę wierszy W: "))
    M = int(input("Podaj liczbę iteracji M: "))
    D = int(input("Podaj długość tekstu D: "))
    N = int(input("Ile tekstów testować: "))

    print("\nTworzenie tablicy hashów...")
    tablica = utworz_tablice_hashow(W, M, D)

    print("Liczba końców łańcuchów w tablicy:", len(tablica))
    print("\nSzukanie kolizji...\n")

    znalezione = 0
    pierwsza_kolizja = None

    for i in range(N):
        tekst = losowy_tekst(D)

        znaleziony, h = szukaj_kolizji_dla_tekstu(
            tekst,
            tablica,
            M,
            D
        )

        if znaleziony is not None:
            znalezione += 1

            if pierwsza_kolizja is None:
                pierwsza_kolizja = (tekst, znaleziony, h)

    print("=== PODSUMOWANIE ===")
    print("Wiersze W:", W)
    print("Iteracje M:", M)
    print("Długość D:", D)
    print("Testowane teksty:", N)
    print("Liczba znalezionych kolizji:", znalezione)

    if pierwsza_kolizja:
        tekst1, tekst2, h = pierwsza_kolizja

        print("\nPierwsza znaleziona kolizja:")
        print("Tekst 1:", tekst1)
        print("Tekst 2:", tekst2)
        print("Hash:", h)
        print("HEX:", hex(h))
    else:
        print("\nNie znaleziono kolizji.")


def menu():
    while True:
        print("\n=== MENU ===")
        print("1. Policz hash DJB")
        print("2. Test kolizji z tablicą hashów")
        print("0. Wyjście")

        wybor = input("Wybierz opcję: ")

        if wybor == "1":
            tekst = input("Podaj tekst: ")
            h = djb(tekst)
            print("DJB =", h)
            print("HEX =", hex(h))

        elif wybor == "2":
            testuj_kolizje()

        elif wybor == "0":
            print("Koniec programu.")
            break

        else:
            print("Nieprawidłowa opcja.")


menu()