def get_expression() -> str:
    """

    function that scan math expression from user and return it without spaces
    :return:  math expression without spaces
    """
    try:
        expression_with_spaces = input("enter math expression: ")
        expression = "".join(expression_with_spaces.split())
        if not expression:
            raise ValueError("user didn't give an expression")

    except EOFError:
        raise EOFError("given end of file input")
    return expression


def check_tilda_and_neg(string: str) -> []:
    """

    :param string: get math expression as string
    :return: list that every element is char in the string and all '-' in a row become 1 (if the number of them is odd)
     and all '-' which suppose to be negative and not operator becomes '~', also the function check all '-' and '~' are
     legal
    """
    if string[-1] == '~' or string[-1] == '-':
        raise ValueError("'-' or '~' cannot be in the end of a mathematical expression")
    if 't' in string or '#' in string:
        raise ValueError("illegal char in expression")
    expression_with_correct_Tildas = []
    index = -1
    while index < len(string):
        index += 1
        Tildas_counter = 0
        if index < len(string):
            if string[index] == '~' and index > 0 and (
                    string[index - 1].isnumeric() or string[index - 1] == ')' or string[index - 1] == '!'):
                raise ValueError("'~' cannot be use as binary operator like '-'")
            if string[index] == '-' and index > 0 and (
                    string[index - 1].isnumeric() or string[index - 1] == ')' or string[index - 1] == '!'):
                expression_with_correct_Tildas.append('-')
            elif string[index] == '~':
                Tildas_counter += 1
                if (not expression_with_correct_Tildas) or (expression_with_correct_Tildas[
                                                                len(expression_with_correct_Tildas) - 1] != '~' and
                                                            expression_with_correct_Tildas[
                                                                len(expression_with_correct_Tildas) - 1] != 't' and
                                                            expression_with_correct_Tildas[
                                                                len(expression_with_correct_Tildas) - 1] != '#'):
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
            elif string[index] == '-':
                Tildas_counter += 1
                if (not expression_with_correct_Tildas) or (expression_with_correct_Tildas[
                                                                len(expression_with_correct_Tildas) - 1] != '~' and
                                                            expression_with_correct_Tildas[
                                                                len(expression_with_correct_Tildas) - 1] != 't' and
                                                            expression_with_correct_Tildas[
                                                                len(expression_with_correct_Tildas) - 1] != '#'):
                    index += 1
                    while index < len(string) and string[index] == '-':
                        Tildas_counter += 1
                        index += 1
                    if Tildas_counter % 2 == 1:
                        expression_with_correct_Tildas.append('#')
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
    """

    :param postfix: get a list which represent a postfix math expression
    :return: the result of the math expression
    """
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
        elif item == '!' or item == '~' or item == '#':
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


def converter_expression_to_postfix_and_calculate(string: str) -> float:
    """
     get a math expression and convert it to postfix and return the result of it
    :param string: get a math expression (string)
    :return: result of math expression
    """
    s = []
    postfix_expression = []
    dot = 0
    sum_of_num = 0
    after_dot = 0
    power10_after_dot = 10
    index = 0
    while index in range(len(string)):
        if string[index] == '(':
            if index < len(string) - 1 and string[index + 1] == '!':
                raise ValueError("parenthesis cannot start with factorial")
            if index > 0 and (string[index - 1].isnumeric() or string[index - 1] != '!'):
                raise ValueError("you must put operator before parenthesis")
            s.append(string[index])
        elif string[index] == ')':
            if index > 0 and ((not string[index - 1].isnumeric()) and string[index - 1] != '!'):
                raise ValueError("parenthesis cannot end with operands except factorial and they also cant be empty")
            if index < len(string) - 1 and string[index + 1].isnumeric():
                raise ValueError("you cant put a number after parenthesis")
            while s and s[len(s) - 1] != '(':
                postfix_expression.append(s.pop())
            if not s:
                raise ValueError("there is closing parenthesis without opening parenthesis")
            s.pop()
        elif string[index].isnumeric():
            while (index < len(string)) and (string[index].isnumeric() or string[index] == '.'):
                if dot == 0 and string[index] == '.':
                    dot = 1
                    if index >= len(string) - 1 or not string[index].isnumeric():
                        raise ValueError("you must put a number after dot")
                elif dot == 1 and string[index].isnumeric():
                    after_dot = after_dot + float(string[index]) / power10_after_dot
                    power10_after_dot = power10_after_dot * 10
                elif dot == 0 and string[index].isnumeric():
                    sum_of_num = sum_of_num * 10 + float(string[index])
                else:
                    raise ValueError("there are 2 dots in one number")
                index += 1
            postfix_expression.append(str(sum_of_num + after_dot))
            sum_of_num = 0
            after_dot = 0
            dot = 0
            power10_after_dot = 10
            index -= 1
        elif string[index] == '+' or string[index] == '-' or string[index] == '*' or string[index] == '/' or string[
            index] == '^' or string[index] == '&' or string[index] == '$' or string[index] == '@' or string[
            index] == '%' or string[index] == '~' or string[index] == '!' or string[index] == '#':
            if string[index] == '!':
                if index < len(string) - 1 and string[index + 1].isnumeric():
                    raise ValueError("you cant put a number after factorial")
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
    result = calculate_postfix_expression(postfix_expression)
    return result


def priority(operator: chr) -> int:
    """

    :param operator: get a char which represent operator
    :return: the power of the operator
    """
    if operator == '+' or operator == '-' or operator == '#':
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
    """

    :param num1: number in math expression
    :param num2: number in math expression
    :param operator: operator between 2 numbers in math expression
    :return: the result of: (num1 operator num2) for example: (5+4) return 9
    """
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
        if num1 < 0 < num2 < 1:
            raise ValueError("cant do power between zero to one for number lower than zero")
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
    """

    :param num1: number in math expression
    :param operator: unary operator in math expression
    :return: the result of the number with the operator for example: 3! return 6
    """
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
    if operator == '~' or operator == '#':
        return str(num1 * -1)


def main():
    try:
        expression = get_expression()
        expression = ''.join(check_tilda_and_neg(expression))
        result = converter_expression_to_postfix_and_calculate(expression)
        print("the result of the expression: " + str(result))
    except (EOFError, ValueError, ZeroDivisionError) as err:
        print(err)


if __name__ == '__main__':
    main()
