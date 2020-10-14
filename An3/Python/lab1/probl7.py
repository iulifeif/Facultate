def RegexNumber(text):
    number = "123456789"
    numberString = ""
    for character in text:
        if character in number:
            numberString += character
        if character not in number and numberString != "":
            return numberString
    if character in number:
        return numberString


if __name__ == '__main__':
    text = input("Scrie un text: ")
    print(RegexNumber(text))
