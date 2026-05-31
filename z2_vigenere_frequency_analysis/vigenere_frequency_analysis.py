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
    if len(fragment) == 0:
        return -10**9

    licznik = {}

    for znak in ALFABET:
        licznik[znak] = 0

    for znak in fragment:
        licznik[znak] += 1

    rozne = 0
    max_count = 0

    for znak in ALFABET:
        if licznik[znak] > 0:
            rozne += 1
        if licznik[znak] > max_count:
            max_count = licznik[znak]

    score = 0
    score += rozne

    if max_count / len(fragment) > 0.5:
        score -= 20

    return score


def znajdz_najlepsze_przesuniecie_dla_fragmentu(fragment):
    najlepsze_przesuniecie = 0
    najlepszy_score = -10**9

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
    tekst = tekst.upper()

    liczba_alfabet = 0
    liczba_innych = 0
    licznik = {}

    for znak in ALFABET:
        licznik[znak] = 0

    for znak in tekst:
        if znak in ALFABET:
            liczba_alfabet += 1
            licznik[znak] += 1
        elif znak in " \n\t.,;:!?-()\"'":
            pass
        else:
            liczba_innych += 1

    if liczba_alfabet == 0:
        return -10**9

    score = 0
    score += liczba_alfabet
    score -= liczba_innych * 2

    rozne = 0
    max_count = 0

    for znak in ALFABET:
        if licznik[znak] > 0:
            rozne += 1
        if licznik[znak] > max_count:
            max_count = licznik[znak]

    score += rozne * 2

    if max_count / liczba_alfabet > 0.35:
        score -= 30

    return score


def automatyczne_lamanie(tekst, max_dlugosc_hasla):
    najlepsze_haslo = ""
    najlepszy_wynik = ""
    najlepszy_score = -10**9

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


def pobierz_podsumowanie_analizy(tekst):
    ranking_znakow, _ = analiza_czestosci_znakow(tekst)
    ranking_najczestsze_slowa, ranking_najrzadsze_slowa, _, _ = analiza_slow(tekst)

    najczestsze_znaki = ranking_znakow[:3]
    najrzadsze_znaki = sorted(ranking_znakow, key=lambda x: (x[1], x[0]))[:3]

    najczestsze_slowa = ranking_najczestsze_slowa[:3]
    najrzadsze_slowa = ranking_najrzadsze_slowa[:3]

    return najczestsze_znaki, najrzadsze_znaki, najczestsze_slowa, najrzadsze_slowa


def wypisz_liste_znakow(lista):
    if len(lista) == 0:
        print("Brak")
    else:
        for znak, liczba, procent in lista:
            print(f"{znak} -> {liczba} ({procent:.2f}%)")


def wypisz_liste_slow(lista):
    if len(lista) == 0:
        print("Brak")
    else:
        for slowo, liczba in lista:
            print(f"{slowo} -> {liczba}")


def wypisz_porownanie_analiz(tekst1, tytul1, tekst2, tytul2):
    najcz_zn_1, najrz_zn_1, najcz_sl_1, najrz_sl_1 = pobierz_podsumowanie_analizy(tekst1)
    najcz_zn_2, najrz_zn_2, najcz_sl_2, najrz_sl_2 = pobierz_podsumowanie_analizy(tekst2)

    print()
    print("==================================================")
    print("PORÓWNANIE ANALIZ")
    print("==================================================")

    print()
    print(f"--- {tytul1} ---")
    print("Najczęstsze litery/cyfry:")
    wypisz_liste_znakow(najcz_zn_1)
    print("Najrzadsze litery/cyfry:")
    wypisz_liste_znakow(najrz_zn_1)
    print("Najczęstsze słowa:")
    wypisz_liste_slow(najcz_sl_1)
    print("Najrzadsze słowa:")
    wypisz_liste_slow(najrz_sl_1)

    print()
    print(f"--- {tytul2} ---")
    print("Najczęstsze litery/cyfry:")
    wypisz_liste_znakow(najcz_zn_2)
    print("Najrzadsze litery/cyfry:")
    wypisz_liste_znakow(najrz_zn_2)
    print("Najczęstsze słowa:")
    wypisz_liste_slow(najcz_sl_2)
    print("Najrzadsze słowa:")
    wypisz_liste_slow(najrz_sl_2)


def generuj_haslo_o_dlugosci_ze_wzorca(wzorzec, dlugosc):
    wzorzec_po_przygotowaniu = przygotuj_haslo(wzorzec)

    if len(wzorzec_po_przygotowaniu) == 0:
        return ""

    wynik = ""
    i = 0

    while len(wynik) < dlugosc:
        wynik += wzorzec_po_przygotowaniu[i % len(wzorzec_po_przygotowaniu)]
        i += 1

    return wynik


def pobierz_hasla_od_uzytkownika():
    dlugosci = [3, 6, 9, 12, 16]
    hasla = {}

    print()
    print("Podaj własne hasła dla długości 3, 6, 9, 12, 16.")
    print("Jeśli wpiszesz dłuższe, program je skróci.")
    print("Jeśli wpiszesz krótsze po oczyszczeniu, poprosi ponownie.")
    print()

    for dlugosc in dlugosci:
        while True:
            haslo = input(f"Podaj hasło długości {dlugosc}: ").strip()
            haslo = przygotuj_haslo(haslo)

            if len(haslo) < dlugosc:
                print("Hasło po oczyszczeniu jest za krótkie. Podaj dłuższe.")
            else:
                hasla[dlugosc] = haslo[:dlugosc]
                break

    return hasla


def wygeneruj_hasla_ze_wzorca(wzorzec):
    dlugosci = [3, 6, 9, 12, 16]
    hasla = {}

    for dlugosc in dlugosci:
        hasla[dlugosc] = generuj_haslo_o_dlugosci_ze_wzorca(wzorzec, dlugosc)

    return hasla


def porownaj_dlugosci_hasel(tekst, nazwa_bazowa):
    print()
    print("=== PORÓWNANIE CZĘSTOTLIWOŚCI DLA DŁUGOŚCI HASEŁ 3, 6, 9, 12, 16 ===")
    print("1 - użytkownik podaje własne hasła")
    print("2 - hasła generowane ze wzorca 'zaq1@WSX'")

    wybor = input("Wybierz opcję (1/2): ").strip()

    if wybor == "1":
        hasla = pobierz_hasla_od_uzytkownika()
        print()
        print("Użyte będą hasła podane przez użytkownika.")

    elif wybor == "2":
        wzorzec = "zaq1@WSX"
        wzorzec_po_przygotowaniu = przygotuj_haslo(wzorzec)

        print()
        print("Wzorzec oryginalny:", wzorzec)
        print("Wzorzec po przygotowaniu do alfabetu:", wzorzec_po_przygotowaniu)

        if len(wzorzec_po_przygotowaniu) == 0:
            print("Błąd: wzorzec po przygotowaniu jest pusty.")
            return

        hasla = wygeneruj_hasla_ze_wzorca(wzorzec)

    else:
        print("Błędna opcja.")
        return

    for dlugosc in [3, 6, 9, 12, 16]:
        haslo = hasla[dlugosc]
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
        wypisz_porownanie_analiz(tekst, "PRZED SZYFROWANIEM", wynik, "PO SZYFROWANIU")


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

        if tryb == "s":
            wypisz_porownanie_analiz(tekst, "PRZED SZYFROWANIEM", wynik, "PO SZYFROWANIU")
        else:
            wypisz_porownanie_analiz(tekst, "PRZED ODSZYFROWANIEM", wynik, "PO ODSZYFROWANIU")

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
        wypisz_porownanie_analiz(tekst, "PRZED ODSZYFROWANIEM", wynik, "PO ODSZYFROWANIU")

    elif tryb == "p":
        nazwa_bazowa = input("Podaj bazową nazwę plików wyjściowych: ").strip()
        porownaj_dlugosci_hasel(tekst, nazwa_bazowa)


main()