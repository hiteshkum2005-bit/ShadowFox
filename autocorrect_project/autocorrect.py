from spellchecker import SpellChecker

spell = SpellChecker()

sentence = input("Enter a sentence: ")
words = sentence.split()

corrected = []

for word in words:
    if word in spell:
        corrected.append(word)
    else:
        print(f"\nWord '{word}' is incorrect")
        print("Suggestions:", spell.candidates(word))

        correction = spell.correction(word)

        if correction is None:
            corrected.append(word)
        else:
            corrected.append(correction)

print("\nFinal corrected sentence:")
print(" ".join(corrected))