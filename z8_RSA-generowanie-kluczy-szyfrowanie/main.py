'''
Zadanie: IMPLEMENTACJA RSA

1. Generowanie kluczy
p=? p=... (czy p pierwsza)
q=? q=... (czy q pierwsza)

2. wybieranie e :     1 < e < φ(n) NWD(e, φ(n)) = 1
e=? (lub losowanie e)

3. liczysz odwrotność modulo: d * e ≡ 1 (mod φ(n))
d=...

4. Tekst -> liczby
dzielisz tekst na kawałki i zamieniasz na liczby
Tekst = 45 36 27 itd

5. Szyfrowanie dla każdego m_i:  c_i = m_i^e mod n

m_i=... ... ... ... ... ... ... ... ... ...
c_i=... ... ... ... ... ... ... ... ... ...

6. Odszyfrowanie dla każdego c_i: m_i = c_i^d mod n
m_i= ... ... ... ... ... ... ... ... ... ...

7. Powrót do tekstu ( zamieniasz liczby z powrotem na znaki)
Tekst = ..............

AD. zrobic wieksze n tak do 2 bajtow
brac tekst po 2 znaki i zamieniac je na liczbe

p = 257
q = 263
e = 17
'''

import random
import math


def czy_pierwsza(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def nwd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def odwrotnosc_modulo(e, phi):
    t, new_t = 0, 1
    r, new_r = phi, e

    while new_r != 0:
        q = r // new_r
        t, new_t = new_t, t - q * new_t
        r, new_r = new_r, r - q * new_r

    if r != 1:
        return None

    if t < 0:
        t += phi

    return t


def losuj_liczbe_pierwsza(min_w=100, max_w=300):
    pierwsze = []
    for i in range(min_w, max_w + 1):
        if czy_pierwsza(i):
            pierwsze.append(i)
    return random.choice(pierwsze)


def wybierz_e(phi):
    mozliwe = []
    for e in range(2, phi):
        if nwd(e, phi) == 1:
            mozliwe.append(e)
    return random.choice(mozliwe)


def szyfruj_tekst(tekst, e, n):
    m_lista = [ord(znak) for znak in tekst]
    c_lista = [pow(m, e, n) for m in m_lista]
    return m_lista, c_lista


def odszyfruj_tekst(c_lista, d, n):
    m_lista = [pow(c, d, n) for c in c_lista]
    tekst = "".join(chr(m) for m in m_lista)
    return m_lista, tekst


def pobierz_pierwsza(nazwa):
    while True:
        x = int(input(f"Podaj {nazwa}: "))
        if czy_pierwsza(x):
            return x
        print(f"{nazwa} nie jest liczbą pierwszą. Spróbuj jeszcze raz.")


def main():
    print("=== IMPLEMENTACJA RSA ===")
    print("1 - wpisz p i q ręcznie")
    print("2 - wylosuj p i q")
    wybor = input("Wybierz opcję: ")

    if wybor == "1":
        p = pobierz_pierwsza("p")
        q = pobierz_pierwsza("q")
        while p == q:
            print("p i q nie powinny być takie same.")
            q = pobierz_pierwsza("q")
    else:
        p = losuj_liczbe_pierwsza()
        q = losuj_liczbe_pierwsza()
        while p == q:
            q = losuj_liczbe_pierwsza()

    n = p * q
    phi = (p - 1) * (q - 1)

    print("\n--- Generowanie kluczy ---")
    print(f"p = {p}")
    print(f"q = {q}")
    print(f"n = p * q = {n}")
    print(f"phi(n) = (p - 1) * (q - 1) = {phi}")

    print("\n1 - wpisz e ręcznie")
    print("2 - wylosuj e")
    wybor_e = input("Wybierz opcję: ")

    if wybor_e == "1":
        while True:
            e = int(input("Podaj e: "))
            if 1 < e < phi and nwd(e, phi) == 1:
                break
            print("Niepoprawne e. Musi spełniać: 1 < e < phi(n) oraz NWD(e, phi(n)) = 1.")
    else:
        e = wybierz_e(phi)

    d = odwrotnosc_modulo(e, phi)

    print(f"e = {e}")
    print(f"d = {d}")

    print("\nKlucz publiczny:")
    print(f"({n}, {e})")

    print("Klucz prywatny:")
    print(f"({n}, {d})")

    tekst = input("\nPodaj tekst do zaszyfrowania: ")

    max_kod = max(ord(znak) for znak in tekst) if tekst else 0
    if max_kod >= n:
        print("\nBŁĄD:")
        print("Kod co najmniej jednego znaku jest większy lub równy n.")
        print("Wybierz większe p i q.")
        return

    m_lista, c_lista = szyfruj_tekst(tekst, e, n)
    m_odzyskane, tekst_odzyskany = odszyfruj_tekst(c_lista, d, n)

    print("\n--- Tekst -> liczby ---")
    print("m_i =", " ".join(str(x) for x in m_lista))

    print("\n--- Szyfrowanie ---")
    print("c_i =", " ".join(str(x) for x in c_lista))

    print("\n--- Odszyfrowanie ---")
    print("m_i =", " ".join(str(x) for x in m_odzyskane))

    print("\n--- Powrót do tekstu ---")
    print("Tekst =", tekst_odzyskany)


if __name__ == "__main__":
    main()
