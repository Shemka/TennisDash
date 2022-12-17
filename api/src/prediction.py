# we use a pseudorandom number generator
from random import random


# probability of a player winning a big point
# serves as an auxiliary function and returns new probabilities if the point is defined as a large point
def get_big_point_prob(server):
    if server == p1:
        return p1_big_point
    elif server == p2:
        return p2_big_point
    else:
        print("Error")


# auxiliary function, which defines and associated function getBigPointProbability
def is_big_point(server_points, returner_points, tiebreak):
    server_next_point = server_points
    if tiebreak:
        if server_next_point >= 6 and abs(server_next_point - returner_points) >= 1:
            print("set point")
            return True

    elif server_next_point >= 3 and (server_next_point - returner_points) >= 1:
        print("game point")
        return True


# takes the player's score string and returns the tennis score agreement
# functions as a scoreboard
def get_score(points_server, points_returner, server_games, returner_games, completed_kits, tiebreaker):
    display_server = '0'
    display_returner = '0'

    if not tiebreaker:
        in_game = ['15', '30', '40']
        if points_server == 0:
            display_server = '0'
        elif 0 < points_server < 4:
            display_server = in_game[points_server - 1]
        elif points_server >= 4:
            display_server = 'D'

        if points_returner == 0:
            display_returner = '0'
        elif 0 < points_returner < 4:
            display_returner = in_game[points_returner - 1]
        elif points_returner >= 4:
            display_returner = 'D'

        if (points_server >= 4 and points_returner < 4) or (points_server < 4 and points_returner >= 4):
            display_server = 'D'
            display_returner = 'D'

        if points_server > points_returner:
            if display_server == 'D':
                display_server = 'A'
        elif points_returner > points_server:
            if display_server == 'D':
                display_returner = 'A'

        if (display_server == 'A' and display_returner == 'A') or (display_server == '40' and display_returner == '40'):
            display_server = 'D'
            display_returner = 'D'
        if display_server == 'A' and display_returner == '40':
            display_server = 'A'
            display_returner = 'D'
        if display_server == '40' and display_returner == 'A':
            display_server = 'D'
            display_returner = 'A'
    else:
        display_server = str(points_server)
        display_returner = str(points_returner)

    if len(completed_kits) == 0:
        print(f"{display_server}-{display_returner}|[{str(server_games)}-{str(returner_games)}]")

    else:
        completed = ""
        for sets in completed_kits:
            completed = f"{completed} {str(sets[0])}:{str(sets[1])}"
        print(f"{display_server}-{display_returner}|{str(completed)}[{str(server_games)}:{str(returner_games)}]")


# after each game print out winner
# Increases the points for the server and the returner and keeps track of large points
def player_serve(server, returner, server_prob, match_play, s, server_points_match,
                 returner_points_match, server_games, returner_games, server_points_game, returner_points_game,
                 completed_kits):
    if is_big_point(server_points_game, returner_points_game, False):
        server_prob = get_big_point_prob(server)
    if random() < server_prob:
        print(f"{server} ", end="")
        get_score(server_points_game, returner_points_game, server_games, returner_games, completed_kits, False)
        server_points_game += 1
        server_points_match += 1
    else:
        print(f"{server} ", end="")
        get_score(server_points_game, returner_points_game, server_games, returner_games, completed_kits, False)
        returner_points_game += 1
        returner_points_match += 1
    if max(server_points_game, returner_points_game) >= 4 and abs(server_points_game - returner_points_game) > 1:
        print("\t", f"{server}:", f"{str(server_points_game)},", f"{returner}:", returner_points_game, end="")

        if server_points_game > returner_points_game:
            server_games += 1
            print()
        else:
            returner_games += 1
            print(f" -- {returner}", "broke")
        match_play += 1
        return server_games, returner_games, match_play, s, server_points_match, returner_points_match, \
               server_points_game, returner_points_game

    return server_games, returner_games, match_play, s, server_points_match, returner_points_match, server_points_game, \
           returner_points_game


# play a set
# tracks games in the set and determines if the set is going to a tie-break
def simulate_set(var_a, var_b, match_play, s, points_match_1, points_match_2, completed_kits):
    s += 1
    games_set_1, games_set_2 = 0, 0
    while (max(games_set_1, games_set_2) < 6 or abs(
            games_set_1 - games_set_2) < 2) and games_set_1 + games_set_2 < 12:  # Conditions to play another Game in
        # this Set
        points_game1, points_game2 = 0, 0
        # player 1 serves
        while match_play % 2 == 0:
            games_set_1, games_set_2, match_play, s, points_match_1, points_match_2, points_game1, points_game2 = player_serve(
                p1, p2, var_a, match_play, s, points_match_1, points_match_2, games_set_1, games_set_2, points_game1,
                points_game2,
                completed_kits)
        points_game1, points_game2 = 0, 0
        # player 2 serves, but we also include logic to complete the set
        while match_play % 2 == 1 and (
                max(games_set_1, games_set_2) < 6 or abs(
            games_set_1 - games_set_2) < 2) and games_set_1 + games_set_2 < 12:
            games_set_2, games_set_1, match_play, s, points_match_2, points_match_1, points_game2, points_game1 = player_serve(
                p2,
                p1,
                var_b,
                match_play,
                s,
                points_match_2,
                points_match_1,
                games_set_2,
                games_set_1,
                points_game2,
                points_game1,
                completed_kits)
    # at 6 games all go to a tie-break.
    if games_set_1 == 6 and games_set_2 == 6:
        print("Set", s, "is 6-6 and going to a Tiebreaker.")

    return games_set_1, games_set_2, match_play, s, points_match_1, points_match_2


# play a tiebreak
def simulate_tiebreaker(player1, player2, var_a, var_b, match_play, points_match_1, points_match_2, completed_kits):
    points_tie1, points_tie2 = 0, 0
    while max(points_tie1, points_tie2) < 7 or abs(points_tie1 - points_tie2) < 2:
        # player 1 will server first
        if match_play % 2 == 0:
            while (points_tie1 + points_tie2) % 4 in [0, 3]:
                server_prob = var_a
                if is_big_point(points_tie1, points_tie2, True):
                    server_prob = get_big_point_prob(player1)
                if random() < server_prob:
                    get_score(points_tie1, points_tie2, 6, 6, completed_kits, True)
                    points_tie1 += 1
                    points_match_1 += 1
                else:
                    get_score(points_tie1, points_tie2, 6, 6, completed_kits, True)
                    points_tie2 += 1
                    points_match_2 += 1
                if max(points_tie1, points_tie2) >= 7 and abs(points_tie1 - points_tie2) > 1:
                    print("\t", f"{p1}:", f"{points_tie1},", f"{p2}:", points_tie2)
                    match_play += 1
                    break
            while (max(points_tie1, points_tie2) < 7 or abs(points_tie1 - points_tie2) < 2) and (
                    points_tie1 + points_tie2) % 4 in [1, 2]:
                # Conditions for continuation Tay-break (race to 7, win 2) and Player 2 serves (points 4N+1 and 4N+2)
                server_prob = var_b
                if is_big_point(points_tie2, points_tie1, True):
                    server_prob = get_big_point_prob(player2)
                if random() < server_prob:
                    get_score(points_tie1, points_tie2, 6, 6, completed_kits, True)
                    points_tie2 += 1
                    points_match_2 += 1
                else:
                    get_score(points_tie1, points_tie2, 6, 6, completed_kits, True)
                    points_tie1 += 1
                    points_match_1 += 1
                if max(points_tie1, points_tie2) >= 7 and abs(points_tie1 - points_tie2) > 1:
                    print("\t", f"{p1}:", f"{points_tie1},", f"{p2}:", points_tie2)
                    break

        # player 2 will server first
        if match_play % 2 == 1:
            while (points_tie1 + points_tie2) % 4 in [1, 2]:
                server_prob = var_a
                if is_big_point(points_tie1, points_tie2, True):
                    server_prob = get_big_point_prob(player1)
                if random() < server_prob:
                    # print(player1+" ", end = "")
                    get_score(points_tie1, points_tie2, 6, 6, completed_kits, True)
                    points_tie1 += 1
                    points_match_1 += 1
                else:
                    get_score(points_tie1, points_tie2, 6, 6, completed_kits, True)
                    points_tie2 += 1
                    points_match_2 += 1
                if max(points_tie1, points_tie2) >= 7 and abs(points_tie1 - points_tie2) > 1:
                    print("\t", f"{p1}:", f"{points_tie1},", f"{p2}:", points_tie2)
                    break
            while (max(points_tie2, points_tie1) < 7 or abs(points_tie1 - points_tie2) < 2) and (
                    points_tie1 + points_tie2) % 4 in [0,
                                                       3]:  # Conditions to continue Tiebreaker (race to 7, win by 2)
                # and Player 2 serves (points 4N and 4N+3)
                server_prob = var_b
                if is_big_point(points_tie2, points_tie1, True):
                    server_prob = get_big_point_prob(player2)
                if random() < server_prob:
                    get_score(points_tie1, points_tie2, 6, 6, completed_kits, True)
                    points_tie2 += 1
                    points_match_2 += 1
                else:
                    get_score(points_tie1, points_tie2, 6, 6, completed_kits, True)
                    points_tie1 += 1
                    points_match_1 += 1
                if max(points_tie1, points_tie2) >= 7 and abs(points_tie1 - points_tie2) > 1:
                    print("\t", f"{p1}:", f"{points_tie1},", f"{p2}:", points_tie2)
                    break
    match_play += 1
    return points_tie1, points_tie2, match_play, points_match_1, points_match_2


# useful updates
# displays the current score as the referee would have announced the score at the end of the set
def print_set_match_summary(p_1, p_2, games_set_1, games_set_2, s, points_tie1, points_tie2, sets_match_1,
                            sets_match_2):
    if games_set_1 > games_set_2:
        sets_match_1 += 1
        print(p_1.upper(), "wins Set", f"{str(s)}:", games_set_1, "games to", f"{str(games_set_2)}.")

    elif games_set_2 > games_set_1:
        sets_match_2 += 1
        print(p_2.upper(), "wins Set", f"{str(s)}:", games_set_2, "games to", f"{str(games_set_1)}.")


    elif games_set_1 == games_set_2:
        if points_tie1 > points_tie2:
            sets_match_1 += 1
            print(p_1.upper(), "wins Set", f"{str(s)}: 7 games to 6 ({str(points_tie1)}-{str(points_tie2)}).")

        else:
            sets_match_2 += 1
            print(p_2.upper(), "wins Set", f"{str(s)}: 7 games to 6 ({str(points_tie2)}-{str(points_tie1)}).")

    print("After", s, "Sets:", p_1, f"{str(sets_match_1)},", p_2, str(sets_match_2) + ".\n")

    return sets_match_1, sets_match_2


# outputs the final winner and the number of sets won
def points_match_summary(p_1, p_2, sets_match_1, sets_match_2):
    if sets_match_1 == 3:
        print(p_1.upper(), f"({str(a)})", "beat", p_2, f"({str(b)}) by", sets_match_1, "Sets to",
              f"{str(sets_match_2)}.")

        winner.append(p_1)
    else:
        print(p_2.upper(), f"({str(b)})", "beat", p_1, f"({str(a)}) by", sets_match_2, "Sets to",
              f"{str(sets_match_1)}.")

        winner.append(p_2)


# this control flow is one simulation
winner = []
completed_sets = []
S = 0
games_match = 0

# For example, setsMatch1 are the sets won by player1 and
# setsMatch2 are sets won by player2
points_match1, points_match2 = 0, 0
sets_match1, sets_match2 = 0, 0
pointsTie1, pointsTie2 = 0, 0
pointsGame1, pointsGame2 = 0, 0

# initialize the first and second player
# a is ps1 and b is ps2
# p1_big_point and p2_big_point are the probabilities
# of winning p1 and p2 on the big point, respectively.
p1 = "Player 1"
p2 = "Player 2"
a = 0.64
b = 0.62
p1_big_point = 0.70
p2_big_point = 0.68

while S < 5 and max(sets_match1, sets_match2) < 3:
    games_set1, games_set2, games_match, S, points_match1, points_match2 = simulate_set(a, b, games_match, S,
                                                                                        points_match1, points_match2,
                                                                                        completed_sets)
    print()
    if games_set1 == 6 and games_set2 == 6:
        pointsTie1, pointsTie2, games_match, points_match1, points_match2 = simulate_tiebreaker(p1, p2, a, b,
                                                                                                games_match,
                                                                                                points_match1,
                                                                                                points_match2,
                                                                                                completed_sets)

    sets_match1, sets_match2 = print_set_match_summary(p1, p2, games_set1, games_set2,
                                                       S, pointsTie1, pointsTie2,
                                                       sets_match1, sets_match2)

    if games_set1 == 6 and games_set2 == 6:
        if pointsTie1 > pointsTie2:
            completed_sets.append([games_set1 + 1, games_set2])
        else:
            completed_sets.append([games_set1, games_set2 + 1])
    else:
        completed_sets.append([games_set1, games_set2])

points_match_summary(p1, p2, sets_match1, sets_match2)
