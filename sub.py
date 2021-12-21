import random
import requests
from bs4 import BeautifulSoup

def get_sub():
    r = requests.get(f'https://codeforces.com/api/user.status?handle=TheScrasse').json()['result']
    r = random.choice(r)
    id, contest_id = r['id'], r['contestId']

    html = requests.get(f'https://codeforces.com/contest/{contest_id}/submission/{id}').text
    soup = BeautifulSoup(html, "html.parser")
    problem = r['problem']

    problem_info = f"{problem['contestId']} {problem['index']} - {problem['name']} - *{r['verdict']}*"
    code = soup.find(id='program-source-text').text
    return problem_info + '\n' + f'`{code}`'

if __name__ == '__main__':
    print(get_sub())
