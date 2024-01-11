ALL_OPERATORS_PRIORITIES = {
    '+': 1,
    '-': 1,
    '_': 1,
    '*': 2,
    '/': 2,
    '^': 3,
    '%': 4,
    '&': 5,
    '@': 5,
    '$': 5,
    '!': 6,
    '~': 6,
    '#': 6,
    '(': 0,
    ')': 0
}
RIGHT_TO_LEFT_OPERATORS = ['!', '#']
BINARY_OPERATORS = ['+', '-', '*', '/', '^', '&', '$', '@', '%']
UNARY_OPERATORS = ['!', '~', '#', '_']


def check_tilda_and_neg(string: str) -> []:
    """
    :param string: get math expression as string
    :return: list that every element is char in the string and all '-' in a row become 1 (if the number of them is odd)
     and all '-' which suppose to be negative and not operator becomes '~', also the function check all '-' and '~' are
    :raise ValueError for illegal syntax problems with '-- and '~' in the expression for example: (~~2)
    """
    if string[-1] == '~' or string[-1] == '-':
        raise ValueError("'-' or '~' cannot be in the end of a mathematical expression")
    if 't' in string or '_' in string:
        raise ValueError("illegal char in expression")
    expression_with_correct_minuses = []
    index = -1
    while index < len(string):
        index += 1
        t_counter = 0
        if index < len(string):
            if string[index] == '~' and index > 0 and (
                    string[index - 1].isnumeric() or string[index - 1] == ')'
                    or string[index - 1] in RIGHT_TO_LEFT_OPERATORS):
                raise ValueError("'~' cannot be use as binary operator like '-'")
            if string[index] == '-' and index > 0 and (
                    string[index - 1].isnumeric() or string[index - 1] == ')' or
                    string[index - 1] in RIGHT_TO_LEFT_OPERATORS):
                expression_with_correct_minuses.append('-')
            elif string[index] == '-' and (index == 0 or string[index - 1] == '('):
                t_counter += 1
                index += 1
                while index < len(string) and string[index] == '-':
                    t_counter += 1
                    index += 1
                if t_counter % 2 == 1:
                    expression_with_correct_minuses.append('_')
                else:
                    expression_with_correct_minuses.append('t')
                index -= 1
            elif string[index] == '~' or string[index] == '-':
                t_counter += 1
                if (not expression_with_correct_minuses) or (expression_with_correct_minuses[
                                                                 len(expression_with_correct_minuses) - 1] != '~' and
                                                             expression_with_correct_minuses[
                                                                 len(expression_with_correct_minuses) - 1] != 't' and
                                                             expression_with_correct_minuses[
                                                                 len(expression_with_correct_minuses) - 1] != '_'):
                    index += 1
                    while index < len(string) and string[index] == '-':
                        t_counter += 1
                        index += 1
                    if t_counter % 2 == 1:
                        expression_with_correct_minuses.append('~')
                    else:
                        expression_with_correct_minuses.append('t')
                    index -= 1
                else:
                    raise ValueError(
                        "2 '~' in a row cannot be in a mathematical expression unless the first '-' is an operator")
            else:
                expression_with_correct_minuses.append(string[index])
    for item in expression_with_correct_minuses:
        if item == 't':
            expression_with_correct_minuses.remove(item)
    return expression_with_correct_minuses


def calculate_postfix_expression(postfix: list) -> float:
    """
    :param postfix: get a list which represent a postfix math expression
    :return: the result of the math expression
    :raise ValueError if number of operators doesn't match to the number of operands
    """
    s = []
    for item in postfix:
        s.append(item)
        if item in BINARY_OPERATORS:
            operator = s.pop()
            if len(s) >= 2:
                num1 = s.pop()
                num2 = s.pop()
                try:
                    num = calculate_by_two_operators(float(num2), float(num1), operator)
                except (ValueError, ZeroDivisionError, OverflowError) as err:
                    raise err
                s.append(num)
            else:
                raise ValueError("number of operators doesn't match to the number of operands")
        elif item in UNARY_OPERATORS:
            operator = s.pop()
            if len(s) >= 1:
                num1 = s.pop()
                try:
                    num = calculate_by_one_operator(float(num1), operator)
                except ValueError as err:
                    raise err
                s.append(num)
            else:
                raise ValueError("number of operators doesn't match to the number of operands")
    if s:
        return s[len(s) - 1]
    return 0


def converter_expression_to_postfix(string: str) -> list:
    """
     get a math expression and convert it to postfix and return it
    :param string: get a math expression (string)
    :return: postfix of math expression
    :raise ValueError for illegal syntax problems in the expression for example: (!)
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
            if index < len(string) - 1 and (string[index + 1] in RIGHT_TO_LEFT_OPERATORS):
                raise ValueError("parenthesis cannot start with factorial or hash mark")
            if index > 0 and (
                    string[index - 1].isnumeric() or string[index - 1] == ')' or
                    string[index - 1] in RIGHT_TO_LEFT_OPERATORS):
                raise ValueError("you must put operator before parenthesis")
            s.append(string[index])
        elif string[index] == ')':
            if index > 0 and (
                    (not string[index - 1].isnumeric()) and (string[index - 1] not in RIGHT_TO_LEFT_OPERATORS)):
                raise ValueError(
                    "parenthesis cannot end with operator except factorial and hash mark and they also cant be empty")
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
                    if index >= len(string) - 1 or not string[index + 1].isnumeric():
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
        elif string[index] in ALL_OPERATORS_PRIORITIES:
            if string[index] in RIGHT_TO_LEFT_OPERATORS:
                if index < len(string) - 1 and string[index + 1].isnumeric():
                    raise ValueError("you cant put a number after factorial or hash mark")
            while s and (ALL_OPERATORS_PRIORITIES[string[index]] <= ALL_OPERATORS_PRIORITIES[s[len(s) - 1]]):
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


def calculate_by_two_operators(num1: float, num2: float, operator: chr) -> str:
    """

    :param num1: number in math expression
    :param num2: number in math expression
    :param operator: operator between 2 numbers in math expression
    :return: the result of: (num1 operator num2) for example: (5+4) return 9
    :raise OverflowError if number is too big
    :raise ZeroDivisionError if there is division by zero in the expression
    :raise ValueError if power is between zero and one on for number lower than zero
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
        try:
            str(num1 ** num2)
        except OverflowError:
            raise OverflowError("number is too big")
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
    :raise ValueError if factorial is on negative or float number or hash mark is on negative number
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
    if operator == '~' or operator == '_':
        return str(num1 * -1)
    if operator == '#':
        st_num = str(num1)
        if st_num[0] == '-':
            raise ValueError("cant do hash mark on a negative number")
        total = 0
        for char in st_num:
            if char != '.':
                total += int(char)
        return str(total)


def all_together(user_expression: str):
    """
    get expression from user and combine all functions together to print the result of the expression
    or print the error in the expression
    :param user_expression: get expression from the input of a user
    """
    try:
        expression_without_spaces = "".join(user_expression.split())
        if not expression_without_spaces:
            print("user didn't give an expression")
            return
        final_expression = ''.join(check_tilda_and_neg(expression_without_spaces))
        postfix_expression = converter_expression_to_postfix(final_expression)
        result_of_expression = calculate_postfix_expression(postfix_expression)
        print("the result of the expression: " + str(result_of_expression))
    except (ValueError, ZeroDivisionError, OverflowError) as err:
        print(err)


def main():
    user_expression = ""
    while user_expression != "exit":
        try:
            user_expression = input("\nTo stop, press ^D (EOF) or type exit\nPlease enter math expression:")
            if user_expression != "exit":
                all_together(user_expression)
            else:
                print("user wants to exit, bye bye!  :)")
        except EOFError as err:
            print("user gave EOF input, bye bye!  :)")
            break


if __name__ == '__main__':
    main()
