"""
Gra Black Jack na podstawie video Ala Sweigarta: Calm Programming - Blackjack Game:
https://www.youtube.com/watch?v=tu0lnL0EbGE&ab_channel=AlSweigart
"""

import random, sys

# przypisanie symboli do kart:
HEARTS = chr(9829)
DIAMONDS = chr(9830)
SPADES = chr(9824)
CLUBS = chr(9827)

BACKSIDE = 'backside'


def main():
    print('''
    
    Gra Black Jack
    
    Zasady:
        Zadaniem gracza jest uzyskać jak najbliżej (ale nie więcej niż) 21 punktów. 
        Król, Dama i Walet są warte 10 punktów. As 1 lub 11.
        Karty od 2 do 10 są warte tyle, ile wskazuje ich numer.
        Wybierz H (hit), aby dobrać kartę. S (stand), aby nie dobierać kart.
        Przy pierwszym ruchu możesz dodatkowo zwiększyć (podwoić) stawkę zakładu: D (double down), 
        jednak wtedy możesz dobrać już tylko jedną kartę.
        W przypadku remisu stawka zakładu jest zwracana do gracza.
        Krupier nie dobiera więcej kart gdy osiągnie 16 punktów.
        
        ''')

    money = 5000
    while True:
        # Sprawdzenie czy gracz ma pieniądze aby postawić:
        if money <= 0:
            print("Nie masz już środków, aby postawić!")
            print("Dobrze, że nie graliśmy na prawdziwe pieniądze.")
            print("Dziękuję za grę!")
            sys.exit()

        # Postawienie pieniędzy w danej rundzie:
        print("Twoje pieniądze: ", money)
        bet = get_bet(money)

        # Rozdanie graczowi i krupierowi po 2 karty z talii:
        deck = get_deck()
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]

        # Wybór gracza:
        print("Twój zakład: ", bet)
        while True:
            display_hands(player_hand, dealer_hand, False)
            print()

            # Sprawdzenie czy gracz przekroczył 21:
            if get_hand_value(player_hand) > 21:
                break

            # Pobranie ruchu od gracza - H, S lub D:
            move = get_move(player_hand, money - bet)

            # Rozegranie wyboru gracza:
            if move == 'D':
                additional_bet = get_bet(min(bet, (money-bet)))
                bet += additional_bet
                print(f"Stawka podniesiona o {additional_bet}.")
                print("Zakład: ", bet)

            if move in ('H', 'D'):
                new_card = deck.pop()
                rank, suit = new_card
                print(f"Dobrałeś/aś kartę: {rank}{suit}")
                player_hand.append(new_card)

                if get_hand_value(player_hand) > 21:
                    continue

            if move in ('S', 'D'):
                break

        # Rozegranie wyboru krupiera:
        if get_hand_value(player_hand) <= 21:
            while get_hand_value(dealer_hand) < 17:  # jeśli krupier ma 16 lub mniej pkt dobiera kartę
                print("Krupier dobiera kartę...")
                dealer_hand.append(deck.pop())
                display_hands(player_hand, dealer_hand, False)

                if get_hand_value(dealer_hand) > 21:  # krupier przekroczył 21:
                    break
                input("Wciśnij ENTER aby kontynuować...")
                print("\n\n")

        # Pokazanie kart:
        display_hands(player_hand, dealer_hand, True)
        player_value = get_hand_value(player_hand)
        dealer_value = get_hand_value(dealer_hand)

        # Rozegranie wygranej, przegranej lub remisu:
        if dealer_value > 21:
            print(f"Krupier przegrał! Wygrywasz {bet}!")
            money += bet
        elif (player_value > 21) or (player_value < dealer_value):
            print("Przegrałeś/aś!")
            money -= bet
        elif player_value > dealer_value:
            print(f"Wygrywasz {bet}!")
            money += bet
        elif player_value == dealer_value:
            print("Remis! Twój zakład zostaje zwrócony.")

        input("Wciśnij ENTER aby kontynuować...")
        print("\n\n")


def get_bet(max_bet):
    while True:
        print(f"Ile chcesz postawić? Od 1 do {max_bet}. \nWpisz 'QUIT', aby opuścić grę.")
        bet = input('> ').upper().strip()
        if bet == 'QUIT':
            print("Dziękuję za grę!")
            sys.exit()
        if not bet.isdecimal():
            continue

        bet = int(bet)
        if 1 <= bet <= max_bet:
            return bet


def get_deck():
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))
        for rank in ("K", "Q", "J", "A"):
            deck.append((rank, suit))
    random.shuffle(deck)
    return deck


def display_hands(player_hand, dealer_hand, show_dealer_hand):
    print()
    # Pokazanie kart krupiera:
    if show_dealer_hand:
        print('KRUPIER: ', get_hand_value(dealer_hand))
        display_cards(dealer_hand)
    else:
        print('KRUPIER: ???')
        display_cards([BACKSIDE] + dealer_hand[1:])

    # Pokazanie kart gracza:
    print('GRACZ: ', get_hand_value(player_hand))
    display_cards(player_hand)


def get_hand_value(cards):
    value = 0
    number_of_Aces = 0

    # Dodanie wartości kart (z wyłączeniem Asów):
    for card in cards:
        rank = card[0]
        if rank == 'A':
            number_of_Aces += 1
        elif rank in ('K', 'Q', 'J'):
            value += 10
        else:
            value += int(rank)

    # Dodanie wartości Asów (1 lub 11 pkt):
    value += number_of_Aces
    for i in range(number_of_Aces):
        if value + 10 <= 21:
            value += 10

    return value


def display_cards(cards):
    rows = ['', '', '', '', '']

    for i, card in enumerate(cards):
        rows[0] += ' ___ '
        if card == BACKSIDE:
            rows[1] += '|## |'
            rows[2] += '|###|'
            rows[3] += '|_##|'
        else:
            rank, suit = card
            rows[1] += f'|{rank.ljust(2)} |'
            rows[2] += f'| {suit} |'
            rows[3] += f'|_{rank.rjust(2, "_")}|'

    for row in rows:
        print(row)


def get_move(player_hand, money):
    while True:
        moves = ['(H)it', '(S)tand']
        # Gracz może też zwiększyć stawkę = D tylko przy pierwszym ruchu (= kiedy ma dokładnie 2 karty):
        if len(player_hand) == 2 and money > 0:
            moves.append('(D)ouble down')

        # Pobranie ruchu od gracza (H, S lub D) i zwrócenie go:
        move_prompt = ', '.join(moves) + ' > '
        move = input(move_prompt).upper()
        if move in ('H', 'S'):
            return move
        if move == 'D' and '(D)ouble down' in moves:
            return move


if __name__ == '__main__':
    main()