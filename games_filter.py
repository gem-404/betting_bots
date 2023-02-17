"""
Will filter those games that are over the 50th minute
and their score difference is more than or equal to 2.

Will also filter those games that are over the 70th minute
and their score difference is more than or equal to 1.

Will also filter those games that are over the 80th minute
and their score difference is more than or equal to 0.

The scores and the teams will be read from a txt file, live_games.txt
or will be read from a dictionary imported from the chromium_shabiki.py.

Structure of the dictionary

{
'SB-match__matchMinute': '90',
'SB-match__scoreInfo': '1\n0',
'SB-match__teamsInfo': 'Arsenal\nChelsea',
'SB-btnOddsGroup': '1.00\n1.00\n1.00'
}

This module will be used to place my bets in the near future...
"""
from chromium_shabiki import acquire_live_games


def getify_games(games_lst: list[dict[str, str]] | None):
    """Will get the list of games, and for each dict in the list,
    will get the minute, score difference and the teams"""

    scores, teams, minute = [], [], ''
    score_diff = 0

    assert games_lst is not None

    for games_dct in games_lst:
        scores = games_dct["SB-match__scoreInfo"].split("\n")
        teams = ' and '.join(games_dct["SB-match__teamsInfo"].split("\n"))
        minute = games_dct["SB-match__matchMinute"]
        odds = ' and '.join(games_dct["SB-btnOddsGroup"].split("\n"))

        score_diff = abs(int(scores[0]) - int(scores[1]))

        new_dct: dict = {
            "teams": teams,
            "score_diff": score_diff,
            "minute": minute,
            "odds": odds,
        }

        if any(map(str.isdigit, minute)):
            minute = int(minute.rstrip("'"))

            if score_diff >= 2 and minute >= 50:
                print()
                print(new_dct)

            elif score_diff >= 1 and minute >= 70:
                print()
                print(new_dct)

            elif score_diff >= 0 and minute >= 80:
                print()
                print(new_dct)

        else:
            # We are at half time, or maybe fulltime and the game is over
            # but still showing

            if score_diff >= 1:
                print()
                print("This game is a little tricky to bet on...")
                print("Can result in a draw")
                print(new_dct)
                print()

            elif score_diff >= 2:
                print()
                print(new_dct)
                print()


def main():
    """our main function"""
    games_lst: list[dict[str, str]] | None = acquire_live_games()

    getify_games(games_lst)


if __name__ == "__main__":
    main()
