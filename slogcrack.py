import hashlib
import time
import sys

TEST_HASH_TO_CRACK = '54d381f9733bede2d0f532654ad9f7d2'  # password == Unicorn69


def crack_hash(pw_list, hashed_pw):
    start_time = time.time()
    cracked_pw = "Not in list"
    with open(pw_list, "r") as pl:
        for pw in pl:
            hash = hashlib.md5(pw.strip().encode('utf8')).hexdigest()
            if hash == hashed_pw:
                cracked_pw = pw
                break
    end_time = time.time()
    return f'HASH[ {hashed_pw} ] == "{cracked_pw.strip()}". It took {end_time - start_time} seconds.'


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('usage: {sys.argv[0]} password_file MD5_hash')
    else:
        print(crack_hash(sys.argv[1], sys.argv[2]))
