# record all cards
card_list = []


def show_menu():
    """display function menu"""
    print("*" * 50)
    print("welcome to use my application [Cards Manager System]")
    print("")
    print("1. add a new card")
    print("2. show all cards")
    print("3. search cards")
    print("")
    print("0. exit")
    print("")
    print("*" * 50)


def new_card():
    """add a new card"""
    print("-" * 50)
    print("add a new card")

    # Promopt the user for details of the new card
    name_str = input("Please input your name:")
    job_str = input("Please input your job:")
    phone_str = input("Please input your phone number:")

    # Create a dictionary using the information entered by the user
    card_dict = {
        "name": name_str,
        "job": job_str,
        "phone": phone_str
    }

    # Add the dictionary into the list of cards
    card_list.append(card_dict)

    # Prompt the user for successful input
    print(f"Added {name_str} successfully!")


def show_all():
    """show all cards"""
    print("-" * 50)
    print("show all cards")

    # Determine whether there is card record
    if len(card_list) == 0:
        print("There are no cards in the current list, please add a new card first!")
        return

    # Print header
    # for elem in ["name", "job", "phone"]:
    #     print(elem, end="\t\t\t")
    print(f"name\t\tjob\t\tphone")

    print("")
    print("=" * 50)

    # Traverse the card list and output dictionary information
    for card_dict in card_list:
        print(f"{card_dict['name']}\t\t{card_dict['job']}\t\t{card_dict['phone']}")


def search_card():
    """search card"""
    print("-" * 50)
    print("search card")

    # Prompt the user to enter the name to search
    find_name = input("Please input the name you want to search:")

    # Traverse the list and query the name to search, if the name does not exit, the user needs to be prompted
    for card_dict in card_list:

        if card_dict["name"] == find_name:
            print(f"name\t\tjob\t\tphone")
            print("=" * 50)
            print(f"{card_dict['name']}\t\t{card_dict['job']}\t\t{card_dict['phone']}")
            print("")

            deal_card(card_dict)

            break

    else:
        print("sorry, this name does not exit")


def deal_card(find_dict):

    """Process the card
    :param find_dict: the founded card
    """

    action_str = input("Please select the operation to be performed: [1] Modify [2] Delete [0] Previous Menu:")

    if action_str == "1":

        find_dict["name"] = input_card_info(find_dict["name"], "Please input the new name")
        find_dict["job"] = input_card_info(find_dict["job"], "Please input the new job")
        find_dict["phone"] = input_card_info(find_dict["phone"], "Please input the new phone")
        print("Modify succeeded!")

    elif action_str == "2":
        card_list.remove(find_dict)
        print("Delete succeeded!")


def input_card_info(dict_value, tip_message):

    """input the new message of the card
    :param dict_value: Original value in dictionary
    :param tip_message: Prompt message entered
    :return: If the user inputs content, the input value will be returned; if not, the original value in the dictionary will be returned
    """

    # Prompt the user for input
    result_str = input(tip_message + "[Enter 'enter' directly to make no change]:")

    # Judge according to the user's input
    if len(result_str) > 0:
        return result_str
    else:
        return dict_value