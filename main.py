def get_expression() -> str:
    try:
        expression_with_spaces = input("enter expression")
        expression = "".join(expression_with_spaces.split())
        if not expression:
            raise ValueError("user didn't give an expression")

    except EOFError:
        raise EOFError("given end of file input")
    return expression


def check_tilda_and_neg(string: str) -> []:
    if string[-1] == '~' or string[-1] == '-':
        raise ValueError("'-' or '~' cannot be in the end of a mathematical expression")
    if 't' in string:
        raise ValueError("illegal char in expression")
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
                    raise ValueError(
                        "2 '~' in a row cannot be in a mathematical expression unless the first '-' is an operator")
            else:
                expression_with_correct_Tildas.append(string[index])
    for item in expression_with_correct_Tildas:
        if item == 't':
            expression_with_correct_Tildas.remove(item)
    return expression_with_correct_Tildas


def calculate_postfix_expression(postfix: list) -> float:
    s = []
    for item in postfix:
        s.append(item)
        if (item == '+' or item == '-' or item == '*' or item == '/' or item == '^' or item == '&'
                or item == '$' or item == '@' or item == '%'):
            operator = s.pop()
            if len(s) >= 2:
                num1 = s.pop()
                num2 = s.pop()
                try:
                    num = calculate_by_two_operators(float(num2), float(num1), operator)
                except Exception as err:
                    raise err
                s.append(num)
            else:
                raise ValueError("number of operators doesnt match to the number of operands")
        elif item == '!' or item == '~':
            operator = s.pop()
            if len(s) >= 1:
                num1 = s.pop()
                try:
                    num = calculate_by_one_operator(float(num1), operator)
                except Exception as err:
                    raise err
                s.append(num)
            else:
                raise ValueError("number of operators doesnt match to the number of operands")
    if s:
        return s[len(s) - 1]
    return 0


def converter_expression_to_postfix(string: str) -> list:
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
                raise ValueError("there is closing parenthesis without opening parenthesis")
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
                    raise ValueError("cant be 2 dots in one number")
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
            raise ValueError("illegal char in expression")
        index += 1
    if '(' in s:
        raise ValueError("there is opening parenthesis without closing parenthesis")
    while s:
        postfix_expression.append(s.pop())
    return postfix_expression


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
            raise ZeroDivisionError("there is division by zero in the expression")
        return str(num1 / num2)
    if operator == '^':
        return str(num1 ** num2)
    if operator == '%':
        return str(num1 % num2)
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
            raise ValueError("factorial cannot be done on a float number")
        if num1 < 0:
            raise ValueError("factorial cannot be done on a negative number")
        index = 1
        sum_factorial = 1
        while index <= num1:
            sum_factorial = sum_factorial * index
            index += 1
        return sum_factorial
    if operator == '~':
        return str(num1 * -1)


def main():
    try:
        expression = get_expression()
        expression = ''.join(check_tilda_and_neg(expression))
        postfix_expression = converter_expression_to_postfix(expression)
        result = calculate_postfix_expression(postfix_expression)
        print("the result of the expression: " + str(result))
    except (EOFError, ValueError, ZeroDivisionError) as err:
        print(err)


if __name__ == '__main__':
    main()
