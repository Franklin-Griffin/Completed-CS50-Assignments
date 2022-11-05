dlimit = 20

def initial_state():
    """
    Returns starting state.
    """
    return ((1, 1,), (1, 1))


def actions(hands, player):
    """
    Returns set of all possible actions [new config] available
    """
    actions = set()
    opp = 1 if player == 0 else 0
    for hand in range(len(hands[player])):
        if hands[player][hand] != 0:
            for opphand in range(len(hands[opp])):
                if hands[opp][opphand] != 0:
                    action = list(map(list, hands))
                    action[opp][opphand] += action[player][hand]
                    if action[opp][opphand] > 4:
                        action[opp][opphand] = 0
                    actions.add(tuple(map(tuple, action)))
    return actions


def winner(hands):
    if hands[0][0] == 0 and hands[0][1] == 0:
        return -1
    elif hands[1][0] == 0 and hands[1][1] == 0:
        return 1
    return None


def minimax(hands):
    """
    Returns the optimal action for the current player on the hands.
    """
    x = winner(hands)
    if x:
        return x

    # start with max player
    bestV = -2
    bestActions = []
    for a in actions(hands, 0):
        v = MinValue(a, 1)
        if v and v[0] > bestV:
            bestV = v[0]
            bestActions = [a] + v[1]
        if v == 1:
            return (bestV, bestActions)
    return (bestV, bestActions)


def MaxValue(hands, depth):
    x = winner(hands)
    if x:
        return (x, [])
    if depth == dlimit:
        return None
        
    v = -2
    bestAction = []
    for action in actions(hands, 0):
        x = MinValue(action, depth+1)
        if x and x[0] > v:
            v = x[0]
            bestAction = [action] + x[1]
        if v == 1:
            return (v, bestAction)
    return (v, bestAction)


def MinValue(hands, depth):
    x = winner(hands)
    if x:
        return (x, [])
    if depth == dlimit:
        return None

    v = 2
    bestAction = []
    for action in actions(hands, 1):
        x = MaxValue(action, depth+1)
        if x and x[0] < v:
            v = x[0]
            bestAction = [action] + x[1]
        if v == -1:
            return (v, bestAction)
    return (v, bestAction)


x = minimax(((int(input()),int(input())),(int(input()),int(input()))))
print(x[0])
print(x[1])