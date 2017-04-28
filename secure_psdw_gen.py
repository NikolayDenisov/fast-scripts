#!/usr/bin/python3.6

"""Generate password for me and encode with cipher ROT"""

import sys
import string
import secrets


def generate_pw(pswd_len=9):
    """Encodes a string (s) using ROT (ROT_number) encoding."""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(pswd_len))
    return password


def encode(password, rotate=13):
    """Encodes a string (password) using ROT (rotate) encoding."""
    rotate %= 26  # To avoid IndexErrors
    alpha = "abcdefghijklmnopqrstuvwxyz" * 2
    alpha += alpha.upper()

    def get_i():
        """"get index for i"""
        for i in range(26):
            yield i  # indexes of the lowercase letters
        for i in range(53, 78):
            yield i  # indexes of the uppercase letters
    rot = {alpha[i]: alpha[i + rotate] for i in get_i()}
    return "".join(rot.get(i, i) for i in password)


def decode(password, rotate=13):
    """Decodes a string (password) using ROT (rotate) encoding."""
    return encode(password, abs(rotate % 26 - 26))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("You must set argument!")
    elif sys.argv[1] == 'generate':
        print(generate_pw(9))
    elif sys.argv[1] == 'encode':
        print(encode(sys.argv[2], int(sys.argv[3])))
    elif sys.argv[1] == 'decode':
        print(decode(sys.argv[2], int(sys.argv[3])))
