from pathlib import Path

ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789"

def read_text(file_path: str) -> str:
    try:
        return Path(file_path).read_text(encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")


def write_text(file_path: str, text: str) -> None:
    Path(file_path).write_text(text, encoding="utf-8")


def shift_character(char: str, shift: int) -> str:

    lower_char = char.lower()

    if lower_char in ALPHABET:
        index = ALPHABET.index(lower_char)
        new_index = (index + shift) % len(ALPHABET)
        return ALPHABET[new_index]

    return char


def transform_text(text: str, shift: int, mode: str) -> str:

    if mode == "d":
        shift = -shift

    result = ""
    for char in text:
        result += shift_character(char, shift)

    return result


def count_frequencies(text: str) -> tuple[dict[str, int], dict[str, float], int]:
    counts = {char: 0 for char in ALPHABET}
    total = 0

    for char in text:
        lower_char = char.lower()
        if lower_char in ALPHABET:
            counts[lower_char] += 1
            total += 1

    percentages = {}
    for char in ALPHABET:
        if total == 0:
            percentages[char] = 0.0
        else:
            percentages[char] = (counts[char] / total) * 100

    return counts, percentages, total


def build_frequency_report(text: str) -> str:
    counts, percentages, total = count_frequencies(text)

    lines = []
    lines.append("CHARACTER FREQUENCY ANALYSIS")
    lines.append("=" * 40)
    lines.append(f"Total letters and digits (excluding spaces, punctuation, new lines, etc.): {total}")
    lines.append("")

    for char in ALPHABET:
        lines.append(f"{char} -> {counts[char]:>5} ({percentages[char]:>6.2f}%)")

    return "\n".join(lines)


def frequency_difference(
    reference_percentages: dict[str, float],
    candidate_percentages: dict[str, float]
) -> float:

    diff = 0.0
    for char in ALPHABET:
        diff += abs(reference_percentages[char] - candidate_percentages[char])
    return diff


def find_best_shift(reference_text: str, encrypted_text: str) -> tuple[int, float, list[tuple[int, float]]]:
    _, reference_percentages, reference_total = count_frequencies(reference_text)

    if reference_total == 0:
        raise ValueError("Reference text does not contain any characters from the alphabet a-z0-9.")

    ranking = []

    for shift in range(len(ALPHABET)):
        candidate_text = transform_text(encrypted_text, shift, "d")
        _, candidate_percentages, candidate_total = count_frequencies(candidate_text)

        if candidate_total == 0:
            score = float("inf")
        else:
            score = frequency_difference(reference_percentages, candidate_percentages)

        ranking.append((shift, score))

    ranking.sort(key=lambda x: x[1])
    best_shift, best_score = ranking[0]
    return best_shift, best_score, ranking


def get_file_path(prompt: str, default: str) -> str:
    value = input(f"{prompt} [{default}]: ").strip()
    return value if value else default


def get_shift() -> int:
    while True:
        try:
            return int(input("Enter shift value: ").strip())
        except ValueError:
            print("Error: please enter an integer.")


def encrypt_or_decrypt_file() -> None:
    while True:
        mode = input("Choose mode: [e] encrypt, [d] decrypt: ").strip().lower()
        if mode in ("e", "d"):
            break
        print("Error: enter 'e' or 'd'.")

    shift = get_shift()
    input_file = get_file_path("Input file", "input.txt")
    output_file = get_file_path("Output file", "output.txt")

    try:
        text = read_text(input_file)
        result = transform_text(text, shift, mode)
        write_text(output_file, result)
        print(f"Done. Output saved to: {output_file}")
    except Exception as error:
        print(f"Error: {error}")


def analyze_file() -> None:
    input_file = get_file_path("File to analyze", "input.txt")
    report_file = get_file_path("Report file", "analysis.txt")

    try:
        text = read_text(input_file)
        report = build_frequency_report(text)

        print("\n" + report + "\n")
        write_text(report_file, report)

        print(f"Report saved to: {report_file}")
    except Exception as error:
        print(f"Error: {error}")


def find_shift_and_decrypt() -> None:
    reference_file = get_file_path("Reference text file", "reference.txt")
    encrypted_file = get_file_path("Encrypted text file", "encrypted.txt")
    output_file = get_file_path("Decrypted output file", "decrypted.txt")
    ranking_file = get_file_path("Shift ranking file", "ranking.txt")

    try:
        reference_text = read_text(reference_file)
        encrypted_text = read_text(encrypted_file)

        best_shift, best_score, ranking = find_best_shift(reference_text, encrypted_text)

        decrypted_text = transform_text(encrypted_text, best_shift, "d")
        write_text(output_file, decrypted_text)

        lines = []
        lines.append("SHIFT RANKING")
        lines.append("=" * 30)
        for shift, score in ranking:
            lines.append(f"Shift {shift:>2} -> difference: {score:.4f}")

        report = "\n".join(lines)
        write_text(ranking_file, report)

        print(f"Best decryption shift: {best_shift}")
        print(f"Matching score: {best_score:.4f}")
        print(f"Decrypted text saved to: {output_file}")
        print(f"Ranking saved to: {ranking_file}")

    except Exception as error:
        print(f"Error: {error}")


def menu() -> None:
    while True:
        print("\n" + "=" * 50)
        print("PROGRAM: Encryption / Decryption / Frequency Analysis")
        print("=" * 50)
        print("1 - Encrypt / decrypt a file")
        print("2 - Character frequency analysis")
        print("3 - Find shift and decrypt")
        print("4 - Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            encrypt_or_decrypt_file()
        elif choice == "2":
            analyze_file()
        elif choice == "3":
            find_shift_and_decrypt()
        elif choice == "4":
            print("Program finished.")
            break
        else:
            print("Error: choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    menu()