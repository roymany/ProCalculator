def task9(postfix: list) -> float:
    s = []
    num = 0
    num1 = 0
    oper = ''
    num2 = 0
    for char in postfix:
        s.append(char)
        if char == '+' or char == '-' or char == '*' or char == '/':
            oper = s.pop()  # opperator
            num1 = s.pop()
            num2 = s.pop()
            num = caculateByOpperator(float(num2), float(num1), oper)
            s.append(num)

    return s[len(s) - 1]


def task10() -> float:
    s = []
    toReturn = []
    string = input("enter mat")
    dot = 0
    sum_of_num = 0
    after_dot = 0
    power10_after_dot = 10
    index = 0
    while index in range(len(string)):
        if string[index] == '(':
            s.append(string[index])
        if string[index] == ')':
            while s[len(s) - 1] != '(':
                toReturn.append(s.pop())
            s.pop()
        if string[index].isnumeric():
            while (index < len(string)) and (string[index].isnumeric() or string[index] == '.'):
                if dot == 0 and string[index] == '.':
                    dot = 1
                elif dot == 1 and string[index].isnumeric():
                    after_dot = after_dot + float(string[index]) / power10_after_dot
                    power10_after_dot = power10_after_dot * 10
                elif dot == 0 and string[index].isnumeric():
                    sum_of_num = sum_of_num * 10 + float(string[index])
                else:
                    print("error: 2 . in a row")
                    return 0
                index += 1
            toReturn.append(str(sum_of_num + after_dot))
            sum_of_num = 0
            after_dot = 0
            dot = 0
            power10_after_dot = 10
            index -= 1
        if string[index] == '+' or string[index] == '-' or string[index] == '*' or string[index] == '/':
            while s and (kdimut(string[index], s[len(s) - 1]) == 1):
                toReturn.append(s.pop())
            s.append(string[index])
        index += 1
    while s:
        toReturn.append(s.pop())
    print(toReturn)
    result = task9(toReturn)
    return result


def kdimut(oper1: chr, oper2: chr):
    if (oper2 == '*' or oper2 == '/') and (oper1 == '+' or oper1 == '-'):
        return 1
    else:
        return 0


# gets 2 numbers and opperator and return the result for the action betwwen them
def caculateByOpperator(num1: float, num2: float, oper: chr) -> float:
    if oper == '+':
        return num1 + num2
    if oper == '-':
        return num1 - num2
    if oper == '*':
        return num1 * num2
    if oper == '/':
        return num1 / num2


def main():
    print(task10())


if __name__ == '__main__':
    main()
