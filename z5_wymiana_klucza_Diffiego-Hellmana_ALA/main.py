# działa z perspektywy jednej osoby w Diffie-Hellman key exchange (Ala i Bob)
# funkcja do a^b mod c przez rozkład na potęgi dwójki

def mod_pow(a, b, c):
    wynik = 1
    a %= c
    while b > 0:
        if b % 2 == 1:
            wynik = (wynik * a) % c
        a = (a * a) % c
        b //= 2
    return wynik


# test próbnego dzielenia
def czy_pierwsza(p):
    if p < 2:
        return False
    i = 2
    while i * i <= p:
        if p % i == 0:
            return False
        i += 1
    return True


def ala():
    g, p, a = map(int, input("podaj g p a\n").split())

    if not czy_pierwsza(p):
        print("p nie jest pierwsza")
        return

    A = mod_pow(g, a, p)
    print("wyslij do Boba A:", A)

    B = int(input("podaj B od Boba: "))

    K = mod_pow(B, a, p)
    print("wspolny klucz K:", K)


def main():
    ala()


if __name__ == "__main__":
    main()