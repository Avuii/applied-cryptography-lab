# ElGamal
# p > 65536, bo jeden blok wiadomości ma 2 bajty: 0..65535
# c1 jest jedno dla całej wiadomości
# c2 jest listą wartości, po jednej dla każdego bloku m_i

# przykład
# p = 65537
# g = 3
# x = 12345

import secrets
import math

def modexp(a, b, p):
    """
    Szybkie potęgowanie modularne:
    zwraca a^b mod p
    """
    return pow(a, b, p)


def egcd(a, b):
    """
    Rozszerzony algorytm Euklidesa.
    Zwraca: gcd(a,b), x, y takie że ax + by = gcd(a,b)
    """
    if b == 0:
        return a, 1, 0

    gcd, x1, y1 = egcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1

    return gcd, x, y


def inverse_mod(a, p):
    """
    Odwrotność modulo p.
    Szuka liczby a^(-1) takiej, że:
    a * a^(-1) ≡ 1 mod p
    """
    gcd, x, _ = egcd(a, p)

    if gcd != 1:
        raise ValueError("Odwrotność modulo nie istnieje")

    return x % p


def is_prime(n):
    """
    Prosty test pierwszości wystarczający do małych przykładów.
    Dla p < 2^32 działa szybko.
    """
    if n < 2:
        return False

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    limit = int(math.sqrt(n)) + 1

    for i in range(3, limit, 2):
        if n % i == 0:
            return False

    return True


def text_to_blocks(text):
    """
    Zamiana tekstu na bloki 2-bajtowe.

    Przykład:
    'AB' -> bajty [65, 66] -> blok 65 * 256 + 66 = 16706

    Jeżeli liczba bajtów jest nieparzysta, dokładamy 0 na końcu.
    Zwracamy też oryginalną długość bajtów, żeby poprawnie odtworzyć tekst.
    """
    data = text.encode("utf-8")
    original_length = len(data)

    if len(data) % 2 != 0:
        data += b"\x00"

    blocks = []

    for i in range(0, len(data), 2):
        block = data[i] * 256 + data[i + 1]
        blocks.append(block)

    return blocks, original_length


def blocks_to_text(blocks, original_length=None):
    """
    Zamiana bloków 2-bajtowych z powrotem na tekst.
    """
    data = bytearray()

    for block in blocks:
        if block < 0 or block > 65535:
            raise ValueError("Niepoprawny blok wiadomości")

        first_byte = block // 256
        second_byte = block % 256

        data.append(first_byte)
        data.append(second_byte)

    if original_length is not None:
        data = data[:original_length]

    return data.decode("utf-8", errors="replace")


def parse_numbers(line):
    """
    Zamiana linii tekstu na listę liczb.
    Przykład:
    '123 456 789' -> [123, 456, 789]
    """
    return [int(x) for x in line.replace(",", " ").split()]


def read_p():
    """
    Wczytanie p z kontrolą warunku z zajęć.
    """
    p = int(input("Podaj p, liczbę pierwszą większą od 65536 i mniejszą niż 2^32: "))

    if p <= 65536:
        print("UWAGA: p powinno być większe od 65536, żeby blok 2-bajtowy był mniejszy od p.")

    if p >= 2**32:
        print("UWAGA: p miało być mniejsze niż 2^32.")

    if not is_prime(p):
        print("UWAGA: podane p nie wygląda na liczbę pierwszą.")

    return p


def encrypt():
    print("\n--- SZYFROWANIE ELGAMAL ---")

    p = read_p()

    g = int(input("Podaj g: "))
    x = int(input("Podaj klucz prywatny x: "))

    if not (1 < g < p):
        print("UWAGA: g powinno spełniać 1 < g < p.")

    if not (1 <= x <= p - 2):
        print("UWAGA: x zwykle wybiera się z zakresu 1..p-2.")

    # Klucz publiczny
    h = modexp(g, x, p)

    print("\nKlucz publiczny:")
    print(f"p = {p}")
    print(f"g = {g}")
    print(f"h = g^x mod p = {h}")

    text = input("\nPodaj tekst do zaszyfrowania: ")

    blocks, original_length = text_to_blocks(text)

    print("\nBloki wiadomości m_i:")
    print(blocks)

    # Jeden losowy y dla całej wiadomości
    y = secrets.randbelow(p - 2) + 1

    # c1 jedno dla całej wiadomości
    c1 = modexp(g, y, p)

    # wspólny sekret s
    s = modexp(h, y, p)

    c2 = []

    for m in blocks:
        c2_i = (m * s) % p
        c2.append(c2_i)

    print("\n--- SZYFROGRAM ---")
    print(f"c1 = {c1}")
    print("c2 =", " ".join(str(value) for value in c2))

    print("\nDodatkowo do poprawnego odtworzenia tekstu zapisz długość bajtów:")
    print(f"dlugosc = {original_length}")

    print("\nWartości pomocnicze pokazane tylko edukacyjnie:")
    print(f"y = {y}")
    print(f"s = h^y mod p = {s}")


def decrypt_with_private_key():
    print("\n--- ODSZYFROWYWANIE KLUCZEM PRYWATNYM ---")

    p = read_p()
    x = int(input("Podaj klucz prywatny x: "))

    c1 = int(input("Podaj c1: "))

    line = input("Podaj c2 w jednej linii: ")
    c2 = parse_numbers(line)

    length_line = input("Podaj długość bajtów wiadomości, jeśli znasz, albo zostaw puste: ")

    if length_line.strip() == "":
        original_length = None
    else:
        original_length = int(length_line)

    # s = c1^x mod p
    s = modexp(c1, x, p)

    # s_inv = s^(-1) mod p
    s_inv = inverse_mod(s, p)

    blocks = []

    for c2_i in c2:
        m_i = (c2_i * s_inv) % p
        blocks.append(m_i)

    text = blocks_to_text(blocks, original_length)

    print("\nOdszyfrowane bloki m_i:")
    print(blocks)

    print("\nOdszyfrowany tekst:")
    print(text)


def decrypt_known_plaintext_attack():
    print("\n--- ATAK: ODSZYFROWANIE ZNAJĄC JEDEN BLOK m_i ---")
    print("Ten atak działa dlatego, że użyto jednego wspólnego s dla wszystkich bloków.")
    print("Jeżeli znamy jedno m_i i odpowiadające mu c2_i, możemy policzyć s.")

    p = read_p()

    line = input("Podaj c2 w jednej linii: ")
    c2 = parse_numbers(line)

    index = int(input("Podaj numer znanego bloku, licząc od 1: "))
    known_m = int(input("Podaj znany blok m_i jako liczbę: "))

    if index < 1 or index > len(c2):
        print("Niepoprawny numer bloku.")
        return

    known_c2 = c2[index - 1]

    if known_m == 0:
        print("Nie da się użyć bloku m_i = 0, bo nie ma odwrotności modulo.")
        return

    # c2_i = m_i * s mod p
    # s = c2_i * m_i^(-1) mod p
    known_m_inv = inverse_mod(known_m, p)
    s = (known_c2 * known_m_inv) % p

    s_inv = inverse_mod(s, p)

    blocks = []

    for c2_i in c2:
        m_i = (c2_i * s_inv) % p
        blocks.append(m_i)

    length_line = input("Podaj długość bajtów wiadomości, jeśli znasz, albo zostaw puste: ")

    if length_line.strip() == "":
        original_length = None
    else:
        original_length = int(length_line)

    text = blocks_to_text(blocks, original_length)

    print("\nOdzyskany wspólny sekret:")
    print(f"s = {s}")

    print("\nOdszyfrowane bloki m_i:")
    print(blocks)

    print("\nOdszyfrowany tekst:")
    print(text)


def main():
    while True:
        print("\n==============================")
        print(" ELGAMAL")
        print("==============================")
        print("1 - szyfrowanie")
        print("2 - odszyfrowywanie kluczem prywatnym")
        print("3 - atak: odszyfrowanie znając jeden blok m_i")
        print("0 - koniec")

        choice = input("Wybór: ")

        if choice == "1":
            encrypt()
        elif choice == "2":
            decrypt_with_private_key()
        elif choice == "3":
            decrypt_known_plaintext_attack()
        elif choice == "0":
            break
        else:
            print("Niepoprawny wybór.")


if __name__ == "__main__":
    main()