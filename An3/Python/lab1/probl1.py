
def CMMDC(numbers):
    for number in numbers[1:]:
        while numbers[0] != number:
            if numbers[0] > number:
                numbers[0] = numbers[0] - number
            else:
                number = number - numbers[0]
            number = numbers[0]
    print("CMMDC: {}".format(numbers[0]))


if __name__ == '__main__':
    numbers = [int(element) for element in input("Introdu numerele pls: ").split(" ")]
    CMMDC(numbers)
