from __future__ import division
from operator import itemgetter
import math


all_cards_ranked = {
    "aces" : 5,
    "kings" : 4, 
    "queens" : 3,
    "jacks" : 2,
    "10s" : 1,
    "9s" : 0
}

my_game = {
        "aces" : 1,
        "kings" : 1,
        "queens" : 0, 
        "jacks" : 3,
        "10s" : 0, 
        "9s" : 0
        }



def calculate_chances_call (num_players, fijo, call):
    chances = 0.0
    num_dice = (num_players - 1) * 5
    if not fijo and call[0] != "aces" and my_game[call[0]] + my_game["aces"] >= call[1]: #Verifying that the call isn't lower than what I have
        chances = 1
    elif fijo and my_game[call[0]] >= call[1]:
        chances = 1
    else:
        if call [0] == "aces" or fijo:   #If we are fijos then getting a card is same as ace
            for num in list(range(num_dice + 1))[call[1] - my_game[call[0]]:]:
                chances += combi(num_dice, num) * (1/6)**num * (5/6)**(num_dice - num) #This is the binomial formula of probability
        else : 
            for num in list(range(num_dice + 1))[call[1] - (my_game[call[0]] + my_game["aces"]):]:
                chances += combi(num_dice, call[1]) * (2/6)**call[1] * (4/6)**(num_dice - call[1]) #This is the binomial formula of probability
    return chances

def give_options (fijo, fijos, call):
    options = []
    if fijos and not fijo: 
        options.append([call[0], call[1] + 1])
    elif fijos and fijo: 
        for card in all_cards_ranked: 
            options.append([card, call[1] + 1])
    else: 
        if call[0] == "aces":
            options.append([call[0], call[1] + 1])
            for card in all_cards_ranked:
                options.append([card, call[1] * 2]) #here we are going to have aces twice becuase of the statement earlier. We can ignore this because the chances of the "wrong" aces winning are none so it will be ignored.
        else: 
            options.append(["aces", int(round((call[1]+1)/2 ,0))]) #include half of total for aces taking into account round up option. 
            for card in all_cards_ranked: 
                if all_cards_ranked[call[0]] < all_cards_ranked[card]: #take into account card rank
                    options.append([card, call[1]])
                else: 
                    options.append([card, call[1] + 1])
    
    return options

def give_chances_options (fijo, fijos, call, num_players): 
    chances = []
    options = give_options (fijo, fijos, call)
    for option in options:
        chances.append([option, calculate_chances_call(num_players, fijo, option)])
    chances.append(["dudo", 1.0 - calculate_chances_call(num_players, fijo, call)])
    return sorted(chances, key = itemgetter(1), reverse = True)
        

        
        
        
        
def combi (n, k):
    return math.factorial(n)/(math.factorial(k)*math.factorial(n-k))

print give_chances_options (False, False, ["jacks", 3], 2)
#print calculate_chances_call(2, False, ["jacks", 4])

