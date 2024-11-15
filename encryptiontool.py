from cryptography.fernet import Fernet
import argparse
import os


def generate_key(filename):
    key = Fernet.generate_key()     
    keyname = filename
    with open(filename,"wb") as file:
            file.write(key)
            return keyname
    
def encode(filename, key):
        with open(key,"rb") as keyfile:
            usedkey = keyfile.read()
            cipher = Fernet(usedkey)
            with open(filename, "rb") as file:
                data= file.read()
                encrypted = cipher.encrypt(data)
                with open(filename, 'wb') as encryptedfile:  
                    encryptedfile.write(encrypted)

def decode(filename, key):
    with open(key,"rb") as keyfile:
        usedkey = keyfile.read()
        cipher = Fernet(usedkey)
        with open(filename, 'rb') as file:
            data = file.read()
            decrypted = cipher.decrypt(data)
            with open(filename, 'wb') as decryptedfile:
                decryptedfile.write(decrypted)


def main():
    parser = argparse.ArgumentParser(description='Krypteringsverktyg')

    parser.add_argument('filename', help='Name when generating key or target file')
    parser.add_argument('-o','--operations', choices=['encrypt', 'decrypt', 'createkey'],help='What do you want to do', required=True)
    parser.add_argument('-k','--key', help='Choose the key you want to use')

    args =parser.parse_args()
    
    if args.operations == 'createkey':
        if os.path.exists(args.filename):
            print(f'{args.filename} already exists')
        elif not args.filename.endswith('.key'):
            print('Key needs the suffix .key')
            return
        else:
             generate_key(args.filename)
             print(f'Key {args.filename} has been created')

    elif args.operations == 'encrypt':
        if not os.path.exists(args.filename):
            print(f"{args.filename} doesn't exist")
            return
        elif not args.key:
            print('-k is required for encryption')
            return
        elif not os.path.exists(args.key) == True:
            print(f"{args.key} not found")
            return
        else:
            encode(args.filename, args.key)
            print(f'{args.filename} has been encrypted')
 
    elif args.operations =='decrypt':
        if not os.path.exists(args.filename):
            print(f"{args.filename} doesn't exist")
            return
        elif not args.key:
            print('-k is required for decryption')
            return
        elif not os.path.exists(args.key) == True:
            print(f"{args.key} not found")
            return
        else:
            decode(args.filename, args.key)
            print(f'{args.filename} has been decrypted')


if __name__=="__main__":
    main()