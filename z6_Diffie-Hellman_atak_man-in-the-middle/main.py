# mam byc ewa moj kolega po prawo jest alicja a  po lewo bobem
# Diffie-Hellman z wyborem roli: Alicja / Bob / Ewa

def mod_pow(a, b, c):
    wynik = 1
    a %= c
    while b > 0:
        if b % 2 == 1:
            wynik = (wynik * a) % c
        a = (a * a) % c
        b //= 2
    return wynik


def czy_pierwsza(p):
    if p < 2:
        return False
    i = 2
    while i * i <= p:
        if p % i == 0:
            return False
        i += 1
    return True


def alicja():
    print("\n--- ROLA: ALICJA ---")
    g = int(input("Podaj g: "))
    p = int(input("Podaj p: "))
    a = int(input("Podaj tajne a Alicji: "))

    if not czy_pierwsza(p):
        print("Błąd: p nie jest liczbą pierwszą.")
        return

    A = mod_pow(g, a, p)
    print(f"\nTwoja publiczna wartość A = g^a mod p = {A}")
    print("Wyślij tę wartość do Ewy (nie bezpośrednio do Boba).")

    B_otrzymane = int(input("\nPodaj wartość otrzymaną od Ewy (podszywającą się pod Boba): "))
    K_A = mod_pow(B_otrzymane, a, p)

    print(f"Twój obliczony klucz: K_A = {K_A}")


def bob():
    print("\n--- ROLA: BOB ---")
    g = int(input("Podaj g: "))
    p = int(input("Podaj p: "))
    b = int(input("Podaj tajne b Boba: "))

    if not czy_pierwsza(p):
        print("Błąd: p nie jest liczbą pierwszą.")
        return

    B = mod_pow(g, b, p)
    print(f"\nTwoja publiczna wartość B = g^b mod p = {B}")
    print("Wyślij tę wartość do Ewy (nie bezpośrednio do Alicji).")

    A_otrzymane = int(input("\nPodaj wartość otrzymaną od Ewy (podszywającą się pod Alicję): "))
    K_B = mod_pow(A_otrzymane, b, p)

    print(f"Twój obliczony klucz: K_B = {K_B}")


def ewa():
    print("\n--- ROLA: EWA (MAN-IN-THE-MIDDLE) ---")
    g = int(input("Podaj g: "))
    p = int(input("Podaj p: "))
    ae = int(input("Podaj tajne ae Ewy do Boba: "))
    be = int(input("Podaj tajne be Ewy do Alicji: "))

    if not czy_pierwsza(p):
        print("Błąd: p nie jest liczbą pierwszą.")
        return

    print("\nEwa tworzy dwie własne publiczne wartości:")
    A_e = mod_pow(g, ae, p)  # do Boba
    B_e = mod_pow(g, be, p)  # do Alicji

    print(f"A_e = g^ae mod p = {A_e}   -> to wysyłasz Bobowi zamiast prawdziwego A")
    print(f"B_e = g^be mod p = {B_e}   -> to wysyłasz Alicji zamiast prawdziwego B")

    A_prawdziwe = int(input("\nPodaj prawdziwe A przechwycone od Alicji: "))
    B_prawdziwe = int(input("Podaj prawdziwe B przechwycone od Boba: "))

    K_EA = mod_pow(A_prawdziwe, be, p)
    K_EB = mod_pow(B_prawdziwe, ae, p)

    print(f"\nKlucz Ewy z Alicją: K_EA = {K_EA}")
    print(f"Klucz Ewy z Bobem:   K_EB = {K_EB}")


def main():
    print("=== Diffie-Hellman / MITM z wyborem roli ===")
    print("Dostępne role:")
    print("  A - Alicja")
    print("  B - Bob")
    print("  E - Ewa")

    rola = input("\nWybierz rolę [A/B/E]: ").strip().lower()

    if rola in ["a", "alicja"]:
        alicja()
    elif rola in ["b", "bob"]:
        bob()
    elif rola in ["e", "ewa"]:
        ewa()
    else:
        print("Nieznana rola.")


if __name__ == "__main__":
    main()