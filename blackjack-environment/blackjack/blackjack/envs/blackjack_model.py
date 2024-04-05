import numpy as np
import copy

#deck = np.array(["AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "TH", "JH", "QH", "KH",
#                 "AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "TD", "JD", "QD", "KD",
#                 "AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "TC", "JC", "QC", "KC",
#                 "AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "TS", "JS", "QS", "KS"])

class BlackjackState:
    def __init__(self):
        """0 = in deck, -1 = discarded, 1 = in dealer's hand, 7 = hidden card in dealer's hand, 2 = in player1's hand"""
        self._round = 0
        self._cards = np.zeros(52)
        self._betting = True
        self._bet = 0
        self._wallet = 500
        self._p1turn = False
        self._canDouble = False
       
    def reset(self):
        self._round += 1
        self.compare()
        self.discard()
        self._bet = 0
        self._betting = True
        self._p1turn = False
        self._canDouble = False

    def deal(self):
        self._betting = False
        self.random_draw(7)
        self.random_draw(2)
        self.random_draw(1)
        self.random_draw(2)
        self._p1turn = True
        self._canDouble = True
        return

    def random_draw(self, player, seed=None):
        if seed is not None:
            np.random.seed(seed)
        random_card = np.random.randint(52)
        not_drawn = True
        while not_drawn:
            if self._cards[random_card] == 0:
                self._cards[random_card] = player
                not_drawn = False
            else:
                random_card = np.random.randint(52)
        return self._cards


    def turn(self, action):
        """action:
           0: Stand
           1: Hit
           2: Double down
           3: bet 10
           4: bet 25
           5: bet 50"""
        if action == 0:
            self._p1turn = False
            self.dealer_turn()
            self.reset()
        if action == 1:
            self.random_draw(2)
            self._canDouble = False
            hand = self.obs_to_hand(2)
            if self.evaluate_hand(hand) >= 21:
                self._p1turn = False
                self.dealer_turn()
                self.reset()
        if action == 2:
            self._bet = self._bet * 2
            self.random_draw(2)
            self._p1turn = False
            self.dealer_turn()
            self.reset()
        if action == 3:
            self._bet = 10
            self.deal()
        if action == 4:
            self._bet = 25
            self.deal()
        if action == 5:
            self._bet = 50
            self.deal()
        return

    @property
    def observation(self):
        cards = copy.deepcopy(self._cards)
        for i in cards:
            if i == 7:
                i = 0
        betting = 0
        p1turn = 0
        canDouble = 0
        if self._betting == True: betting = 1
        if self._p1turn == True: p1turn = 1
        if self._canDouble == True: canDouble = 1
        other = np.array([self._round,self._wallet,self._bet,betting, p1turn, canDouble])
        obs = np.append(cards, other)
        return obs 

    @observation.setter
    def observation(self, value):
        self._cards = value[:52]
        self._round = value[52]
        self._wallet = value[53]
        self._bet = value[54]
        if value[55] == 0: self._betting = False
        else: self._betting = True
        if value[56] == 0: self._p1turn = False
        else: self._p1turn = True
        if value[57] == 0: self._canDouble = False
        else: self._canDouble = True
        return

    def evaluate_hand(self, hand):
        score = 0
        for card in hand:
            if card == 'A':
                score += 11
            elif card == 'J' or card == 'Q' or card == 'K':
                score += 10
            else:
                score += card
        if score > 21:
            for card in hand:
                if card == 'A': score -= 10
                if score <= 21: break
        return score

    def compare(self):
        d_score = self.evaluate_hand(self.obs_to_hand(1))
        p_score = self.evaluate_hand(self.obs_to_hand(2))
        if p_score > 21:
            self._wallet -= self._bet
        elif d_score > 21:
            self._wallet += self._bet
        elif p_score > d_score:
            if p_score == 21:
                self._wallet += (1.5 * self._bet)
            else:
                self._wallet += self._bet
        elif p_score < d_score:
            self._wallet -= self._bet
        return


    def dealer_turn(self):
        index = 0
        for card in self._cards:
            if card == 7:
                self._cards[index] = 1
            index += 1
        d = self.evaluate_hand(self.obs_to_hand(1))
        while d < 17:
            self.random_draw(1)
            d = self.evaluate_hand(self.obs_to_hand(1))
        return

    def discard(self):
        index = 0
        undealt = 0
        for card in self._cards:
            if card != 0:
                self._cards[index] = -1
            else:
                undealt += 1
            index += 1
        if undealt < 10:
            self._cards = np.zeros(52)
        return

    def obs_to_hand(self, player):
        index = 0
        hand = []
        for i in self._cards:
            if i == player:
                value = ((index % 13) + 1)
                if value == 1:
                    label = 'A'
                elif value == 11:
                    label = 'J'
                elif value == 12:
                    label = 'Q'
                elif value == 13:
                    label = 'K'
                else: label = value
                hand.append(label)
            index += 1
        return hand

    def __str__(self):
        hand = self.obs_to_hand(1)
        s = f"| Dealer Total: {self.evaluate_hand(hand)} "
        if self.evaluate_hand(hand) > 21:
            s += "| BUST!"
        s += "\n"
        for i in self._cards:
            if i == 7:
                s += "| ? "
        for card in hand:
            s += f"| {card} "
        s += "\n|\n"
        hand = self.obs_to_hand(2)
        for card in hand:
            s += f"| {card} "
        s += f"\n| Player Total: {self.evaluate_hand(hand)}"
        if self.evaluate_hand(hand) > 21:
            s += "| BUST!"
        s += f"\n| Wallet: {self._wallet}\n"
        return s



if __name__ == "__main__":
    s = BlackjackState()
    print(s)
    s.turn(3)
    print(s)
    s.turn(1)
    print(s)
    s.turn(0)
    print(s)


"""action:
           0: Stand
           1: Hit
           2: Double down
           3: bet 10
           4: bet 25
           5: bet 50"""
class BlackjackModel:
    def ACTIONS(state):
        actions = []
        if state._betting:
            actions = [3,4,5]
        elif state._p1turn:
            actions = [0,1]
            if state._canDouble:
                actions.append(2)
        return actions
            

    def RESULT(state, action):
        state1 = copy.deepcopy(state)
        state1.turn(action)
        return state1

    def GOAL_TEST(state):
        if state._round == 10:
            return True
        return False

    def STEP_COST(state, action, state1):
        if state1._p1turn:
            return 0
        if state._p1turn and not state1._p1turn:
            return state1._wallet - state._wallet
            

    def HEURISTIC(state):
        estimated_cost = 0.0
        return estimated_cost

if __name__ == "__main__":
    state = BlackjackState()
    actions = BlackjackModel.ACTIONS(state)
    print(actions)

    print()
    state = BlackjackState()
    print(state)
    state1 = BlackjackModel.RESULT(state, 3)
    print(state1)
    actions = BlackjackModel.ACTIONS(state1)
    print(actions)
    state2 = BlackjackModel.RESULT(state1, 0)
    print(state2)
    actions = BlackjackModel.ACTIONS(state2)
    print(actions)

