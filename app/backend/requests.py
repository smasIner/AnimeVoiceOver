import pandas as pd

from .auth import authenticate_sheets

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

EPISODES_NUMBER = len(SHEETS.keys())

google_sheets_api = authenticate_sheets()


def get_anime_dataframe() -> pd.DataFrame:
    """
    Returns the dataframe where the statistics
    of voice acting by episode are collected.
    """
    names = set()

    def sheet_statistics(episode_id: int) -> dict:
        """
        Returns statistics for the episode.

        Args:
            episode_id: int, number of episode
        """
        result = google_sheets_api.values().get(
            spreadsheetId=SHEETS[episode_id],
            range=f'EP{episode_id}!A:E',
        ).execute()

        values = result.get('values', [])

        dictionary = {}

        for line in values[1:]:
            name = 'EXTRA' if line[3].startswith('EXTRA') else line[3]

            if name not in dictionary:
                dictionary[name] = {}

            if line[2] in dictionary[name]:
                dictionary[name][line[2]] += 1
            else:
                dictionary[name][line[2]] = 1

        return dictionary

    def create_table() -> pd.DataFrame:
        '''
        Compiles a table with statistics for all episodes.
        Returns the pandas Dataframe.
        '''

        table = {}

        for key in SHEETS.keys():
            names.update(sheet_statistics(key))

        characters = {'characters': list(names) + ['']}

        episodes = {}

        for i in range(1, EPISODES_NUMBER + 1):

            ep = []
            dict = sheet_statistics(i)

            total_recorded = 0
            total_not_recorded = 0
            total_cleaned_up = 0

            for character in names:

                try:

                    recorded = 0 if 'Recorded' not in dict[character] \
                        else dict[character]['Recorded']

                    not_recorded = 0 if 'Not recorded' not in dict[character] \
                        else dict[character]['Not recorded']

                    cleaned_up = 0 if 'Cleaned up' not in dict[character] \
                        else dict[character]['Cleaned up']

                    total_recorded += recorded
                    total_not_recorded += not_recorded
                    total_cleaned_up += cleaned_up

                    stat = (recorded, cleaned_up, recorded +
                            cleaned_up + not_recorded)
                    ep.append(stat)

                except KeyError:
                    ep.append(None)

            total_stat = (total_recorded, total_cleaned_up,
                          total_recorded + total_cleaned_up +
                          total_not_recorded)
            ep.append(total_stat)

            episodes[f'EP{i}'] = ep

        total_episodes = []

        for idx in range(len(names)):

            total_rep = 0

            for episode_id in episodes:
                try:
                    if not (episodes[episode_id][idx] is None):
                        total_rep += episodes[episode_id][idx][2]
                except AttributeError:
                    pass

            total_episodes.append(total_rep)

        total_episodes.append(sum(total_episodes))

        links = [f'https://antifandom.com/you-zitsu/wiki/\
                 {name.replace(" ", "%20")}' for name in names] + ['']

        table.update(characters)
        table.update(episodes)
        table.update({'total': total_episodes})
        table.update({'role': links})

        df = pd.DataFrame(table)
        df = df.sort_values(by=['total'], ignore_index=True, ascending=[False])

        return df

    return create_table()
