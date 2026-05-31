ALFABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def przygotuj_haslo(haslo):
    haslo = haslo.upper()
    wynik = ""

    for znak in haslo:
        if znak in ALFABET:
            wynik += znak

    return wynik


def tylko_znaki_alfabetu(tekst):
    wynik = ""

    for znak in tekst.upper():
        if znak in ALFABET:
            wynik += znak

    return wynik


def vigenere(tekst, haslo, tryb):
    tekst = tekst.upper()
    haslo = przygotuj_haslo(haslo)

    if len(haslo) == 0:
        print("Błąd: hasło musi zawierać przynajmniej jedną literę lub cyfrę z alfabetu A-Z, 0-9.")
        return ""

    wynik = ""
    indeks_hasla = 0
    dlugosc_alfabetu = len(ALFABET)

    for znak in tekst:
        if znak in ALFABET:
            indeks_tekstu = ALFABET.index(znak)
            znak_hasla = haslo[indeks_hasla % len(haslo)]
            indeks_hasla_znaku = ALFABET.index(znak_hasla)

            if tryb == "s":
                nowy_indeks = (indeks_tekstu + indeks_hasla_znaku) % dlugosc_alfabetu
            elif tryb == "d":
                nowy_indeks = (indeks_tekstu - indeks_hasla_znaku) % dlugosc_alfabetu
            else:
                print("Błąd: nieznany tryb.")
                return ""

            wynik += ALFABET[nowy_indeks]
            indeks_hasla += 1
        else:
            wynik += znak

    return wynik


def wydziel_kolumny(tekst_bez_znakow, dlugosc_hasla):
    kolumny = []

    for i in range(dlugosc_hasla):
        kolumna = ""
        j = i

        while j < len(tekst_bez_znakow):
            kolumna += tekst_bez_znakow[j]
            j += dlugosc_hasla

        kolumny.append(kolumna)

    return kolumny


def odszyfruj_cezar_fragment(fragment, przesuniecie):
    wynik = ""
    n = len(ALFABET)

    for znak in fragment:
        indeks = ALFABET.index(znak)
        nowy_indeks = (indeks - przesuniecie) % n
        wynik += ALFABET[nowy_indeks]

    return wynik


def policz_score(fragment):
    czeste = "AEIOZNRSTW1234567890"
    score = 0

    for znak in fragment:
        if znak in czeste:
            score += 2
        elif znak in ALFABET:
            score += 1

    for znak in "AEIOANRSTZ":
        score += fragment.count(znak)

    return score


def znajdz_najlepsze_przesuniecie_dla_fragmentu(fragment):
    najlepsze_przesuniecie = 0
    najlepszy_score = -1

    for przesuniecie in range(len(ALFABET)):
        kandydat = odszyfruj_cezar_fragment(fragment, przesuniecie)
        score = policz_score(kandydat)

        if score > najlepszy_score:
            najlepszy_score = score
            najlepsze_przesuniecie = przesuniecie

    return najlepsze_przesuniecie


def znajdz_haslo(tekst, dlugosc_hasla):
    tekst_bez_znakow = tylko_znaki_alfabetu(tekst)

    if len(tekst_bez_znakow) == 0:
        return ""

    kolumny = wydziel_kolumny(tekst_bez_znakow, dlugosc_hasla)

    haslo = ""

    for kolumna in kolumny:
        przesuniecie = znajdz_najlepsze_przesuniecie_dla_fragmentu(kolumna)
        haslo += ALFABET[przesuniecie]

    return haslo


def score_calego_tekstu(tekst):
    score = 0
    tekst = tekst.upper()

    for znak in tekst:
        if znak in "AEIOZNRSTW":
            score += 3
        elif znak in ALFABET:
            score += 1
        elif znak in " \n\t.,;:!?-()":
            score += 0

    czeste_fragmenty = ["A", "I", "Z", "NA", "TO", "TA", "NIE", "THE", "AND", "ING"]
    for frag in czeste_fragmenty:
        score += tekst.count(frag) * 2

    return score


def automatyczne_lamanie(tekst, max_dlugosc_hasla):
    najlepsze_haslo = ""
    najlepszy_wynik = ""
    najlepszy_score = -1

    for dlugosc in range(1, max_dlugosc_hasla + 1):
        haslo = znajdz_haslo(tekst, dlugosc)

        if haslo == "":
            continue

        wynik = vigenere(tekst, haslo, "d")
        score = score_calego_tekstu(wynik)

        if score > najlepszy_score:
            najlepszy_score = score
            najlepsze_haslo = haslo
            najlepszy_wynik = wynik

    return najlepsze_haslo, najlepszy_wynik


def analiza_czestosci_znakow(tekst):
    tekst = tekst.upper()
    licznik = {}

    for znak in ALFABET:
        licznik[znak] = 0

    suma = 0

    for znak in tekst:
        if znak in ALFABET:
            licznik[znak] += 1
            suma += 1

    ranking = []

    for znak in ALFABET:
        if suma > 0:
            procent = (licznik[znak] / suma) * 100
        else:
            procent = 0.0

        ranking.append((znak, licznik[znak], procent))

    ranking.sort(key=lambda x: (-x[1], x[0]))

    return ranking, suma


def podziel_na_slowa(tekst):
    tekst = tekst.upper()
    slowa = []
    aktualne = ""

    for znak in tekst:
        if znak in ALFABET:
            aktualne += znak
        else:
            if aktualne != "":
                slowa.append(aktualne)
                aktualne = ""

    if aktualne != "":
        slowa.append(aktualne)

    return slowa


def analiza_slow(tekst):
    slowa = podziel_na_slowa(tekst)
    licznik = {}

    for slowo in slowa:
        if slowo in licznik:
            licznik[slowo] += 1
        else:
            licznik[slowo] = 1

    ranking_najczestsze = sorted(licznik.items(), key=lambda x: (-x[1], x[0]))
    ranking_najrzadsze = sorted(licznik.items(), key=lambda x: (x[1], x[0]))

    return ranking_najczestsze, ranking_najrzadsze, len(slowa), len(licznik)


def wypisz_analize(tekst, tytul):
    ranking_znakow, suma_znakow = analiza_czestosci_znakow(tekst)
    ranking_najczestsze_slowa, ranking_najrzadsze_slowa, liczba_slow, liczba_roznych_slow = analiza_slow(tekst)

    print()
    print("===", tytul, "===")
    print("Liczba liter/cyfr z alfabetu:", suma_znakow)
    print("Liczba słów:", liczba_slow)
    print("Liczba różnych słów:", liczba_roznych_slow)
    print()

    print("3 najczęstsze litery/cyfry:")
    for znak, liczba, procent in ranking_znakow[:3]:
        print(f"{znak} -> {liczba} ({procent:.2f}%)")

    print()
    print("3 najrzadsze litery/cyfry:")
    najrzadsze_znaki = sorted(ranking_znakow, key=lambda x: (x[1], x[0]))[:3]
    for znak, liczba, procent in najrzadsze_znaki:
        print(f"{znak} -> {liczba} ({procent:.2f}%)")

    print()
    print("3 najczęstsze słowa:")
    if len(ranking_najczestsze_slowa) == 0:
        print("Brak słów")
    else:
        for slowo, ile in ranking_najczestsze_slowa[:3]:
            print(f"{slowo} -> {ile}")

    print()
    print("3 najrzadsze słowa:")
    if len(ranking_najrzadsze_slowa) == 0:
        print("Brak słów")
    else:
        for slowo, ile in ranking_najrzadsze_slowa[:3]:
            print(f"{slowo} -> {ile}")


def generuj_haslo_o_dlugosci(dlugosc):
    bazowe = "MASLO"
    wynik = ""

    i = 0
    while len(wynik) < dlugosc:
        wynik += bazowe[i % len(bazowe)]
        i += 1

    return wynik


def porownaj_dlugosci_hasel(tekst, nazwa_bazowa):
    dlugosci = [3, 6, 9, 12, 16]

    print()
    print("=== PORÓWNANIE CZĘSTOTLIWOŚCI DLA RÓŻNYCH DŁUGOŚCI HASEŁ ===")

    for dlugosc in dlugosci:
        haslo = generuj_haslo_o_dlugosci(dlugosc)
        wynik = vigenere(tekst, haslo, "s")

        nazwa_pliku = f"{nazwa_bazowa}_haslo_{dlugosc}.txt"

        with open(nazwa_pliku, "w", encoding="utf-8") as plik:
            plik.write(wynik)

        print()
        print("--------------------------------------------------")
        print(f"Długość hasła: {dlugosc}")
        print(f"Hasło użyte do szyfrowania: {haslo}")
        print(f"Plik zapisany: {nazwa_pliku}")

        wypisz_analize(wynik, f"ANALIZA DLA HASŁA DŁUGOŚCI {dlugosc}")


def main():
    print("=== Szyfr Vigenere'a ===")
    print("Alfabet:", ALFABET)
    print("s - szyfrowanie")
    print("d - deszyfrowanie")
    print("a - automatyczne łamanie bez hasła")
    print("p - porównanie częstotliwości dla długości hasła 3, 6, 9, 12, 16")

    tryb = input("Wybierz tryb (s/d/a/p): ").strip().lower()

    if tryb not in ["s", "d", "a", "p"]:
        print("Błąd: wybierz 's', 'd', 'a' albo 'p'.")
        return

    nazwa_pliku_we = input("Podaj nazwę pliku wejściowego: ").strip()

    try:
        with open(nazwa_pliku_we, "r", encoding="utf-8") as plik:
            tekst = plik.read()
    except FileNotFoundError:
        print("Błąd: nie znaleziono pliku wejściowego.")
        return
    except Exception as e:
        print("Błąd podczas odczytu pliku:", e)
        return

    wypisz_analize(tekst, "ANALIZA PLIKU WEJŚCIOWEGO")

    if tryb in ["s", "d"]:
        nazwa_pliku_wy = input("Podaj nazwę pliku wyjściowego: ").strip()
        haslo = input("Podaj hasło: ").strip()
        wynik = vigenere(tekst, haslo, tryb)

        if wynik == "":
            return

        try:
            with open(nazwa_pliku_wy, "w", encoding="utf-8") as plik:
                plik.write(wynik)
        except Exception as e:
            print("Błąd podczas zapisu pliku:", e)
            return

        print()
        print("Gotowe. Wynik zapisano do pliku:", nazwa_pliku_wy)
        wypisz_analize(wynik, "ANALIZA PLIKU WYNIKOWEGO")

    elif tryb == "a":
        nazwa_pliku_wy = input("Podaj nazwę pliku wyjściowego: ").strip()

        try:
            max_dlugosc = int(input("Podaj maksymalną długość hasła do sprawdzenia: ").strip())
        except ValueError:
            print("Błąd: to musi być liczba całkowita.")
            return

        haslo, wynik = automatyczne_lamanie(tekst, max_dlugosc)

        if haslo == "":
            print("Nie udało się znaleźć hasła.")
            return

        try:
            with open(nazwa_pliku_wy, "w", encoding="utf-8") as plik:
                plik.write(wynik)
        except Exception as e:
            print("Błąd podczas zapisu pliku:", e)
            return

        print()
        print("Prawdopodobne hasło:", haslo)
        print("Gotowe. Odszyfrowany tekst zapisano do pliku:", nazwa_pliku_wy)
        wypisz_analize(wynik, "ANALIZA ODSZYFROWANEGO PLIKU")

    elif tryb == "p":
        nazwa_bazowa = input("Podaj bazową nazwę plików wyjściowych: ").strip()
        porownaj_dlugosci_hasel(tekst, nazwa_bazowa)


main()