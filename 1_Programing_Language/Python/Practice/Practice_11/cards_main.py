#! /usr/bin/python3
import sys
import cards_tools

while True:
    # display function menu
    cards_tools.show_menu()

    action_str = input("Please input the action you want to perfrom:")
    # Perform corresponding functions
    if action_str in ['1', '2', '3']:
        # add a new card
        if action_str == '1':
            cards_tools.new_card()

        # show all cards
        elif action_str == '2':
            cards_tools.show_all()

        # search card
        else:
            cards_tools.search_card()

        pass

    # exit from application program
    elif action_str == '0':
        print("Thanks for using!")
        break

    # error input prompt
    else:
        print("Wrong action! Please input again!")