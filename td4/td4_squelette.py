# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 12:22:34 2024

@author: JDION
"""

import random

from math import gcd


"""
GENERATION DE NB PREMIER SELON TEST DE PRIMALITE DE FERMAT
"""

def is_prime_fermat(n, k=100):
    """
    Teste si n est premier
    """
    if n <= 1:
        return False
    if n == 2: 
        return True
    
    for _ in range(k):
        a = random.randint(2, n - 2)  
        if pow(a, n - 1, n) != 1:  
            return False  
    
    return True  

def generate_prime(start, end, test_function):
    """
    Génère un nombre premier dans l'intervalle [start, end] à partir d'un test personnalisé
    """
    while True:
        candidate = random.randint(start, end)
        if test_function:
            if test_function(candidate):
                return candidate
            
            
"""
EXERCICE 1
"""

    
"""
EXERCICE 3
"""

"""
Q1
"""

def generate_rsa_keys(bits):
    """
    Génère les clés de l'algorithme RSA en forcant e = 3
    """
    e = 3
    p = generate_prime(0, 2 ** bits, is_prime_fermat)
    q = generate_prime(0, 2 ** bits, is_prime_fermat)
    n = p * q
    phi = (p - 1) * (q - 1)
    while p == q or gcd(e, phi) != 1:  # S'assurer que p et q sont distincts et gcd(e, phi) = 1
        p = generate_prime(0, 2 ** bits, is_prime_fermat)
        q = generate_prime(0, 2 ** bits, is_prime_fermat)
        n = p * q
        phi = (p - 1) * (q - 1)

    d = pow(e, -1, phi)

    return (e, n), (d, n)

def encrypt_message(message, public_key):
    """
    Chiffre le message
    """
    e, n = public_key
    return pow(message, e, n)

def string_to_int(message):
    """
    Convertit une chaîne de caractères en un entier unique en utilisant un encodage UTF-8.
    """
    return int.from_bytes(message.encode('utf-8'), 'big')

def int_to_string(number):
    """
    Convertit un entier en sa chaîne de caractères d'origine en utilisant un encodage UTF-8.
    """
    return number.to_bytes((number.bit_length() + 7) // 8, 'big').decode('utf-8')

# Génération des clés
public_key, private_key = generate_rsa_keys(bits=512)
print("Clé publique :", public_key)
print("Clé privée :", private_key)

# Message à chiffrer
message = "RSA fonctionne!"
print("Message original :", message)

# Conversion en entier
message_as_int = string_to_int(message)
print("Message converti en entier :", message_as_int)

# Chiffrement
ciphertext = encrypt_message(message_as_int, public_key)
print("Message chiffré :", ciphertext)

# Déchiffrement
decrypted_message_as_int = None # à compléter !
decrypted_message = int_to_string(decrypted_message_as_int)
print("Message déchiffré :", decrypted_message)

"""
Q2
"""

N1 = 2828397017089907131052840387106128713282514421195726109593859
c1 = 161340658484276930595607630148167439628632052300968205657282
N2 = 3093736383172883855913466918447482558463408826373170329533707
c2 = 2920025432866783050696766042954529191133978814738805935291595
N3 = 4495119919511106064205284407123143309601197579854381074387973
c3 = 742851878532958654303493521961761568283962501737283926134034


"""
EXERCICE 4
"""

def generate_rsa_keys(bits):
    """
    Génère les clés de l'algorithme RSA
    """
    p = generate_prime(0, 2 ** bits, is_prime_fermat)
    q = generate_prime(0, 2 ** bits, is_prime_fermat)
    while p == q:
        q = generate_prime(0, 2 ** bits, is_prime_fermat)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(2, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)

    d = pow(e, -1, phi)

    return (e, n), (d, n)

def encrypt_message(message, public_key):
    """
    Chiffre le message
    """
    e, n = public_key
    return pow(message, e, n)

def decrypt_message(ciphertext, private_key):
    """
    Déchiffre le message
    """
    d, n = private_key
    return pow(ciphertext, d, n)

# Génération des clés
public_key, private_key = generate_rsa_keys(bits=512)
print("Clé publique :", public_key)
print("Clé privée :", private_key)

# Message à chiffrer
message = "Hi"
print("Message original :", message)

# Ajout d'un padding aléatoire de 3 octets
padded_message = None # à compléter
print("Message paddé :") # à compléter
print("Message paddé converti en entier :") # à compléter

# Chiffrement
ciphertext = None # à compléter
print("Message chiffré :", ciphertext)

# Déchiffrement
decrypted_message_as_int = decrypt_message(ciphertext, private_key)
print("Message déchiffré :", decrypted_message_as_int)
print("Message déchiffré :", decrypted_message_as_int.to_bytes(length = len(padded_message[0]), byteorder='big'))

# Attaque de Bleichenbacher
retrieved_message = None # à compléter
print(f"Message récupéré : {retrieved_message}")
print(f"Message récupéré : {retrieved_message.to_bytes(length = len(padded_message[0]), byteorder='big')}")



