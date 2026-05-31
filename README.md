# 🔐 Data Protection — Cryptography Exercises and Algorithms

<p align="center">
  <strong>A collection of Python exercises, implementations and study materials for the Data Protection course.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Course-Data_Protection-111827?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Type-Educational_Project-4B5563?style=for-the-badge" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Classical-Caesar_|_Vigenere-2563EB?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Cryptanalysis-Frequency_|_IC_|_Kasiski-7C3AED?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Number_Theory-Modular_Arithmetic-0891B2?style=for-the-badge" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Asymmetric-RSA_|_ElGamal_|_Diffie--Hellman-DC2626?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Attacks-MITM_|_Known_Plaintext-B91C1C?style=for-the-badge" />
  <img src="https://img.shields.io/badge/OpenPGP-Digital_Signatures-475569?style=for-the-badge" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Hashing-DJB2_|_Adler32-F59E0B?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Collisions-Birthday_Paradox-10B981?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Rainbow_Tables-Hash_Chains-059669?style=for-the-badge" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Study_Note-Polish_PDF-0F172A?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" />
</p>

---

## 📚 Table of Contents

- [Overview](#overview)
- [Repository Contents](#repository-contents)
- [Polish Study Note](#polish-study-note)
- [Repository Structure](#repository-structure)
- [Task List](#task-list)
- [Task Details](#task-details)
- [Technologies](#technologies)
- [Key Concepts](#key-concepts)
- [How to Run](#how-to-run)
- [Example Workflows](#example-workflows)
- [Purpose](#purpose)
- [Disclaimer](#disclaimer)
- [Author](#author)

---

<a id="overview"></a>

## 📌 Overview

This repository contains a collection of practical exercises and algorithm implementations prepared for the **Data Protection** course.

The project focuses on understanding selected cryptographic concepts through simple Python programs. It includes classical ciphers, cryptanalysis methods, modular arithmetic, asymmetric cryptography, hash functions, collision testing and hash table experiments.

The repository also includes a Polish PDF study note with theory, formulas, examples and solved tasks.

---

<a id="repository-contents"></a>

## 📦 Repository Contents

The repository contains:

- Python implementations of cryptographic algorithms
- exercises related to classical and asymmetric cryptography
- frequency analysis and basic cryptanalysis tools
- primality testing examples
- RSA, Diffie–Hellman and ElGamal implementations
- hash functions and collision testing scripts
- hash table and reduction chain experiments
- a Polish PDF study note for revision

---

<a id="polish-study-note"></a>

## 📄 Polish Study Note

The repository includes a PDF file:

```txt
ochronadanych.pdf
```

The note is written in Polish and was prepared as a study material for the course.

It covers the following areas:

### Modular Arithmetic and Number Theory

- modular arithmetic
- fast modular exponentiation
- Extended Euclidean Algorithm
- modular inverse
- greatest common divisor
- Euler's phi function
- trial division
- primality testing
- Sieve of Eratosthenes
- Lucas-Lehmer test
- Mersenne numbers
- generators modulo p
- discrete logarithm

### Classical Cryptography and Cryptanalysis

- Caesar cipher
- Vigenère cipher
- Index of Coincidence
- Kasiski examination
- ASCII, UTF-8 and text representation

### Asymmetric Cryptography

- Diffie–Hellman key exchange
- Man-in-the-Middle attack
- RSA
- text-to-number conversion and byte blocks
- ElGamal
- public key vs private key
- symmetric vs asymmetric encryption
- why RSA works
- known plaintext attack

### OpenPGP and Digital Signatures

- OpenPGP Studio
- RSA key generation
- public key exchange
- file encryption and decryption
- digital signatures
- signature verification
- data integrity

### Hash Functions and Collisions

- hash functions
- DJB2
- Adler32
- hash collisions
- Birthday Paradox
- collision probability
- Rainbow Tables
- reduction functions
- hash tables
- hash → reduction → hash chains
- bit operations

---

<a id="repository-structure"></a>

## 📁 Repository Structure

```txt
data-protection/
├── z1_caesar_shift_frequency/
├── z2_vigenere_frequency_analysis/
├── z3_vigenere_key_length_ic_kasiski/
├── z4_sprawdzanie_czy_pierwsza/
├── z5_wymiana_klucza_Diffiego-Hellmana_ALA/
├── z6_Diffie-Hellman_atak_man-in-the-middle/
├── z7_nwd-rozszerzony-euklides-odwrotnosc-modulo/
├── z8_RSA-generowanie-kluczy-szyfrowanie/
├── z9_elgamal-szyfrowanie-atak-znany-blok/
├── z10_DJB_Adler32_testkolizji/
├── z11_Tablice-hashów_redukcja_i_szukanie-kolizji-DJB/
├── ochronadanych.pdf
├── README.md
├── LICENSE
└── .gitignore
```

---

<a id="task-list"></a>

## 🧩 Task List

| Folder | Topic | Description |
|---|---|---|
| `z1_caesar_shift_frequency` | Caesar cipher | Shift cipher implementation, text transformation and frequency analysis |
| `z2_vigenere_frequency_analysis` | Vigenère cipher | Vigenère encryption, decryption, frequency analysis and automatic breaking attempts |
| `z3_vigenere_key_length_ic_kasiski` | IC and Kasiski | Estimating Vigenère key length using Index of Coincidence and Kasiski examination |
| `z4_sprawdzanie_czy_pierwsza` | Primality testing | Sieve of Eratosthenes, trial division and Lucas-Lehmer test |
| `z5_wymiana_klucza_Diffiego-Hellmana_ALA` | Diffie–Hellman | Shared secret calculation from one participant's perspective |
| `z6_Diffie-Hellman_atak_man-in-the-middle` | MITM attack | Diffie–Hellman communication with Alice, Bob and Eve roles |
| `z7_nwd-rozszerzony-euklides-odwrotnosc-modulo` | Extended Euclidean Algorithm | GCD, modular inverse and congruence solving |
| `z8_RSA-generowanie-kluczy-szyfrowanie` | RSA | RSA key generation, text encryption and decryption |
| `z9_elgamal-szyfrowanie-atak-znany-blok` | ElGamal | ElGamal encryption, decryption and known plaintext attack example |
| `z10_DJB_Adler32_testkolizji` | Hash functions | DJB2, Adler32, collision probability and collision tests |
| `z11_Tablice-hashów_redukcja_i_szukanie-kolizji-DJB` | Hash tables and reduction | DJB hash chains, reduction functions, hash table creation and collision search |

---

<a id="task-details"></a>

## 🔎 Task Details

### `z1_caesar_shift_frequency`

Main files:

```txt
caesar_shift_frequency.py
maineng.py
przestawieniowy.py
```

This task includes a Caesar-style shift cipher for letters and digits, file input/output, encryption, decryption and frequency analysis.  
The folder also contains an additional transposition-style script.

---

### `z2_vigenere_frequency_analysis`

Main files:

```txt
vigenere_frequency_analysis.py
maineng.py
main4.py
biblia.txt
```

This task focuses on the Vigenère cipher.  
It includes text cleaning, key preparation, encryption, decryption, frequency analysis, column splitting and automatic attempts to recover the key.

The `biblia.txt` file is used as sample text input.

---

### `z3_vigenere_key_length_ic_kasiski`

Main files:

```txt
metoda1_IC/metoda1.py
metoda2_Kasinski/metoda2.py
```

This task contains two approaches for estimating the Vigenère key length:

- Index of Coincidence analysis
- Kasiski examination

The scripts analyze ciphertext structure, repeated fragments and possible key lengths.

---

### `z4_sprawdzanie_czy_pierwsza`

Main files:

```txt
main.py
main2.py
main3.py
```

This task compares primality testing methods:

- Sieve of Eratosthenes
- trial division
- Lucas-Lehmer test

The scripts also include experiments related to Mersenne numbers.

---

### `z5_wymiana_klucza_Diffiego-Hellmana_ALA`

Main file:

```txt
main.py
```

This task implements Diffie–Hellman key exchange from one participant's perspective.  
It includes modular exponentiation, primality checking and shared secret calculation.

---

### `z6_Diffie-Hellman_atak_man-in-the-middle`

Main file:

```txt
main.py
```

This task demonstrates the Man-in-the-Middle concept in Diffie–Hellman key exchange.

The program contains separate roles:

```txt
Alice
Bob
Eve
```

It shows why unauthenticated Diffie–Hellman is vulnerable to active key substitution.

---

### `z7_nwd-rozszerzony-euklides-odwrotnosc-modulo`

Main file:

```txt
main.py
```

This task implements the Extended Euclidean Algorithm.

It includes:

- GCD calculation
- table-based Euclidean steps
- modular inverse
- solving modular congruences

---

### `z8_RSA-generowanie-kluczy-szyfrowanie`

Main file:

```txt
main.py
```

This task implements RSA basics.

It includes:

- prime number validation
- random prime selection
- Euler's phi calculation
- public exponent selection
- modular inverse calculation
- text encryption
- text decryption

---

### `z9_elgamal-szyfrowanie-atak-znany-blok`

Main file:

```txt
ElGamal.py
```

This task implements ElGamal encryption.

It includes:

- modular exponentiation
- modular inverse
- prime number validation
- text-to-block conversion
- encryption
- decryption with a private key
- known plaintext attack demonstration

The implementation uses two-byte message blocks, so the prime number `p` should be greater than `65536`.

---

### `z10_DJB_Adler32_testkolizji`

Main file:

```txt
zadanie.py
```

This task compares two simple hash/checksum algorithms:

```txt
DJB2
Adler32
```

It includes:

- text hashing
- random text generation
- collision probability estimation
- expected number of collisions
- collision testing

---

### `z11_Tablice-hashów_redukcja_i_szukanie-kolizji-DJB`

Main file:

```txt
zadanie.py
```

This task focuses on hash tables and reduction chains based on DJB2.

It includes:

- DJB2 hashing
- reduction function
- random text generation
- hash → reduction → hash chains
- hash table generation
- searching inside chains
- collision search

---

<a id="technologies"></a>

## 🛠️ Technologies

| Area | Tools / Concepts |
|---|---|
| Language | Python |
| Cryptography | RSA, ElGamal, Diffie–Hellman |
| Classical ciphers | Caesar, Vigenère |
| Cryptanalysis | Frequency analysis, Index of Coincidence, Kasiski examination |
| Number theory | Modular arithmetic, GCD, modular inverse, primality testing |
| Hashing | DJB2, Adler32 |
| Data structures | Hash tables, reduction chains |
| Documentation | Markdown, PDF |
| Version control | Git, GitHub |

---

<a id="key-concepts"></a>

## 🔑 Key Concepts

### Modular Arithmetic

Many tasks are based on calculations performed modulo `n`.

Examples:

```txt
(a + b) mod n
(a * b) mod n
a^b mod n
```

These operations are essential for RSA, Diffie–Hellman and ElGamal.

---

### Classical Cryptography

The repository includes classical ciphers such as Caesar and Vigenère.

These tasks show how substitution and polyalphabetic ciphers work, and how they can be analyzed using frequency analysis, Index of Coincidence and Kasiski examination.

---

### Asymmetric Cryptography

The asymmetric cryptography section focuses on algorithms that use public and private keys.

Included algorithms:

```txt
Diffie–Hellman
RSA
ElGamal
```

The tasks include key generation, encryption, decryption, shared secret calculation and basic attack scenarios.

---

### OpenPGP and Digital Signatures

The Polish PDF note also includes an OpenPGP section.

It explains:

- RSA key generation
- public and private keys
- public key exchange
- file encryption
- file decryption
- digital signatures
- verification
- data integrity

---

### Hash Functions and Collisions

The hashing section includes simple hash/checksum algorithms:

```txt
DJB2
Adler32
```

The goal is to test how hash values are generated, how collisions occur and why simple hash functions should not be used for real cryptographic security.

---

<a id="how-to-run"></a>

## 🚀 How to Run

1. Clone the repository:

```bash
git clone https://github.com/Avuii/ochrona-danych.git
cd ochrona-danych
```

2. Go to the selected task folder:

```bash
cd z8_RSA-generowanie-kluczy-szyfrowanie
```

3. Run the Python script:

```bash
python main.py
```

or, depending on the task:

```bash
python zadanie.py
```

For the ElGamal task:

```bash
python ElGamal.py
```

---

<a id="example-workflows"></a>

## 🧪 Example Workflows

### RSA workflow

1. Choose prime numbers `p` and `q`.
2. Calculate `n = p * q`.
3. Calculate `phi(n) = (p - 1) * (q - 1)`.
4. Choose public exponent `e`.
5. Calculate private exponent `d`.
6. Encrypt the message.
7. Decrypt the ciphertext.

### Diffie–Hellman workflow

1. Choose public values `p` and `g`.
2. Alice chooses private value `a`.
3. Bob chooses private value `b`.
4. Alice calculates public value `A`.
5. Bob calculates public value `B`.
6. Both sides calculate the same shared secret.

### Hash collision workflow

1. Generate random text.
2. Calculate its hash.
3. Store the hash in a table.
4. Generate another text.
5. Check whether the hash already exists.
6. If yes, a collision was found.

---

<a id="purpose"></a>

## 🎯 Purpose

This repository was created to:

- organize course exercises in one place
- practice implementing cryptographic algorithms
- understand modular arithmetic in practice
- prepare for tests and practical assignments
- document solutions in a clean and reusable form
- keep both code and study materials together

---

<a id="disclaimer"></a>

## ⚠️ Disclaimer

This repository is intended for educational purposes only.

The implementations are simplified and should not be used in real-world security systems.

Algorithms such as `DJB2` and `Adler32` are not cryptographically secure and are used here only for learning and experimentation.


---

<a id="author"></a>

## 👩‍💻 Author

Created by **Katarzyna Stańczyk**.
