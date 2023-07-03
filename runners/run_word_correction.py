from components.word_correction import get_word_suggestions

word="שלום"
suggested_words = get_word_suggestions(word)

if len(suggested_words) == 0:
    print( "No matching words found.")
else:
    print("Suggested words:")
    for i, word in enumerate(suggested_words):
        print(f"{i + 1}. {word}")
    choice = input("Choose a word from the list (enter the number): ")
    chosen_word = suggested_words[int(choice) - 1]
    print(f"You chose: {chosen_word}")
