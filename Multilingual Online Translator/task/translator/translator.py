import requests
from bs4 import BeautifulSoup
import sys

languages = {
    '1': 'arabic',
    '2': 'german',
    '3': 'english',
    '4': 'spanish',
    '5': 'french',
    '6': 'hebrew',
    '7': 'japanese',
    '8': 'dutch',
    '9': 'polish',
    '10': 'portuguese',
    '11': 'romanian',
    '12': 'russian',
    '13': 'turkish'
}

language_in = sys.argv[1]
language_out = sys.argv[2]
word = sys.argv[3]


def get_lang(lng_in, lng_out):
    return str(f'{lng_in}-{lng_out}')


def get_url(lang):
    url = 'https://context.reverso.net/translation/' + lang + '/' + word
    return url


def get_translations(language_in, language_out, file):
    url = get_url(get_lang(language_in, language_out))
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        page = requests.get(url, headers=headers)
    except requests.exceptions.ConnectionError:
        print('Something wrong with your internet connection')
    soup = BeautifulSoup(page.content, 'html.parser', from_encoding='utf-8')
    words = soup.find_all('span', {'class': 'display-term'})
    if len(words) == 0:
        print(f'Sorry, unable to find {word}')
        exit()
    offers_left = soup.find_all('div', {'class': 'src ltr'})
    offers_right = soup.find_all('div', {'class': ['trg ltr', 'trg rtl arabic', 'trg rtl']})
    translations_words = []
    translations_offers_l = []
    translations_offers_r = []
    for c, w, l, r in zip(range(1), words, offers_left, offers_right):
        translations_words.append(w.text)
        of_l = l.text.strip()
        of_r = r.text.strip()
        translations_offers_l.append(of_l)
        translations_offers_r.append(of_r)
    print(f'{language_out.capitalize()} Translations:')
    file.write(f'{language_out.capitalize()} Translations:\n')
    for w in translations_words:
        print(w)
        file.write(w + '\n')
    file.write('\n')
    print()
    print(f'{language_out.capitalize()} Examples:')
    file.write(f'{language_out.capitalize()} Examples:\n')
    for offer_l, offer_r in zip(translations_offers_l, translations_offers_r):
        print(offer_l)
        print(offer_r)
        file.write(offer_l + '\n')
        file.write(offer_r + '\n')
    file.write('\n')
    print()


def execute():
    if language_out != 'all':
        if language_out not in languages.values():
            print(f"Sorry, the program doesn't support {language_out}")
            exit()
    with open(f'{word}.txt', 'w', encoding='utf-8') as file:
        if language_out != 'all':
            get_translations(language_in, language_out, file, )
        else:
            for i in range(1, 14):
                if languages[str(i)] != language_in:
                    get_translations(language_in, languages[str(i)], file)


if __name__ == '__main__':
    execute()
