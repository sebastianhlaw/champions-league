import numpy as np
import itertools

teams_x = [("Arsenal", "A", "UK"),
           ("Naples", "B", "IT"),
           ("Barcelona", "C", "ES"),
           ("Athletico", "D", "ES"),
           ("Monaco", "E", "FR"),
           ("Dortmund", "F", "DE"),
           ("Leicester", "G", "UK"),
           ("Juventus", "H", "IT")]

teams_y = [("PSG", "A", "FR"),
           ("Benfica", "B", "PT"),
           ("Man City", "C", "UK"),
           ("Bayern", "D", "DE"),
           ("Leverkusen", "E", "DE"),
           ("Real", "F", "ES"),
           ("Porto", "G", "PT"),
           ("Sevilla", "H", "ES")]

dimension = 4

print("dimension", dimension)
matches = [m for m in range(dimension)]
teams_x = teams_x[:dimension]
teams_y = teams_y[:dimension]

blocked_matches = np.empty((dimension, dimension)).astype(bool)
permitted_match_tally = np.zeros((dimension, dimension)).astype(int)
invalid_last_tally = np.zeros((dimension, dimension)).astype(int)
invalid_combo_tally = np.zeros((dimension, dimension)).astype(int)

for i, iTeam in enumerate(teams_x):
    for j, jTeam in enumerate(teams_y):
        if iTeam[1] == jTeam[1] or iTeam[2] == jTeam[2]:
            blocked_matches[i, j] = True
        else:
            blocked_matches[i, j] = False

perm_x = [i for i in itertools.permutations(range(dimension))]
perm_y = [i for i in itertools.permutations(range(dimension))]
permutations = len(perm_x) * len(perm_x)
print("permutations (total sets)", permutations)

permitted_matches = 0
ticker = 0

valid_set_tally = 0
avoided_set_tally = 0
invalid_set_tally = 0

for it_x in perm_x:
    if dimension == 8:
        ticker += 1
        print(ticker, "of", len(perm_x))
    for it_y in perm_y:
        block = False
        for m in matches[:dimension-1]:
            if blocked_matches[it_x[m], it_y[m]]:
                # invalid_combo_tally[it_x[m], it_y[m]] += 1
                block = True
        if block:
            avoided_set_tally += 1
        if not block:
            m = dimension - 1
            if blocked_matches[it_x[m], it_y[m]]:
                # invalid_combo_tally[it_x[m], it_y[m]] += 1
                invalid_last_tally[it_x[m], it_y[m]] += 1
                block = True
                invalid_set_tally += 1
                print(it_x, it_y)
        if not block:
            valid_set_tally += 1
            for m in matches:
                permitted_match_tally[it_x[m], it_y[m]] += 1
                permitted_matches += 1

print("permitted_matches", permitted_matches)
print("- valid_set_tally (no blockages)", valid_set_tally)
print("- avoided_set_tally", avoided_set_tally)
print("- invalid_set_tally (blocked @ last point only)", invalid_set_tally)

print("permitted_match_tally", np.sum(permitted_match_tally), "\n", permitted_match_tally)
print(np.sum(permitted_match_tally, axis=0), np.sum(permitted_match_tally, axis=1))
probabilities = permitted_match_tally / (permitted_matches / dimension)

print("probabilities\n", probabilities)
print(np.sum(probabilities, axis=0), np.sum(probabilities, axis=1))

# print("invalid_combo_tally", np.sum(invalid_combo_tally), "\n", invalid_combo_tally)
# print(np.sum(invalid_combo_tally, axis=0), np.sum(invalid_combo_tally, axis=1))

print("invalid_last_tally", np.sum(invalid_last_tally), "\n", invalid_last_tally)
print(np.sum(invalid_last_tally, axis=0), np.sum(invalid_last_tally, axis=1))

print("answer:", np.sum(invalid_last_tally) / (np.sum(permitted_match_tally) + np.sum(invalid_last_tally)))
