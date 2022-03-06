import random
import requests
import threading
import time
from bs4 import BeautifulSoup

def time_cache(tl):
    def inner(f):
        lock = threading.Lock()
        t = 0
        res = None

        def foo():
            nonlocal t, res

            with lock:
                t2 = time.time()
                if t2 > t:
                    res = f()
                    t = t2 + tl
                return res
        return foo
    return inner

@time_cache(3600)
def get_list():
    r = requests.get(f'https://codeforces.com/api/user.status?handle=TheScrasse')
    return r.json()['result']

def get_sub():
    r = random.choice(get_list())
    id, contest_id = r['id'], r['contestId']

    html = requests.get(f'https://codeforces.com/contest/{contest_id}/submission/{id}').text
    soup = BeautifulSoup(html, "html.parser")
    problem = r['problem']

    problem_info = f"{problem['contestId']} {problem['index']} - {problem['name']} - *{r['verdict']}*"
    code = soup.find(id='program-source-text').text
    return problem_info + '\n' + f'`{code}`'

if __name__ == '__main__':
    print(get_sub())
