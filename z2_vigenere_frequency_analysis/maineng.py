ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def prepare_key(key):
    key = key.upper()
    result = ""

    for char in key:
        if char in ALPHABET:
            result += char

    return result


def keep_only_alphabet_chars(text):
    result = ""

    for char in text.upper():
        if char in ALPHABET:
            result += char

    return result


def vigenere(text, key, mode):
    text = text.upper()
    key = prepare_key(key)

    if len(key) == 0:
        print("Error: key must contain at least one letter or digit from A-Z, 0-9.")
        return ""

    result = ""
    key_index = 0
    alphabet_length = len(ALPHABET)

    for char in text:
        if char in ALPHABET:
            text_index = ALPHABET.index(char)
            key_char = key[key_index % len(key)]
            key_char_index = ALPHABET.index(key_char)

            if mode == "e":
                new_index = (text_index + key_char_index) % alphabet_length
            elif mode == "d":
                new_index = (text_index - key_char_index) % alphabet_length
            else:
                print("Error: unknown mode.")
                return ""

            result += ALPHABET[new_index]
            key_index += 1
        else:
            result += char

    return result


def split_into_columns(text_without_symbols, key_length):
    columns = []

    for i in range(key_length):
        column = ""
        j = i

        while j < len(text_without_symbols):
            column += text_without_symbols[j]
            j += key_length

        columns.append(column)

    return columns


def decrypt_caesar_fragment(fragment, shift):
    result = ""
    n = len(ALPHABET)

    for char in fragment:
        index = ALPHABET.index(char)
        new_index = (index - shift) % n
        result += ALPHABET[new_index]

    return result


def fragment_score(fragment):
    if len(fragment) == 0:
        return -10**9

    counter = {}

    for char in ALPHABET:
        counter[char] = 0

    for char in fragment:
        counter[char] += 1

    unique_chars = 0
    max_count = 0

    for char in ALPHABET:
        if counter[char] > 0:
            unique_chars += 1
        if counter[char] > max_count:
            max_count = counter[char]

    score = unique_chars

    if max_count / len(fragment) > 0.5:
        score -= 20

    return score


def find_best_shift_for_fragment(fragment):
    best_shift = 0
    best_score = -10**9

    for shift in range(len(ALPHABET)):
        candidate = decrypt_caesar_fragment(fragment, shift)
        score = fragment_score(candidate)

        if score > best_score:
            best_score = score
            best_shift = shift

    return best_shift


def find_key(text, key_length):
    text_without_symbols = keep_only_alphabet_chars(text)

    if len(text_without_symbols) == 0:
        return ""

    columns = split_into_columns(text_without_symbols, key_length)
    key = ""

    for column in columns:
        shift = find_best_shift_for_fragment(column)
        key += ALPHABET[shift]

    return key


def full_text_score(text):
    text = text.upper()

    alphabet_count = 0
    other_count = 0
    counter = {}

    for char in ALPHABET:
        counter[char] = 0

    for char in text:
        if char in ALPHABET:
            alphabet_count += 1
            counter[char] += 1
        elif char in " \n\t.,;:!?-()\"'":
            pass
        else:
            other_count += 1

    if alphabet_count == 0:
        return -10**9

    score = 0
    score += alphabet_count
    score -= other_count * 2

    unique_chars = 0
    max_count = 0

    for char in ALPHABET:
        if counter[char] > 0:
            unique_chars += 1
        if counter[char] > max_count:
            max_count = counter[char]

    score += unique_chars * 2

    if max_count / alphabet_count > 0.35:
        score -= 30

    return score


def automatic_break(text, max_key_length):
    best_key = ""
    best_result = ""
    best_score = -10**9

    for key_length in range(1, max_key_length + 1):
        key = find_key(text, key_length)

        if key == "":
            continue

        result = vigenere(text, key, "d")
        score = full_text_score(result)

        if score > best_score:
            best_score = score
            best_key = key
            best_result = result

    return best_key, best_result


def character_frequency_analysis(text):
    text = text.upper()
    counter = {}

    for char in ALPHABET:
        counter[char] = 0

    total = 0

    for char in text:
        if char in ALPHABET:
            counter[char] += 1
            total += 1

    ranking = []

    for char in ALPHABET:
        percentage = (counter[char] / total) * 100 if total > 0 else 0.0
        ranking.append((char, counter[char], percentage))

    ranking.sort(key=lambda x: (-x[1], x[0]))
    return ranking, total


def split_into_words(text):
    text = text.upper()
    words = []
    current = ""

    for char in text:
        if char in ALPHABET:
            current += char
        else:
            if current != "":
                words.append(current)
                current = ""

    if current != "":
        words.append(current)

    return words


def word_analysis(text):
    words = split_into_words(text)
    counter = {}

    for word in words:
        if word in counter:
            counter[word] += 1
        else:
            counter[word] = 1

    most_common = sorted(counter.items(), key=lambda x: (-x[1], x[0]))
    least_common = sorted(counter.items(), key=lambda x: (x[1], x[0]))

    return most_common, least_common, len(words), len(counter)


def print_analysis(text, title):
    char_ranking, total_chars = character_frequency_analysis(text)
    most_common_words, least_common_words, total_words, unique_words = word_analysis(text)

    print()
    print("===", title, "===")
    print("Number of letters/digits from alphabet:", total_chars)
    print("Number of words:", total_words)
    print("Number of unique words:", unique_words)
    print()

    print("3 most common letters/digits:")
    for char, count, percentage in char_ranking[:3]:
        print(f"{char} -> {count} ({percentage:.2f}%)")

    print()
    print("3 least common letters/digits:")
    rare_chars = sorted(char_ranking, key=lambda x: (x[1], x[0]))[:3]
    for char, count, percentage in rare_chars:
        print(f"{char} -> {count} ({percentage:.2f}%)")

    print()
    print("3 most common words:")
    if len(most_common_words) == 0:
        print("No words")
    else:
        for word, count in most_common_words[:3]:
            print(f"{word} -> {count}")

    print()
    print("3 least common words:")
    if len(least_common_words) == 0:
        print("No words")
    else:
        for word, count in least_common_words[:3]:
            print(f"{word} -> {count}")


def get_analysis_summary(text):
    char_ranking, _ = character_frequency_analysis(text)
    most_common_words, least_common_words, _, _ = word_analysis(text)

    most_common_chars = char_ranking[:3]
    least_common_chars = sorted(char_ranking, key=lambda x: (x[1], x[0]))[:3]

    return most_common_chars, least_common_chars, most_common_words[:3], least_common_words[:3]


def print_char_list(items):
    if len(items) == 0:
        print("None")
    else:
        for char, count, percentage in items:
            print(f"{char} -> {count} ({percentage:.2f}%)")


def print_word_list(items):
    if len(items) == 0:
        print("None")
    else:
        for word, count in items:
            print(f"{word} -> {count}")


def print_comparison(text1, title1, text2, title2):
    mc1, lc1, mw1, lw1 = get_analysis_summary(text1)
    mc2, lc2, mw2, lw2 = get_analysis_summary(text2)

    print()
    print("==================================================")
    print("ANALYSIS COMPARISON")
    print("==================================================")

    print()
    print(f"--- {title1} ---")
    print("Most common letters/digits:")
    print_char_list(mc1)
    print("Least common letters/digits:")
    print_char_list(lc1)
    print("Most common words:")
    print_word_list(mw1)
    print("Least common words:")
    print_word_list(lw1)

    print()
    print(f"--- {title2} ---")
    print("Most common letters/digits:")
    print_char_list(mc2)
    print("Least common letters/digits:")
    print_char_list(lc2)
    print("Most common words:")
    print_word_list(mw2)
    print("Least common words:")
    print_word_list(lw2)


def generate_key_from_pattern(pattern, length):
    prepared_pattern = prepare_key(pattern)

    if len(prepared_pattern) == 0:
        return ""

    result = ""
    i = 0

    while len(result) < length:
        result += prepared_pattern[i % len(prepared_pattern)]
        i += 1

    return result


def get_user_keys():
    lengths = [3, 6, 9, 12, 16]
    keys = {}

    print()
    print("Enter your own keys for lengths 3, 6, 9, 12, 16.")
    print("If a key is longer, it will be truncated.")
    print("If it becomes too short after filtering, the program will ask again.")
    print()

    for length in lengths:
        while True:
            key = input(f"Enter key of length {length}: ").strip()
            key = prepare_key(key)

            if len(key) < length:
                print("Filtered key is too short. Please enter a longer key.")
            else:
                keys[length] = key[:length]
                break

    return keys


def generate_keys_from_pattern(pattern):
    lengths = [3, 6, 9, 12, 16]
    keys = {}

    for length in lengths:
        keys[length] = generate_key_from_pattern(pattern, length)

    return keys


def compare_key_lengths(text, base_name):
    print()
    print("=== FREQUENCY COMPARISON FOR KEY LENGTHS 3, 6, 9, 12, 16 ===")
    print("1 - user provides custom keys")
    print("2 - keys generated from pattern 'zaq1@WSX'")

    choice = input("Choose option (1/2): ").strip()

    if choice == "1":
        keys = get_user_keys()
        print()
        print("Using user-provided keys.")
    elif choice == "2":
        pattern = "zaq1@WSX"
        prepared_pattern = prepare_key(pattern)

        print()
        print("Original pattern:", pattern)
        print("Pattern after filtering:", prepared_pattern)

        if len(prepared_pattern) == 0:
            print("Error: filtered pattern is empty.")
            return

        keys = generate_keys_from_pattern(pattern)
    else:
        print("Invalid option.")
        return

    for length in [3, 6, 9, 12, 16]:
        key = keys[length]
        result = vigenere(text, key, "e")
        output_name = f"{base_name}_key_{length}.txt"

        with open(output_name, "w", encoding="utf-8") as file:
            file.write(result)

        print()
        print("--------------------------------------------------")
        print(f"Key length: {length}")
        print(f"Key used: {key}")
        print(f"Saved file: {output_name}")

        print_analysis(result, f"ANALYSIS FOR KEY LENGTH {length}")
        print_comparison(text, "BEFORE ENCRYPTION", result, "AFTER ENCRYPTION")


def main():
    print("=== Vigenere Cipher ===")
    print("Alphabet:", ALPHABET)
    print("e - encrypt")
    print("d - decrypt")
    print("a - automatic breaking without key")
    print("p - compare frequencies for key lengths 3, 6, 9, 12, 16")

    mode = input("Choose mode (e/d/a/p): ").strip().lower()

    if mode not in ["e", "d", "a", "p"]:
        print("Error: choose 'e', 'd', 'a' or 'p'.")
        return

    input_file = input("Enter input file name: ").strip()

    try:
        with open(input_file, "r", encoding="utf-8") as file:
            text = file.read()
    except FileNotFoundError:
        print("Error: input file not found.")
        return
    except Exception as e:
        print("Error while reading file:", e)
        return

    print_analysis(text, "INPUT FILE ANALYSIS")

    if mode in ["e", "d"]:
        output_file = input("Enter output file name: ").strip()
        key = input("Enter key: ").strip()
        result = vigenere(text, key, mode)

        if result == "":
            return

        try:
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(result)
        except Exception as e:
            print("Error while writing file:", e)
            return

        print()
        print("Done. Result saved to file:", output_file)
        print_analysis(result, "OUTPUT FILE ANALYSIS")

        if mode == "e":
            print_comparison(text, "BEFORE ENCRYPTION", result, "AFTER ENCRYPTION")
        else:
            print_comparison(text, "BEFORE DECRYPTION", result, "AFTER DECRYPTION")

    elif mode == "a":
        output_file = input("Enter output file name: ").strip()

        try:
            max_key_length = int(input("Enter maximum key length to test: ").strip())
        except ValueError:
            print("Error: this must be an integer.")
            return

        key, result = automatic_break(text, max_key_length)

        if key == "":
            print("Could not find a key.")
            return

        try:
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(result)
        except Exception as e:
            print("Error while writing file:", e)
            return

        print()
        print("Probable key:", key)
        print("Done. Decrypted text saved to file:", output_file)
        print_analysis(result, "DECRYPTED FILE ANALYSIS")
        print_comparison(text, "BEFORE DECRYPTION", result, "AFTER DECRYPTION")

    elif mode == "p":
        base_name = input("Enter base name for output files: ").strip()
        compare_key_lengths(text, base_name)


main()