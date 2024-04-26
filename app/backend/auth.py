import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get('SPREADSHEETS_API_KEY')


def authenticate_sheets():
    return build('sheets', 'v4', developerKey=API_KEY).spreadsheets()


# Example

SHEETS = {
    1: '1yFa0KKmWQ8ptFESTNRX18zmDWlDXBy6SGruJ7IpIEas',
    2: '1jd7Es4eNpjYDHS1CTfhdWX-7eTaTsYqzwbixALeUtqI',
    3: '1cqAU98YevCKO7I11ywlcmz_yJ1hLXxmlI0BDNvIaynk',
    4: '17y33ViTAnl2IKCPZtkY4sIr-36_QYG8Ca1aXKQhvJKc',
    5: '1DE7M9ApQJcz0-9lBoRizLbe0F9jR7Ck7tIEXqO3OxEU',
    6: '1203HHjpR9XJDdARJtJMLcpRfIVhwpmrJzMKFkAuo8W8',
    7: '1LPqQq4nYQNgxFXLPtExitLkZUBGJaYCYIvIriCzcc_I',
    8: '1bWcK3inHF32AGe2RV0Qwfepy-OLoWIakffVnaWBmV6M',
}


names = set()

def sheet_statistics(episode_id: int):

    sheets = authenticate_sheets()
    result = sheets.values().get(spreadsheetId=SHEETS[episode_id], range=f'EP{episode_id}!A1:E10000').execute()
    values = result.get('values', [])

    dictionary = {}

    for line in values[1:]:

        name = 'EXTRA' if line[3].startswith('EXTRA') else line[3]

        if name not in dictionary:
            names.add(name)
            dictionary[name] = {}

        if line[2] in dictionary[name]:
            dictionary[name][line[2]] += 1
        else:
            dictionary[name][line[2]] = 1

    return dictionary


if __name__ == "__main__":

    for _ in SHEETS.keys():
        _i = sheet_statistics(_)

    characters = {'characters': list(names)}

    episodes = {}

    for _ in range(1, 9):

        ep = []
        dict = sheet_statistics(_)

        for character in names:

            try:
                recorded = 0 if 'Recorded' not in dict[character] else dict[character]['Recorded']
                not_recorded = 0 if 'Not recorded' not in dict[character] else dict[character]['Not recorded']
                cleaned_up = 0 if 'Cleaned up' not in dict[character] else dict[character]['Cleaned up']

                ep.append(f'{recorded}/{cleaned_up}/{recorded + cleaned_up + not_recorded}')

            except KeyError:
                ep.append(None)

        episodes[f'EP{_}'] = ep

    print(episodes.keys())
