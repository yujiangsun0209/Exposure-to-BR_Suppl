
def get_round_robin_pairs(players_id):
    """
    Round Robin tournament. An infinite generator that returns a list of pairs.
    The number of rounds that respects the principle of the round robin tournament is equal to len(players_is) - 1.
    After this number of rounds, the loop restarts.
    :param players: list of id_in_subsession
    :return: a generator
    """
    left = players_id[: len(players_id) // 2]
    right = players_id[len(players_id) // 2:]

    while True:
        yield list(map(list, list(zip(left, right))))
        right.append(left.pop())
        left.insert(1, right.pop(0))


def get_minutes_from_seconds(seconds):
    m, s = divmod(seconds, 60)
    return f"{m:02}:{s:02}"