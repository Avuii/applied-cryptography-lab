import os

ALFABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def oczysc_tekst(tekst: str) -> str:

    wynik = ""
    for znak in tekst.upper():
        if znak in ALFABET:
            wynik += znak
    return wynik


def wczytaj_plik(sciezka: str) -> str:
    with open(sciezka, "r", encoding="utf-8") as plik:
        return plik.read()


def pobierz_sciezke_pliku(komunikat: str, domyslna: str) -> str:
    sciezka = input(f"{komunikat} [{domyslna}]: ").strip()
    return sciezka if sciezka else domyslna


def znajdz_powtorzenia_kasiski(szyfrogram: str, l_min: int, max_extra_len: int = 3) -> list[dict]:
    """
    Szuka powtarzających się fragmentów o długości L >= l_min.
    Sprawdzamy długości:
        L = l_min, l_min+1, ..., l_min+max_extra_len

    Zwraca listę słowników:
    {
        "fragment": ...,
        "dlugosc": ...,
        "pozycje": [...],
        "odleglosci": [...]
    }
    """
    tekst = oczysc_tekst(szyfrogram)
    wyniki = []

    if l_min < 2:
        raise ValueError("L_min powinno być >= 2.")

    max_len = min(l_min + max_extra_len, len(tekst))
    widziane = set()

    for L in range(l_min, max_len + 1):
        fragmenty = {}

        for i in range(len(tekst) - L + 1):
            fragment = tekst[i:i + L]
            if fragment not in fragmenty:
                fragmenty[fragment] = []
            fragmenty[fragment].append(i)

        for fragment, pozycje in fragmenty.items():
            if len(pozycje) >= 2:
                klucz_widzenia = (fragment, tuple(pozycje))
                if klucz_widzenia in widziane:
                    continue

                odleglosci = []
                for i in range(len(pozycje)):
                    for j in range(i + 1, len(pozycje)):
                        D = abs(pozycje[j] - pozycje[i])
                        odleglosci.append(D)

                wyniki.append({
                    "fragment": fragment,
                    "dlugosc": L,
                    "pozycje": pozycje,
                    "odleglosci": odleglosci
                })
                widziane.add(klucz_widzenia)

    return wyniki


def analiza_kasiski(szyfrogram: str, l_min: int, min_h: int = 2, max_h: int = 20) -> tuple[list[dict], list[int], list[dict]]:
    """
    Metoda Kasiskiego:
    1) szuka powtarzających się fragmentów
    2) zbiera wszystkie odległości D
    3) dla H=2..20 liczy ile razy D mod H == 0

    Zwraca:
    - powtorzenia
    - wszystkie_odleglosci
    - wyniki_h
    """
    powtorzenia = znajdz_powtorzenia_kasiski(szyfrogram, l_min)

    wszystkie_odleglosci = []
    for elem in powtorzenia:
        wszystkie_odleglosci.extend(elem["odleglosci"])

    wyniki_h = []
    for H in range(min_h, max_h + 1):
        trafienia = 0
        pasujace_d = []

        for D in wszystkie_odleglosci:
            if D % H == 0:
                trafienia += 1
                pasujace_d.append(D)

        wyniki_h.append({
            "H": H,
            "trafienia": trafienia,
            "pasujace_odleglosci": pasujace_d
        })

    return powtorzenia, wszystkie_odleglosci, wyniki_h


def wypisz_powtorzenia(powtorzenia: list[dict], limit: int = 15) -> None:
    print("\nZNALEZIONE POWTARZAJĄCE SIĘ FRAGMENTY")
    print("-" * 80)

    if not powtorzenia:
        print("Nie znaleziono powtórzeń.")
        return

    for i, elem in enumerate(powtorzenia[:limit], start=1):
        print(f"{i}. Fragment   : {elem['fragment']}")
        print(f"   Długość    : {elem['dlugosc']}")
        print(f"   Pozycje    : {elem['pozycje']}")
        print(f"   Odległości : {elem['odleglosci']}")
        print()

    if len(powtorzenia) > limit:
        print(f"... pominięto pozostałe {len(powtorzenia) - limit} powtórzenia.")


def wypisz_wyniki_h(wyniki_h: list[dict]) -> None:
    print("\nWYNIKI DLA H = 2..20")
    print("-" * 80)

    for wynik in wyniki_h:
        print(f"H = {wynik['H']:2d}  -> liczba trafień: {wynik['trafienia']}")

    najlepszy = max(wyniki_h, key=lambda x: x["trafienia"])
    print("-" * 80)
    print(f"Najlepszy kandydat wg metody Kasiskiego: H = {najlepszy['H']}")
    print(f"Liczba trafień: {najlepszy['trafienia']}")


def zapisz_raport_kasiski(
    nazwa_pliku: str,
    l_min: int,
    powtorzenia: list[dict],
    wszystkie_odleglosci: list[int],
    wyniki_h: list[dict]
) -> None:
    najlepszy = max(wyniki_h, key=lambda x: x["trafienia"])

    with open(nazwa_pliku, "w", encoding="utf-8") as plik:
        plik.write("METODA KASISKIEGO - ANALIZA DŁUGOŚCI HASŁA W SZYFRZE VIGENERE'A\n")
        plik.write("=" * 80 + "\n\n")
        plik.write(f"L_min = {l_min}\n")
        plik.write(f"Liczba znalezionych powtórzeń: {len(powtorzenia)}\n")
        plik.write(f"Liczba wszystkich odległości D: {len(wszystkie_odleglosci)}\n\n")

        plik.write("POWTARZAJĄCE SIĘ FRAGMENTY\n")
        plik.write("-" * 80 + "\n")
        if not powtorzenia:
            plik.write("Nie znaleziono powtórzeń.\n\n")
        else:
            for elem in powtorzenia:
                plik.write(f"Fragment   : {elem['fragment']}\n")
                plik.write(f"Długość    : {elem['dlugosc']}\n")
                plik.write(f"Pozycje    : {elem['pozycje']}\n")
                plik.write(f"Odległości : {elem['odleglosci']}\n")
                plik.write("\n")

        plik.write("\nWYNIKI DLA H = 2..20\n")
        plik.write("-" * 80 + "\n")
        for wynik in wyniki_h:
            plik.write(f"H = {wynik['H']:2d}  -> liczba trafień: {wynik['trafienia']}\n")

        plik.write("\n")
        plik.write(f"Najlepszy kandydat wg metody Kasiskiego: H = {najlepszy['H']}\n")
        plik.write(f"Liczba trafień: {najlepszy['trafienia']}\n")


def zapisz_wyniki_h_do_folderu(folder_wyjsciowy: str, wyniki_h: list[dict]) -> None:
    """
    Tworzy folder z plikami:
    H_2.txt, H_3.txt, ..., H_20.txt
    """
    os.makedirs(folder_wyjsciowy, exist_ok=True)

    for wynik in wyniki_h:
        H = wynik["H"]
        sciezka = os.path.join(folder_wyjsciowy, f"H_{H}.txt")

        with open(sciezka, "w", encoding="utf-8") as plik:
            plik.write(f"Wyniki dla H = {H}\n")
            plik.write("=" * 80 + "\n\n")
            plik.write(f"Liczba trafień: {wynik['trafienia']}\n")
            plik.write("Odległości spełniające warunek D mod H = 0:\n")
            plik.write(f"{wynik['pasujace_odleglosci']}\n")


def main():
    print("=== METODA KASISKIEGO ===")

    plik_szyfrogram = pobierz_sciezke_pliku("Podaj plik z szyfrogramem", "zaszyfrowany.txt")
    plik_raport = pobierz_sciezke_pliku("Podaj nazwę pliku raportu", "raport_kasiski.txt")
    folder_h = pobierz_sciezke_pliku("Podaj nazwę folderu na wyniki H", "wyniki_kasiski_h")

    try:
        l_min = int(input("Podaj minimalną długość fragmentu L_min: ").strip())
        szyfrogram = wczytaj_plik(plik_szyfrogram)

        powtorzenia, wszystkie_odleglosci, wyniki_h = analiza_kasiski(
            szyfrogram=szyfrogram,
            l_min=l_min,
            min_h=2,
            max_h=20
        )

        wypisz_powtorzenia(powtorzenia)
        wypisz_wyniki_h(wyniki_h)

        zapisz_raport_kasiski(
            nazwa_pliku=plik_raport,
            l_min=l_min,
            powtorzenia=powtorzenia,
            wszystkie_odleglosci=wszystkie_odleglosci,
            wyniki_h=wyniki_h
        )
        zapisz_wyniki_h_do_folderu(folder_h, wyniki_h)

        print(f"\nZapisano raport do pliku: {plik_raport}")
        print(f"Zapisano wyniki H = 2..20 do folderu: {folder_h}")

    except FileNotFoundError as e:
        print(f"\nBłąd: nie znaleziono pliku: {e.filename}")
    except ValueError as e:
        print(f"\nBłąd: {e}")


if __name__ == "__main__":
    main()