def sito_eratostenesa(n):
    if n < 2:
        return False

    pierwsze = [True] * (n + 1)
    pierwsze[0] = False
    pierwsze[1] = False

    i = 2
    while i * i <= n:
        if pierwsze[i]:
            j = i * i
            while j <= n:
                pierwsze[j] = False
                j += i
        i += 1

    return pierwsze[n]

def probne_dzielenie(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
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


print("Wybierz metode:")
print("1 - Sito Eratostenesa")
print("2 - Probne dzielenie")
print("3 - Test Lucasa-Lehmera")

wybor = input("metoda: ")

if wybor == "1":
    n = int(input("Podaj liczbe n: "))
    if sito_eratostenesa(n):
        print("Liczba", n, "jest pierwsza")
    else:
        print("Liczba", n, "nie jest pierwsza")

elif wybor == "2":
    n = int(input("Podaj liczbe n: "))
    if probne_dzielenie(n):
        print("Liczba", n, "jest pierwsza")
    else:
        print("Liczba", n, "nie jest pierwsza")

elif wybor == "3":
    p = int(input("Podaj wykladnik p: "))
    if lucas_lehmer(p):
        print("Liczba 2^" + str(p) + " - 1 jest pierwsza")
    else:
        print("Liczba 2^" + str(p) + " - 1 nie jest pierwsza")

else:
    print("Niepoprawny wybor")