# -*- coding: utf-8 -*-

import os

ALFABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def oczysc_tekst(tekst: str) -> str:
    """
    Zostawia tylko litery A-Z i zamienia na wielkie litery.
    """
    wynik = ""
    for znak in tekst.upper():
        if znak in ALFABET:
            wynik += znak
    return wynik


def przygotuj_klucz(klucz: str) -> str:
    """
    Czyści klucz i zostawia tylko litery A-Z.
    """
    klucz_czysty = oczysc_tekst(klucz)
    if not klucz_czysty:
        raise ValueError("Klucz po oczyszczeniu jest pusty.")
    return klucz_czysty


def szyfruj_vigenere(tekst_jawny: str, klucz: str) -> str:
    """
    Szyfruje tylko litery A-Z.
    Pozostałe znaki (spacje, cyfry, interpunkcja) zostawia bez zmian.
    """
    klucz = przygotuj_klucz(klucz)
    szyfrogram = ""
    j = 0

    for znak in tekst_jawny.upper():
        if znak in ALFABET:
            p = ALFABET.index(znak)
            k = ALFABET.index(klucz[j % len(klucz)])
            c = (p + k) % 26
            szyfrogram += ALFABET[c]
            j += 1
        else:
            szyfrogram += znak

    return szyfrogram


def deszyfruj_vigenere(szyfrogram: str, klucz: str) -> str:
    """
    Deszyfruje tylko litery A-Z.
    Pozostałe znaki (spacje, cyfry, interpunkcja) zostawia bez zmian.
    """
    klucz = przygotuj_klucz(klucz)
    tekst_jawny = ""
    j = 0

    for znak in szyfrogram.upper():
        if znak in ALFABET:
            c = ALFABET.index(znak)
            k = ALFABET.index(klucz[j % len(klucz)])
            p = (c - k + 26) % 26
            tekst_jawny += ALFABET[p]
            j += 1
        else:
            tekst_jawny += znak

    return tekst_jawny


def policz_czestosci(tekst: str) -> dict:
    """
    Zlicza wystąpienia liter A-Z w oczyszczonym tekście.
    """
    tekst = oczysc_tekst(tekst)
    czestosci = {litera: 0 for litera in ALFABET}

    for znak in tekst:
        czestosci[znak] += 1

    return czestosci


def index_of_coincidence(tekst: str) -> float:
    """
    IC = sum(ni * (ni - 1)) / (N * (N - 1))
    ni - liczba wystąpień i-tej litery
    N  - długość tekstu
    """
    tekst = oczysc_tekst(tekst)
    N = len(tekst)

    if N < 2:
        return 0.0

    czestosci = policz_czestosci(tekst)

    licznik = 0
    for ni in czestosci.values():
        licznik += ni * (ni - 1)

    mianownik = N * (N - 1)
    return licznik / mianownik


def podziel_na_grupy(szyfrogram: str, dlugosc_hasla: int) -> list[str]:
    """
    Dzieli oczyszczony szyfrogram na H grup:
    G1 = pozycje 1, 1+H, 1+2H, ...
    G2 = pozycje 2, 2+H, 2+2H, ...
    ...
    """
    tekst = oczysc_tekst(szyfrogram)
    grupy = [""] * dlugosc_hasla

    for i, znak in enumerate(tekst):
        grupy[i % dlugosc_hasla] += znak

    return grupy


def analiza_dlugosci_hasla_ic(
    szyfrogram: str,
    tekst_wzorcowy: str,
    min_h: int = 2,
    max_h: int = 20
) -> tuple[float, list[dict]]:
    """
    METODA 1:
    - liczy IC dla tekstu wzorcowego
    - dla H = min_h..max_h dzieli szyfrogram na H grup
    - liczy IC każdej grupy
    - liczy średnie IC_H
    """
    szyfrogram = oczysc_tekst(szyfrogram)
    tekst_wzorcowy = oczysc_tekst(tekst_wzorcowy)

    ic_wzorcowe = index_of_coincidence(tekst_wzorcowy)
    wyniki = []

    for H in range(min_h, max_h + 1):
        grupy = podziel_na_grupy(szyfrogram, H)
        ic_grup = []

        for grupa in grupy:
            ic = index_of_coincidence(grupa)
            ic_grup.append(ic)

        srednie_ic = sum(ic_grup) / H
        roznica = abs(srednie_ic - ic_wzorcowe)

        wyniki.append({
            "H": H,
            "grupy": grupy,
            "ic_grup": ic_grup,
            "srednie_ic": srednie_ic,
            "roznica_od_wzorcowego": roznica
        })

    return ic_wzorcowe, wyniki


def wczytaj_plik(sciezka: str) -> str:
    with open(sciezka, "r", encoding="utf-8") as plik:
        return plik.read()


def zapisz_plik(sciezka: str, tresc: str) -> None:
    with open(sciezka, "w", encoding="utf-8") as plik:
        plik.write(tresc)


def pobierz_sciezke_pliku(komunikat: str, domyslna: str) -> str:
    sciezka = input(f"{komunikat} [{domyslna}]: ").strip()
    return sciezka if sciezka else domyslna


def wypisz_tabele_wynikow(ic_wzorcowe: float, wyniki: list[dict]) -> None:
    print("\nMETODA 1: Analiza długości hasła w szyfrze Vigenère’a z użyciem IC")
    print("-" * 78)
    print(f"IC dla tekstu wzorcowego: {ic_wzorcowe:.6f}")
    print("-" * 78)

    for wynik in wyniki:
        H = wynik["H"]
        srednie_ic = wynik["srednie_ic"]
        roznica = wynik["roznica_od_wzorcowego"]
        print(f"IC dla H = {H:2d} : {srednie_ic:.6f}   | roznica od wzorcowego = {roznica:.6f}")

    print("-" * 78)

    najlepszy = min(wyniki, key=lambda x: x["roznica_od_wzorcowego"])
    print(f"Najlepszy kandydat na długość hasła: H = {najlepszy['H']}")
    print(f"Średni IC dla tego H: {najlepszy['srednie_ic']:.6f}")
    print(f"Różnica od IC wzorcowego: {najlepszy['roznica_od_wzorcowego']:.6f}")


def wypisz_szczegoly_dla_H(wyniki: list[dict], wybrane_H: int) -> None:
    znaleziony = None
    for wynik in wyniki:
        if wynik["H"] == wybrane_H:
            znaleziony = wynik
            break

    if znaleziony is None:
        print(f"Brak wyników dla H = {wybrane_H}")
        return

    print(f"\nSZCZEGÓŁY DLA H = {wybrane_H}")
    print("-" * 78)

    for i, (grupa, ic) in enumerate(zip(znaleziony["grupy"], znaleziony["ic_grup"]), start=1):
        podglad = grupa[:120]
        if len(grupa) > 120:
            podglad += "..."
        print(f"G{i}: {podglad}")
        print(f"IC_{i}G = {ic:.6f}")
        print()

    print(f"Średni IC_H = {znaleziony['srednie_ic']:.6f}")
    print("-" * 78)


def zapisz_raport_do_pliku(nazwa_pliku: str, ic_wzorcowe: float, wyniki: list[dict]) -> None:
    najlepszy = min(wyniki, key=lambda x: x["roznica_od_wzorcowego"])

    with open(nazwa_pliku, "w", encoding="utf-8") as plik:
        plik.write("METODA 1: Analiza długości hasła w szyfrze Vigenère’a z użyciem IC\n")
        plik.write("=" * 78 + "\n\n")
        plik.write(f"IC dla tekstu wzorcowego: {ic_wzorcowe:.6f}\n\n")

        for wynik in wyniki:
            H = wynik["H"]
            srednie_ic = wynik["srednie_ic"]
            roznica = wynik["roznica_od_wzorcowego"]
            plik.write(
                f"IC dla H = {H:2d} : {srednie_ic:.6f}   | roznica od wzorcowego = {roznica:.6f}\n"
            )

        plik.write("\n")
        plik.write(f"Najlepszy kandydat na długość hasła: H = {najlepszy['H']}\n")
        plik.write(f"Średni IC dla tego H: {najlepszy['srednie_ic']:.6f}\n")
        plik.write(f"Różnica od IC wzorcowego: {najlepszy['roznica_od_wzorcowego']:.6f}\n")


def zapisz_grupy_do_folderu(folder_wyjsciowy: str, wyniki: list[dict]) -> None:
    """
    Zapisuje osobny plik dla każdego H:
    H_2.txt, H_3.txt, ..., H_20.txt
    """
    os.makedirs(folder_wyjsciowy, exist_ok=True)

    for wynik in wyniki:
        H = wynik["H"]
        nazwa_pliku = os.path.join(folder_wyjsciowy, f"H_{H}.txt")

        with open(nazwa_pliku, "w", encoding="utf-8") as plik:
            plik.write(f"Wyniki dla H = {H}\n")
            plik.write("=" * 78 + "\n\n")

            for i, (grupa, ic) in enumerate(zip(wynik["grupy"], wynik["ic_grup"]), start=1):
                plik.write(f"G{i}:\n")
                plik.write(f"{grupa}\n")
                plik.write(f"IC_{i}G = {ic:.6f}\n")
                plik.write("\n")

            plik.write(f"Sredni IC_H = {wynik['srednie_ic']:.6f}\n")
            plik.write(f"Roznica od IC wzorcowego = {wynik['roznica_od_wzorcowego']:.6f}\n")


def main():
    print("=== SZYFR VIGENERE'A + METODA 1 (IC) ===")
    print("\nWybierz opcję:")
    print("1 - szyfrowanie")
    print("2 - deszyfrowanie")
    print("3 - analiza długości hasła metodą IC")
    wybor = input("Twój wybór: ").strip()

    if wybor == "1":
        klucz = input("Podaj klucz: ").strip()
        plik_we = pobierz_sciezke_pliku("Podaj nazwę pliku wejściowego", "biblia.txt")
        plik_wy = pobierz_sciezke_pliku("Podaj nazwę pliku wyjściowego", "zaszyfrowany.txt")

        try:
            tekst = wczytaj_plik(plik_we)
            szyfrogram = szyfruj_vigenere(tekst, klucz)
            zapisz_plik(plik_wy, szyfrogram)

            print("\nSzyfrowanie zakończone.")
            print(f"Plik wejściowy : {plik_we}")
            print(f"Plik wyjściowy : {plik_wy}")
            print(f"Liczba liter A-Z użytych w szyfrowaniu: {len(oczysc_tekst(tekst))}")

        except FileNotFoundError:
            print(f"\nBłąd: nie znaleziono pliku wejściowego: {plik_we}")
        except ValueError as e:
            print(f"\nBłąd: {e}")

    elif wybor == "2":
        klucz = input("Podaj klucz: ").strip()
        plik_we = pobierz_sciezke_pliku("Podaj nazwę pliku wejściowego", "zaszyfrowany.txt")
        plik_wy = pobierz_sciezke_pliku("Podaj nazwę pliku wyjściowego", "odszyfrowany.txt")

        try:
            szyfrogram = wczytaj_plik(plik_we)
            tekst_jawny = deszyfruj_vigenere(szyfrogram, klucz)
            zapisz_plik(plik_wy, tekst_jawny)

            print("\nDeszyfrowanie zakończone.")
            print(f"Plik wejściowy : {plik_we}")
            print(f"Plik wyjściowy : {plik_wy}")
            print(f"Liczba liter A-Z po odszyfrowaniu: {len(oczysc_tekst(tekst_jawny))}")

        except FileNotFoundError:
            print(f"\nBłąd: nie znaleziono pliku wejściowego: {plik_we}")
        except ValueError as e:
            print(f"\nBłąd: {e}")

    elif wybor == "3":
        plik_szyfrogram = pobierz_sciezke_pliku("Podaj plik z szyfrogramem", "zaszyfrowany.txt")
        plik_wzorzec = pobierz_sciezke_pliku("Podaj plik wzorcowy", "biblia.txt")
        plik_raport = pobierz_sciezke_pliku("Podaj nazwę pliku raportu", "raport_ic.txt")
        folder_h = pobierz_sciezke_pliku("Podaj nazwę folderu na grupy H", "wyniki_h")

        try:
            szyfrogram = wczytaj_plik(plik_szyfrogram)
            tekst_wzorcowy = wczytaj_plik(plik_wzorzec)

            ic_wzorcowe, wyniki = analiza_dlugosci_hasla_ic(
                szyfrogram=szyfrogram,
                tekst_wzorcowy=tekst_wzorcowy,
                min_h=2,
                max_h=20
            )

            wypisz_tabele_wynikow(ic_wzorcowe, wyniki)
            zapisz_raport_do_pliku(plik_raport, ic_wzorcowe, wyniki)
            zapisz_grupy_do_folderu(folder_h, wyniki)

            print(f"\nZapisano raport do pliku: {plik_raport}")
            print(f"Zapisano grupy dla H=2..20 do folderu: {folder_h}")

            odp = input("\nCzy chcesz zobaczyć szczegóły dla konkretnego H? (t/n): ").strip().lower()
            if odp == "t":
                try:
                    wybrane_H = int(input("Podaj H: ").strip())
                    wypisz_szczegoly_dla_H(wyniki, wybrane_H)
                except ValueError:
                    print("Nie podano poprawnej liczby H.")

        except FileNotFoundError as e:
            print(f"\nBłąd: nie znaleziono pliku: {e.filename}")

    else:
        print("Niepoprawny wybór.")


if __name__ == "__main__":
    main()