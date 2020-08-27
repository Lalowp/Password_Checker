import requests
import hashlib

try:
    with open('.txt', mode='r') as password: # Add the name of your file
        text = password.readlines()
except FileNotFoundError as error:
    print('Check the file path')


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the API and try again')
    return res

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    #check password if it exist in API response
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)

def main(args):
    for password in args:
        count = pwned_api_check(password)
        password_len  = len(password)
        password_star = password_len* '*' # Here, you can avoid showing the password by deleting the password_star parameter
        if count:                         # In case you will like to see the stars, then leave it like this
            print(f'{password_star} was found {count} times, you should change it')
        else:
            print(f'{password_star} was not found. Use it!')

if __name__ == '__main__':
    main(text) 

