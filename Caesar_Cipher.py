letter_list = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encrypt(plaintext,key):
    ciphertext = ''
    for ch in plaintext:
        if ch.isalpha(): # the plaintext is alpha or not
            if ch.isupper():
                ciphertext += letter_list[(ord(ch)-65+key) % 26] # upper or lower
            else:
                ciphertext += letter_list[(ord(ch)-97+key) % 26].lower()
        else:
            ciphertext+=ch
    return ciphertext

def decrypt(ciphertext,key):
    plaintext = ''
    for ch in ciphertext:
        if ch.isalpha():
            if ch.isupper():
                plaintext += letter_list[(ord(ch)-65-key)%26]
            else:
                plaintext += letter_list[(ord(ch)-97-key)%26].lower()
        else:
            plaintext += ch
    return plaintext

# # Test
# user_input = input("encode D, decode E: ")
# while(user_input != 'D' and user_input != 'E'):
#     user_input = input("wrong, input again: ")

# key = input("input key: ")
# while(int(key.isdigit() == 0)):
#     key = input("wrong, key is digit, input again: ")

# if user_input == 'D':
#     plaintext = input("input plaintext: ")
#     ciphertext = encrypt(plaintext, int(key))
#     print('ciphertext: \n%s' % ciphertext)
# else:
#     ciphertext = input("input ciphertext: ")
#     plaintext = decrypt(ciphertext, int(key))
#     print('plaintext: \n%s\n'%ciphertext)