def Palindrom(number):
    number = list(number)
    start = 0
    end = len(number) - 1
    while start < end:
        if number[start] != number[end]:
            print("Numarul nu este un palindrom")
            break
        start += 1
        end -= 1
    print("Numarul este palindrom")


if __name__ == '__main__':
    number = input("Write a number: ")
    Palindrom(number)
