# Rozszerzony algorytm euklidesa

def extended_euclid_table(a: int, b: int):
    if a == 0 and b == 0:
        raise ValueError("Przynajmniej jedna liczba musi być różna od zera.")

    rows = [
        {"i": 1, "q": None, "r": a, "s": 1, "t": 0},
        {"i": 2, "q": None, "r": b, "s": 0, "t": 1},
    ]

    i = 3
    while rows[-1]["r"] != 0:
        prev2 = rows[-2]
        prev1 = rows[-1]

        q = prev2["r"] // prev1["r"]
        r = prev2["r"] - q * prev1["r"]
        s = prev2["s"] - q * prev1["s"]
        t = prev2["t"] - q * prev1["t"]

        rows.append({"i": i, "q": q, "r": r, "s": s, "t": t})
        i += 1

    return rows


def last_nonzero_row(rows):
    for row in reversed(rows):
        if row["r"] != 0:
            return row
    return None


def modular_inverse(a: int, m: int):

    rows = extended_euclid_table(m, a)
    final_row = last_nonzero_row(rows)
    gcd_value = abs(final_row["r"])

    if gcd_value != 1:
        return None, rows, gcd_value


    inverse = final_row["t"] % m
    return inverse, rows, gcd_value


def solve_congruence(a: int, b: int, m: int):
    inverse, rows, gcd_value = modular_inverse(a, m)
    if inverse is None:
        return None, None, rows, gcd_value

    x = (inverse * b) % m
    return x, inverse, rows, gcd_value


def print_table(rows):
    headers = ["i", "qi", "ri", "si", "ti"]
    data = []

    for row in rows:
        data.append([
            str(row["i"]),
            "-" if row["q"] is None else str(row["q"]),
            str(row["r"]),
            str(row["s"]),
            str(row["t"]),
        ])

    widths = [len(h) for h in headers]
    for line in data:
        for idx, cell in enumerate(line):
            widths[idx] = max(widths[idx], len(cell))

    def fmt(row):
        return " | ".join(cell.rjust(widths[idx]) for idx, cell in enumerate(row))

    sep = "-+-".join("-" * w for w in widths)

    print(fmt(headers))
    print(sep)
    for line in data:
        print(fmt(line))


def show_gcd_mode():
    print("\n=== TRYB 1: Tabela dla NWD(a, b) ===")
    a = int(input("Podaj a: "))
    b = int(input("Podaj b: "))

    rows = extended_euclid_table(a, b)
    final_row = last_nonzero_row(rows)
    gcd_value = abs(final_row["r"])

    print("\nTabela rozszerzonego algorytmu Euklidesa:\n")
    print_table(rows)

    print("\nWynik:")
    print(f"NWD({a}, {b}) = {gcd_value}")
    print(f"{a} * ({final_row['s']}) + {b} * ({final_row['t']}) = {final_row['r']}")


def show_inverse_mode():
    print("\n=== TRYB 2: Odwrotność modulo ===")
    a = int(input("Podaj a: "))
    m = int(input("Podaj modulo m: "))

    inverse, rows, gcd_value = modular_inverse(a, m)

    print("\nTabela rozszerzonego algorytmu Euklidesa:\n")
    print_table(rows)

    print("\nWynik:")
    if inverse is None:
        print(f"gcd({a}, {m}) = {gcd_value}")
        print("Odwrotność modulo nie istnieje, bo NWD != 1.")
    else:
        final_row = last_nonzero_row(rows)
        print(f"gcd({a}, {m}) = 1")
        print(f"{m} * ({final_row['s']}) + {a} * ({final_row['t']}) = 1")
        print(f"{a}^(-1) mod {m} = {inverse}")
        print(f"Sprawdzenie: ({a} * {inverse}) mod {m} = {(a * inverse) % m}")


def show_congruence_mode():
    print("\n=== TRYB 3: Równanie modularne ===")
    print("Rozwiązujemy: a*x ≡ b (mod m)\n")

    a = int(input("Podaj a: "))
    b = int(input("Podaj b: "))
    m = int(input("Podaj modulo m: "))

    x, inverse, rows, gcd_value = solve_congruence(a, b, m)

    print("\nTabela rozszerzonego algorytmu Euklidesa:\n")
    print_table(rows)

    print("\nWynik:")
    if x is None:
        print(f"gcd({a}, {m}) = {gcd_value}")
        print("Nie można użyć odwrotności modulo, bo NWD != 1.")
    else:
        print(f"{a}^(-1) mod {m} = {inverse}")
        print(f"x ≡ {inverse} * {b} (mod {m})")
        print(f"x ≡ {inverse * b} (mod {m})")
        print(f"x ≡ {x} (mod {m})")
        print(f"Sprawdzenie: ({a} * {x}) mod {m} = {(a * x) % m}")


def main():
    while True:
        print("\n" + "=" * 55)
        print("Rozszerzony algorytm Euklidesa / odwrotność modulo")
        print("=" * 55)
        print("1. Pokaż tabelę dla NWD(a, b)")
        print("2. Policz odwrotność a^(-1) mod m")
        print("3. Rozwiąż równanie a*x ≡ b (mod m)")
        print("0. Zakończ")

        choice = input("\nWybierz opcję: ").strip()

        try:
            if choice == "1":
                show_gcd_mode()
            elif choice == "2":
                show_inverse_mode()
            elif choice == "3":
                show_congruence_mode()
            elif choice == "0":
                print("Koniec programu.")
                break
            else:
                print("Nieprawidłowa opcja. Wybierz 0, 1, 2 albo 3.")
        except ValueError as e:
            print(f"Błąd danych: {e}")
        except ZeroDivisionError:
            print("Błąd: nie można dzielić przez zero.")
        except Exception as e:
            print(f"Wystąpił błąd: {e}")


if __name__ == "__main__":
    main()
