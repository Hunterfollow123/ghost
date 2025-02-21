# Hunterfollow123

import requests
import threading
import random

quotes = ['what an idiot..', 'only use on moroccans, jk! or not..', 'this will be fast', '<insert cool quote :D>', '@Hunterfollow123', 'make sure the url is correct']
banner = f'''
          /`._      ,
         /     \\   / \\
         ) ,-==-> /\\/ \\
          )__\\/ // \\  |
         /  /' \\//   | |
        /  (  /|/    | /     {random.choice(quotes)}
       /     //|    /,'
      // /  (( )    '
     //     // \\    |
    //     (#) |
   /        )\\/ \\   '       ____
  /        /#/   )         /,.__\\__,,--=_,
 /         \\#\\  /)      __/ + \\____,--==<
 //gnv_____/#/_/'      (\\_\\__+/_,   ---<^
                                '==--=='
                                
'''
print(banner)
with open('admin wordlist.txt', 'r') as file:
    words = [word.strip() for word in file.readlines()]

link = str(input('Enter the target URL (e.g., https://example.com) No slashes! "\\": ')).strip()

print('\nFinding admin panel...')

found_panel = threading.Event()

def check_path(word):
    full_link = f"{link}/{word}"
    try:
        resp = requests.get(full_link, timeout=5)
        print(f"Trying: /{word} [{resp.status_code}]")
        if resp.status_code != 404 and resp.status_code != 403 and not found_panel.is_set():
            print(f"\nAdmin panel found: {full_link}")
            found_panel.set()
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {full_link}: {e}")

def worker(start, end):
    for word in words[start:end]:
        if not found_panel.is_set():
            check_path(word)

num_threads = 12
chunk_size = len(words) // num_threads
threads = []

for i in range(num_threads):
    start = i * chunk_size
    end = start + chunk_size if i != num_threads - 1 else len(words)
    thread = threading.Thread(target=worker, args=(start, end))
    threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print("Search complete.")
