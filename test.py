from game import Game, HumanPlayer, DumbComputerPlayer

#p = HumanPlayer()
p = DumbComputerPlayer(slow=True)

g = Game(p, display=True)
g.play()

print(p._score_history)
for state in p._state_history:
    print(state)