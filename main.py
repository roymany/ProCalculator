def get_expression() -> str:
    try:
        expression = input("enter expression")
        expression.replace(" ", "")
    except EOFError:
        print("end of file interrupt")
        return ""
    return expression


def check_tilda_and_neg(string: str) -> []:
    if string[-1] == '~' or string[-1] == '-':
        print("error:")
    if 't' in string:
        print("error, not correct input")
    expression_with_correct_Tildas = []
    index = -1
    while index < len(string):
        index += 1
        Tildas_counter = 0
        if index < len(string):
            if string[index] == '-' and index > 0 and (
                    string[index - 1].isnumeric() or string[index - 1] == ')' or string[index - 1] == '!'):
                expression_with_correct_Tildas.append('-')
            elif string[index] == '-' or string[index] == '~':
                Tildas_counter += 1
                if (not expression_with_correct_Tildas) or (expression_with_correct_Tildas[
                                                                len(expression_with_correct_Tildas) - 1] != '~' and
                                                            expression_with_correct_Tildas[
                                                                len(expression_with_correct_Tildas) - 1] != 't'):
                    index += 1
                    while index < len(string) and string[index] == '-':
                        Tildas_counter += 1
                        index += 1
                    if Tildas_counter % 2 == 1:
                        expression_with_correct_Tildas.append('~')
                    else:
                        expression_with_correct_Tildas.append('t')
                    index -= 1
                else:
                    print("error with -~")
                    return
            else:
                expression_with_correct_Tildas.append(string[index])
    for item in expression_with_correct_Tildas:
        if item == 't':
            expression_with_correct_Tildas.remove(item)
    return expression_with_correct_Tildas


"""def check_if_expression_is_valid(string: str) -> bool:
    if (not string[0].isnumeric()) and (string[0] != '-' or string[0] != '~' or string[0] != '('):
        return False
    index = 0
    list_of_brackets = []
    while index in range(len(string)):
        if string[index] == '-' or string[index] == '~':
            index = +1
            while index < len(string) and string[index] == '-':
                index += 1
            if not (index < len(string) and (string[index].isnumeric() or string[index] == '(')):
                return False
            index -= 1
        elif string[index] == '(':
            list_of_brackets.append(1)
        elif string[index] == ')':
            if not list_of_brackets:
                return False
            list_of_brackets.pop()
        elif (string[index] == '+' or string[index] == '*' or string[index] == '/' or string[index] == '@' or
              string[index] == '^' or string[index] == '&' or string[index] == '%' or string[index] == '$'):
            if (((string[index - 1] != '!' or string[index - 1] != ')') and (not string[index - 1].isnumeric()))
                    or (index + 1 >= len(string)) or ((not string[index + 1].isnumeric()) and (
                            string[index + 1] != '-' or string[index + 1] != '~' or string[index + 1] != '('))):
                return False
        elif string[index].isnumeric():
            print("")
        else:
            return False
        index += 1
    return True"""


def calculate_postfix_expression(postfix: list) -> float:
    s = []
    for item in postfix:
        s.append(item)
        if (item == '+' or item == '-' or item == '*' or item == '/' or item == '^' or item == '&'
                or item == '$' or item == '@' or item == '%'):
            operator = s.pop()
            if len(s) > 2:
                num1 = s.pop()
                num2 = s.pop()
                num = calculate_by_two_operators(float(num2), float(num1), operator)
                s.append(num)
            else:
                print("error")
        elif item == '!' or item == '~':
            operator = s.pop()
            if len(s) > 1:
                num1 = s.pop()
                num = calculate_by_one_operator(float(num1), operator)
                s.append(num)
    return s[len(s) - 1]


def converter_expression_to_postfix(string: str) -> float:
    s = []
    postfix_expression = []
    dot = 0
    sum_of_num = 0
    after_dot = 0
    power10_after_dot = 10
    index = 0
    while index in range(len(string)):
        if string[index] == '(':
            s.append(string[index])
        elif string[index] == ')':
            while s and s[len(s) - 1] != '(':
                postfix_expression.append(s.pop())
            if not s:
                print("error: ) with no (")
            s.pop()
        elif string[index].isnumeric():
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
            postfix_expression.append(str(sum_of_num + after_dot))
            sum_of_num = 0
            after_dot = 0
            dot = 0
            power10_after_dot = 10
            index -= 1
        elif string[index] == '+' or string[index] == '-' or string[index] == '*' or string[index] == '/' or string[
            index] == '^' or string[index] == '&' or string[index] == '$' or string[index] == '@' or string[
            index] == '%' or string[index] == '~' or string[index] == '!':
            while s and (priority(string[index]) <= priority(s[len(s) - 1])):
                postfix_expression.append(s.pop())
            s.append(string[index])
        else:
            print("error: illegal char")
        index += 1
    if '(' in s:
        print("error: ( wih no )")
    while s:
        postfix_expression.append(s.pop())
    print(postfix_expression)
    result = calculate_postfix_expression(postfix_expression)
    return result


def priority(operator: chr) -> int:
    if operator == '+' or operator == '-':
        return 1
    elif operator == '*' or operator == '/':
        return 2
    elif operator == '^':
        return 3
    elif operator == '%':
        return 4
    elif operator == '&' or operator == '@' or operator == '$':
        return 5
    elif operator == '!' or operator == '~':
        return 6
    else:
        return 0


def calculate_by_two_operators(num1: float, num2: float, operator: chr) -> str:
    if operator == '+':
        return str(num1 + num2)
    if operator == '-':
        return str(num1 - num2)
    if operator == '*':
        return str(num1 * num2)
    if operator == '/':
        if num2 == 0:
            print("error: divide by zero")
            return ""  # return exception
        return str(num1 / num2)
    if operator == '^':
        return str(num1 ** num2)
    if operator == '@':
        return str((num1 + num2) / 2)
    if operator == '&':
        if num1 < num2:
            return str(num1)
        return str(num2)
    if operator == '$':
        if num1 > num2:
            return str(num1)
        return str(num2)


def calculate_by_one_operator(num1: float, operator: chr) -> str:
    if operator == '!':
        temp = num1
        numbers_after_decimal = str(temp).split('.')[1]
        if int(numbers_after_decimal) != 0:
            print("error: factorial to float number")
            return ""
        if num1 < 0:
            print("error: factorial to negative number")
            return ""
        index = 1
        sum_factorial = 1
        while index <= num1:
            sum_factorial = sum_factorial * index
            index += 1
        return sum_factorial
    if operator == '~':
        return str(num1 * -1)


def main():
    expression = ''.join(check_tilda_and_neg("+*/"))
    print(expression)
    print(converter_expression_to_postfix(expression))


if __name__ == '__main__':
    main()
