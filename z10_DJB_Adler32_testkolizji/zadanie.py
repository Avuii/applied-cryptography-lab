'''
DJB
H0 = 5381
H -> H * 32 + H + znak(ASCII)

--------------------------------------------

Adler-32
A = 1
B = 0
p = 65521
'''
import random
import string
import math


def djb(tekst):
    h = 5381

    for znak in tekst:
        h = ((h << 5) + h) + ord(znak)
        h = h & 0xFFFFFFFF

    return h


def adler32(tekst):
    MOD = 65521

    A = 1
    B = 0

    for znak in tekst:
        A = (A + ord(znak)) % MOD
        B = (B + A) % MOD

    return (B << 16) + A


def hashuj_tekst():
    tekst = input("Podaj tekst: ")

    wynik_djb = djb(tekst)
    wynik_adler = adler32(tekst)

    print("\nWYNIKI:")
    print("DJB     =", wynik_djb, " HEX:", hex(wynik_djb))
    print("Adler32 =", wynik_adler, " HEX:", hex(wynik_adler))


def losowy_tekst(dlugosc):
    znaki = string.ascii_lowercase
    tekst = ""

    for i in range(dlugosc):
        tekst += random.choice(znaki)

    return tekst


def szansa_kolizji(n):
    m = 2 ** 32
    return 1 - math.exp(-(n * (n - 1)) / (2 * m))


def oczekiwana_liczba_kolizji(n):
    return (n * (n - 1)) / (2 * (2 ** 32))


def test_algorytmu(funkcja_hash, nazwa, n, D):
    hashe = {}

    kolizje = 0
    pierwsza_kolizja = None

    for i in range(n):
        tekst = losowy_tekst(D)
        h = funkcja_hash(tekst)

        if h in hashe and hashe[h] != tekst:
            kolizje += 1

            if pierwsza_kolizja is None:
                pierwsza_kolizja = (hashe[h], tekst, h)
        else:
            hashe[h] = tekst

    procent = (kolizje / n) * 100

    print("\n==============================")
    print(nazwa)
    print("D =", D)
    print("n =", n)
    print("Kolizje:", kolizje)
    print("Procent kolizji:", round(procent, 6), "%")

    if pierwsza_kolizja:
        print("\nPierwsza znaleziona kolizja:")
        print("Tekst 1:", pierwsza_kolizja[0])
        print("Tekst 2:", pierwsza_kolizja[1])
        print("Hash:", pierwsza_kolizja[2])
        print("HEX:", hex(pierwsza_kolizja[2]))
    else:
        print("\nNie znaleziono kolizji.")


def test_kolizji():
    n = int(input("Podaj n, np. 260000: "))

    print("\nSzansa na co najmniej jedną kolizję:", round(szansa_kolizji(n) * 100, 4), "%")
    print("Oczekiwana liczba kolizji:", round(oczekiwana_liczba_kolizji(n), 4))

    test_algorytmu(djb, "DJB", n, 12)
    test_algorytmu(djb, "DJB", n, 1000)
    test_algorytmu(adler32, "Adler32", n, 12)
    test_algorytmu(adler32, "Adler32", n, 1000)


while True:
    print("\n=== MENU ===")
    print("1. Hashowanie tekstu")
    print("2. Test kolizji")
    print("0. Wyjście")

    wybor = input("Wybierz opcję: ")

    if wybor == "1":
        hashuj_tekst()
    elif wybor == "2":
        test_kolizji()
    elif wybor == "0":
        print("Koniec programu.")
        break
    else:
        print("Nieprawidłowa opcja.")