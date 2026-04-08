from spellchecker import SpellChecker
import re

spell = SpellChecker()


def extract_punctuation(word: str) -> tuple[str, str, str]:
    match = re.match(r'^(\W*)(.*?)(\W*)$', word)
    if match:
        return match.group(1), match.group(2), match.group(3)
    return "", word, ""


def is_misspelled(word: str) -> bool:
    return word.lower() in spell.unknown([word.lower()])


def get_correction(word: str, preserve_case: bool = True) -> str | None:
    word_lower = word.lower()
    if word_lower not in spell.unknown([word_lower]):
        return None
    correction = spell.correction(word_lower)
    if correction and preserve_case:
        if word[0].isupper():
            correction = correction.capitalize()
    return correction


def correct_word(word: str) -> str:
    prefix, core, suffix = extract_punctuation(word)
    lower_core = core.lower()

    if is_misspelled(lower_core):
        correction = get_correction(lower_core)
        if correction:
            core = correction

    return prefix + core + suffix


def correct_text(text: str) -> str:
    words = text.split()
    return " ".join(correct_word(word) for word in words)


def main():
    print("=" * 50)
    print("         AUTOCORRECT SYSTEM")
    print("=" * 50)

    while True:
        print("\n" + "-" * 50)
        sentence = input("Enter text (or 'quit' to exit): ").strip()

        if sentence.lower() == 'quit':
            print("\nGoodbye!")
            break

        if not sentence:
            print("Please enter some text.")
            continue

        words = sentence.split()
        corrections = []
        has_errors = False

        for word in words:
            lower = word.lower()
            if lower in spell.unknown([lower]):
                has_errors = True
                suggestion = spell.correction(lower)
                if suggestion and word[0].isupper():
                    suggestion = suggestion.capitalize()
                corrections.append((word, suggestion))

        if corrections:
            print("\nMisspelled words found:")
            for original, corrected in corrections:
                print(f"  '{original}' -> '{corrected}'")

        result = correct_text(sentence)
        print(f"\nCorrected: {result}")

        if not has_errors:
            print("(No spelling errors detected)")


if __name__ == "__main__":
    main()
