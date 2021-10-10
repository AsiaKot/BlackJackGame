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


# chr() returns a character (str) from an integer (represents unicode code point of the character)
# win > tablica znaków > serce = U+2665
# cmd > python > int(0x2665) > 9829


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
        while True:  # zapętlenie aż gracz nie spasuje lub nie przekroczy 21:
            display_hands(player_hand, dealer_hand, False)
            print()

            # Sprawdzenie czy gracz przekroczył 21:
            if get_hand_value(player_hand) > 21:
                break

            # Pobranie ruchu od gracza - H, S lub D:
            move = get_move(player_hand, money - bet)

            # Rozegranie wyboru gracza:
            if move == 'D':  # gracz zwiększył stawkę
                additional_bet = get_bet(min(bet, (money - bet)))  # min() zwraca najmniejszą wartość
                bet += additional_bet
                print(f"Stawka podniesiona o {additional_bet}.")
                print("Zakład: ", bet)

            if move in ('H', 'D'):  # gracz zwiększył stawkę i dobiera kolejną kartę
                new_card = deck.pop()
                rank, suit = new_card
                print(f"Dobrałeś/aś kartę: {rank}{suit}")
                player_hand.append(new_card)

                if get_hand_value(player_hand) > 21:  # gracz przekroczył 21:
                    continue

            if move in ('S', 'D'):  # gracz zwiększył stawkę i nie dobiera kolejnej karty
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


def get_bet(max_bet):  # Zapytanie gracza ile chce postawić w tej rundzie:
    while True:  # pytaj dopóki gracz nie wskaże poprawnej wartości
        print(f"Ile chcesz postawić? Od 1 do {max_bet}. \nWpisz 'QUIT', aby opuścić grę.")
        bet = input('> ').upper().strip()
        if bet == 'QUIT':
            print("Dziękuję za grę!")
            sys.exit()
        if not bet.isdecimal():
            continue  # jeśli gracz nie podał liczby pytaj ponownie

        bet = int(bet)
        if 1 <= bet <= max_bet:
            return bet  # gracz podał poprawną wartość


def get_deck():  # Zwrócenie listy krotek (wartość=rank, symbol=suit) dla wszystkich 52 kart
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))  # dodanie do talii kart od 2 do 10
        for rank in ("K", "Q", "J", "A"):
            deck.append((rank, suit))  # dodanie do talii figur
    random.shuffle(deck)  # potasowanie talii
    return deck


def display_hands(player_hand, dealer_hand, show_dealer_hand):
    print()
    # Pokazanie kart krupiera:
    if show_dealer_hand:
        print('KRUPIER: ', get_hand_value(dealer_hand))
        display_cards(dealer_hand)
    else:  # Ukryj pierwszą kartę jeśli show_dealer_hand to False
        print('KRUPIER: ???')
        display_cards([BACKSIDE] + dealer_hand[1:])  # widoczna tylko 2ga karta

    # Pokazanie kart gracza:
    print('GRACZ: ', get_hand_value(player_hand))
    display_cards(player_hand)


def get_hand_value(cards):  # Zwrócenie wartości kart. Figury są warte 10pkt, As - 1 lub 11.
    value = 0
    number_of_Aces = 0

    # Dodanie wartości kart (z wyłączeniem Asów):
    for card in cards:
        rank = card[0]  # karta to krotka: (wartość=rank, symbol=suit)
        if rank == 'A':
            number_of_Aces += 1
        elif rank in ('K', 'Q', 'J'):  # figury 10 pkt
            value += 10
        else:
            value += int(rank)  # karty od 2 do 10 > 2 do 10 pkt

    # Dodanie wartości Asów (1 lub 11 pkt):
    value += number_of_Aces  # dodaj 1pkt za Asa
    for i in range(number_of_Aces):
        if value + 10 <= 21:  # jeśli do wartości kart może być dodane jeszcze 10, dodaj 10:
            value += 10

    return value


def display_cards(cards):  # Wyświetlenie kart z listy kart
    rows = ['', '', '', '', '']  # tekst do wyświetlenia w każdym rzędzie - 5 znaków

    for i, card in enumerate(cards):  # https://realpython.com/python-enumerate/
        rows[0] += ' ___ '  # górny rząd
        if card == BACKSIDE:  # ukryta karta krupiera = pokaż tył karty
            rows[1] += '|## |'
            rows[2] += '|###|'
            rows[3] += '|_##|'
        else:
            rank, suit = card  # karta to krotka: (wartość=rank, symbol=suit)
            rows[1] += f'|{rank.ljust(2)} |'
            rows[2] += f'| {suit} |'
            rows[3] += f'|_{rank.rjust(2, "_")}|'

    for row in rows:  # wyświetlenie wszystkich rzędów
        print(row)


def get_move(player_hand, money):  # Zapytanie gracza o ruch - zwrócenie H (hit), S (stand) i D (double down)
    while True:  # pytaj dopóki gracz nie wskaże poprawnej wartości
        moves = ['(H)it', '(S)tand']  # Ustalenie możliwych ruchów gracza
        # Gracz może też zwiększyć stawkę = D tylko przy pierwszym ruchu (= kiedy ma dokładnie 2 karty):
        if len(player_hand) == 2 and money > 0:
            moves.append('(D)ouble down')

        # Pobranie ruchu od gracza (H, S lub D) i zwrócenie go:
        move_prompt = ', '.join(moves) + ' > '
        move = input(move_prompt).upper()
        if move in ('H', 'S'):
            return move  # oddano poprawy wybór
        if move == 'D' and '(D)ouble down' in moves:
            return move  # oddano poprawy wybór


if __name__ == '__main__':
    main()
