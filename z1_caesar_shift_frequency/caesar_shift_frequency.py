from pathlib import Path

ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789"

def wczytaj_tekst(sciezka: str) -> str:
    try:
        return Path(sciezka).read_text(encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"Nie znaleziono pliku: {sciezka}")


def zapisz_tekst(sciezka: str, tekst: str) -> None:
    Path(sciezka).write_text(tekst, encoding="utf-8")


def przesun_znak(znak: str, przesuniecie: int) -> str:
    z = znak.lower()

    if z in ALPHABET:
        indeks = ALPHABET.index(z)
        nowy_indeks = (indeks + przesuniecie) % len(ALPHABET)
        return ALPHABET[nowy_indeks]

    return znak


def przeksztalc_tekst(tekst: str, przesuniecie: int, tryb: str) -> str:
    if tryb == "d":
        przesuniecie = -przesuniecie

    wynik = ""
    for znak in tekst:
        wynik += przesun_znak(znak, przesuniecie)

    return wynik


def policz_czestosci(tekst: str) -> tuple[dict[str, int], dict[str, float], int]:
    liczniki = {znak: 0 for znak in ALPHABET}
    suma = 0

    for znak in tekst:
        z = znak.lower()
        if z in ALPHABET:
            liczniki[z] += 1
            suma += 1

    procenty = {}
    for znak in ALPHABET:
        if suma == 0:
            procenty[znak] = 0.0
        else:
            procenty[znak] = (liczniki[znak] / suma) * 100

    return liczniki, procenty, suma


def raport_analizy(tekst: str) -> str:
    liczniki, procenty, suma = policz_czestosci(tekst)

    linie = []
    linie.append("ANALIZA CZĘSTOŚCI ZNAKÓW")
    linie.append("=" * 40)
    linie.append(f"Suma liter i cyfr (bez spacji, enterów itd.): {suma}")
    linie.append("")

    for znak in ALPHABET:
        linie.append(f"{znak} -> {liczniki[znak]:>5} ({procenty[znak]:>6.2f}%)")

    return "\n".join(linie)


def roznica_procentow(procenty_a: dict[str, float], procenty_b: dict[str, float]) -> float:
    suma = 0.0
    for znak in ALPHABET:
        suma += abs(procenty_a[znak] - procenty_b[znak])
    return suma


def znajdz_przesuniecie(tekst_wzorcowy: str, tekst_zaszyfrowany: str) -> tuple[int, float, list[tuple[int, float]]]:
    _, procenty_wzorcowe, suma_wzorcowa = policz_czestosci(tekst_wzorcowy)

    if suma_wzorcowa == 0:
        raise ValueError("Tekst wzorcowy nie zawiera liter ani cyfr z alfabetu a-z0-9.")

    ranking = []

    for przesuniecie in range(len(ALPHABET)):
        kandydat = przeksztalc_tekst(tekst_zaszyfrowany, przesuniecie, "d")
        _, procenty_kandydata, suma_kandydata = policz_czestosci(kandydat)

        if suma_kandydata == 0:
            wynik = float("inf")
        else:
            wynik = roznica_procentow(procenty_wzorcowe, procenty_kandydata)

        ranking.append((przesuniecie, wynik))

    ranking.sort(key=lambda x: x[1])
    najlepsze_przesuniecie, najlepszy_wynik = ranking[0]
    return najlepsze_przesuniecie, najlepszy_wynik, ranking


def pobierz_sciezke(komunikat: str, domyslna: str) -> str:
    wartosc = input(f"{komunikat} [{domyslna}]: ").strip()
    return wartosc if wartosc else domyslna


def pobierz_przesuniecie() -> int:
    while True:
        try:
            return int(input("Podaj przesunięcie: ").strip())
        except ValueError:
            print("Błąd: wpisz liczbę całkowitą.")


def szyfruj_lub_deszyfruj() -> None:
    while True:
        tryb = input("Wybierz tryb: [s] szyfrowanie, [d] deszyfrowanie: ").strip().lower()
        if tryb in ("s", "d"):
            break
        print("Błąd: wpisz 's' albo 'd'.")

    przesuniecie = pobierz_przesuniecie()
    plik_we = pobierz_sciezke("Plik wejściowy", "input.txt")
    plik_wy = pobierz_sciezke("Plik wyjściowy", "output.txt")

    try:
        tekst = wczytaj_tekst(plik_we)
        wynik = przeksztalc_tekst(tekst, przesuniecie, tryb)
        zapisz_tekst(plik_wy, wynik)
        print(f"Gotowe. Wynik zapisano do pliku: {plik_wy}")
    except Exception as e:
        print(f"Błąd: {e}")


def analiza_pliku() -> None:
    plik_we = pobierz_sciezke("Plik do analizy", "input.txt")
    plik_raport = pobierz_sciezke("Plik raportu", "analiza.txt")

    try:
        tekst = wczytaj_tekst(plik_we)
        raport = raport_analizy(tekst)

        print("\n" + raport + "\n")
        zapisz_tekst(plik_raport, raport)

        print(f"Raport zapisano do pliku: {plik_raport}")
    except Exception as e:
        print(f"Błąd: {e}")


def znajdz_i_odszyfruj() -> None:
    plik_wzorzec = pobierz_sciezke("Plik wzorcowy", "wzorzec.txt")
    plik_szyfr = pobierz_sciezke("Plik zaszyfrowany", "zaszyfrowany.txt")
    plik_wy = pobierz_sciezke("Plik wyjściowy", "odszyfrowany.txt")
    plik_ranking = pobierz_sciezke("Plik z rankingiem przesunięć", "ranking.txt")

    try:
        tekst_wzorcowy = wczytaj_tekst(plik_wzorzec)
        tekst_zaszyfrowany = wczytaj_tekst(plik_szyfr)

        najlepsze_przesuniecie, najlepszy_wynik, ranking = znajdz_przesuniecie(
            tekst_wzorcowy,
            tekst_zaszyfrowany
        )

        odszyfrowany = przeksztalc_tekst(tekst_zaszyfrowany, najlepsze_przesuniecie, "d")
        zapisz_tekst(plik_wy, odszyfrowany)

        linie = []
        linie.append("RANKING PRZESUNIĘĆ")
        linie.append("=" * 30)
        for przesuniecie, wynik in ranking:
            linie.append(f"Przesunięcie {przesuniecie:>2} -> różnica: {wynik:.4f}")

        raport = "\n".join(linie)
        zapisz_tekst(plik_ranking, raport)

        print(f"Najlepsze przesunięcie do odszyfrowania: {najlepsze_przesuniecie}")
        print(f"Wynik dopasowania: {najlepszy_wynik:.4f}")
        print(f"Odszyfrowany tekst zapisano do: {plik_wy}")
        print(f"Ranking zapisano do: {plik_ranking}")

    except Exception as e:
        print(f"Błąd: {e}")


def menu() -> None:
    while True:
        print("\n" + "=" * 50)
        print("PROGRAM: szyfrowanie / deszyfrowanie / analiza")
        print("=" * 50)
        print("1 - Szyfruj / deszyfruj plik")
        print("2 - Analiza częstości znaków")
        print("3 - Znajdź przesunięcie i odszyfruj")
        print("4 - Zakończ")

        wybor = input("Wybierz opcję: ").strip()

        if wybor == "1":
            szyfruj_lub_deszyfruj()
        elif wybor == "2":
            analiza_pliku()
        elif wybor == "3":
            znajdz_i_odszyfruj()
        elif wybor == "4":
            print("Koniec programu.")
            break
        else:
            print("Błąd: wybierz 1, 2, 3 albo 4.")


if __name__ == "__main__":
    menu()