#do 2^61-1 wypisywać w formie tabelki i porównanie 3 metod dla jednej liczby ktora poda user
def sito_eratostenesa(limit):
    if limit < 2:
        return []

    pierwsze = [True] * (limit + 1)
    pierwsze[0] = False
    pierwsze[1] = False

    i = 2
    while i * i <= limit:
        if pierwsze[i]:
            j = i * i
            while j <= limit:
                pierwsze[j] = False
                j += i
        i += 1

    wynik = []
    for i in range(2, limit + 1):
        if pierwsze[i]:
            wynik.append(i)

    return wynik


def probne_dzielenie(n):
    if n < 2:
        return False, None

    if n == 2:
        return True, None

    if n % 2 == 0:
        return False, 2

    d = 3
    while d * d <= n:
        if n % d == 0:
            return False, d
        d += 2

    return True, None


def lucas_lehmer(p):
    if p < 2:
        return False

    if p == 2:
        return True

    czy_p_pierwsze, _ = probne_dzielenie(p)
    if not czy_p_pierwsze:
        return False

    m = (1 << p) - 1
    s = 4

    for _ in range(p - 2):
        s = (s * s - 2) % m

    return s == 0


def linia():
    print("=" * 60)


def metoda_sito():
    linia()
    print("  SITO ERATOSTENESA")
    linia()

    n = int(input("Podaj górny zakres n: "))

    liczby_pierwsze = sito_eratostenesa(n)

    print(f"Liczby pierwsze <= {n}:")
    print(liczby_pierwsze)
    print(f"Łącznie: {len(liczby_pierwsze)} liczb")
    print()


def metoda_probne_dzielenie():
    linia()
    print("  PRÓBNE DZIELENIE")
    linia()

    n = int(input("Podaj liczbę n: "))

    czy_pierwsza, dzielnik = probne_dzielenie(n)

    print(f"Sprawdzana liczba: {n}")
    print("-" * 60)

    if czy_pierwsza:
        print(f"Liczba {n} jest pierwsza.")
        print("Nie znaleziono dzielnika w przedziale od 2 do sqrt(n).")
    else:
        print(f"Liczba {n} nie jest pierwsza.")
        if dzielnik is not None:
            print(f"Znaleziony dzielnik: {dzielnik}")
            print(f"Ponieważ {n} mod {dzielnik} = 0, liczba jest złożona.")
    print()


def metoda_lucas_lehmer():
    linia()
    print("  TEST LUCASA-LEHMERA")
    linia()

    p = int(input("Podaj wykładnik p dla liczby M_p = 2^p - 1: "))

    czy_p_pierwsze, dzielnik = probne_dzielenie(p)

    print(f"Sprawdzany wykładnik p: {p}")
    print(f"Badana liczba: M_{p} = 2^{p} - 1")
    print("-" * 60)

    if not czy_p_pierwsze:
        print(f"Wykładnik p = {p} nie jest liczbą pierwszą.")
        if dzielnik is not None:
            print(f"Przykładowy dzielnik p: {dzielnik}")
        print("Test Lucasa-Lehmera można stosować tylko dla pierwszego p.")
        print(f"Zatem liczba 2^{p} - 1 nie jest liczbą pierwszą.")
        print()
        return

    wynik = lucas_lehmer(p)

    if wynik:
        print(f"Liczba 2^{p} - 1 jest pierwsza.")
    else:
        print(f"Liczba 2^{p} - 1 nie jest pierwsza.")
    print()


def menu():
    while True:
        linia()
        print("  SPRAWDZANIE LICZB PIERWSZYCH")
        linia()
        print("1 - Sito Eratostenesa")
        print("2 - Próbne dzielenie")
        print("3 - Test Lucasa-Lehmera")
        print("0 - Zakończ")
        print()

        wybor = input("Wybierz metodę: ")

        print()

        if wybor == "1":
            metoda_sito()
        elif wybor == "2":
            metoda_probne_dzielenie()
        elif wybor == "3":
            metoda_lucas_lehmer()
        elif wybor == "0":
            print("Koniec programu.")
            break
        else:
            print("Niepoprawny wybór.\n")

        input("Naciśnij Enter, aby wrócić do menu...")
        print()


menu()