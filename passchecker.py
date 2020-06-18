import requests
import hashlib
import sys

def request_api_data(query_char):
    # SHA1 hash
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the API and try again')
    return res

def get_pass_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for hash, count in hashes:
        if hash == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    sha1password = (hashlib.sha1(password.encode('utf-8'))).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_pass_count(response, tail)

def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times')
        else:
            print(f'{password} was not found! Really good password!')
    return 'Execution Finished!'

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

