# wypisać liczby pierwsze do 2^61-1
# dla każdej liczby pierwszej sprawdzić 3 metodami czy jest pierwsza
# porownac wyniki 3 metod: Sito Eratostenesa, Próbne dzielenie, Test Lucasa-Lehmera
LIMIT_SITO = 10_000_000


def sito_eratostenesa(limit):
    if limit < 2:
        return []

    prime = [True] * (limit + 1)
    prime[0] = False
    prime[1] = False

    i = 2
    while i * i <= limit:
        if prime[i]:
            j = i * i
            while j <= limit:
                prime[j] = False
                j += i
        i += 1

    wynik = []
    for i in range(2, limit + 1):
        if prime[i]:
            wynik.append(i)

    return wynik


def czy_pierwsza_sitem(n):
    if n < 2:
        return False
    if n > LIMIT_SITO:
        return None

    prime = [True] * (n + 1)
    prime[0] = False
    prime[1] = False

    i = 2
    while i * i <= n:
        if prime[i]:
            j = i * i
            while j <= n:
                prime[j] = False
                j += i
        i += 1

    return prime[n]


def probne_dzielenie(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2

    return True


def lucas_lehmer(p):
    if p < 2:
        return False
    if p == 2:
        return True

    if not probne_dzielenie(p):
        return False

    m = (1 << p) - 1
    s = 4

    for _ in range(p - 2):
        s = (s * s - 2) % m

    return s == 0


def formatuj_wynik(w):
    if w is None:
        return "ZA DUŻA"
    return "TAK" if w else "NIE"


def linia():
    print("=" * 95)


def porownanie_mersenne_do_61():
    linia()
    print("PORÓWNANIE 3 METOD DLA LICZB MERSENNE'A M_p = 2^p - 1, GDZIE p <= 61")
    linia()

    wykladniki_p = sito_eratostenesa(61)

    print(f"{'p':>4} {'M_p = 2^p - 1':>24} {'Sito':>12} {'Próbne':>12} {'Lucas-Lehmer':>15}")
    print("-" * 95)

    for p in wykladniki_p:
        mp = (1 << p) - 1

        wynik_sito = czy_pierwsza_sitem(mp)
        wynik_probne = probne_dzielenie(mp)
        wynik_ll = lucas_lehmer(p)

        print(
            f"{p:>4} "
            f"{mp:>24} "
            f"{formatuj_wynik(wynik_sito):>12} "
            f"{formatuj_wynik(wynik_probne):>12} "
            f"{formatuj_wynik(wynik_ll):>15}"
        )

    print()
    print("Uwagi:")
    print(f"- Sito Eratostenesa działa tu tylko do {LIMIT_SITO:,}, dlatego dla większych M_p pokazuje 'ZA DUŻA'.")
    print("- Próbne dzielenie działa dla każdej liczby, ale dla dużych wartości jest wolne.")
    print("- Test Lucasa-Lehmera działa tylko dla liczb Mersenne’a M_p = 2^p - 1.")
    print()


porownanie_mersenne_do_61()