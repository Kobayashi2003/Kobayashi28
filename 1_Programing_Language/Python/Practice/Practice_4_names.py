from Practice_4_name_function import get_formatted_name

print("Enter 'q' at any time to quit.")

while True:
    first = input("\nPlease give a first name: ")
    if first == 'q':
        break
    last = input("\nPlease give a last name: ")
    if last == 'q':
        break

formatted_name = get_formatted_name(first, last)
print(f"\tNeatly formatted name: {formatted_name}.")