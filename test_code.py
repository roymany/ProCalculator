import pytest
from main import all_together


def test_errors():
    """
    test wrong math expressions (math expressions with errors)
    """
    assert all_together("3+*2") == "ValueError"
    assert all_together("3!-") == "ValueError"
    assert all_together("3^*2") == "ValueError"
    assert all_together("5~-1") == "ValueError"
    assert all_together("5+1^2~7") == "ValueError"
    assert all_together("(5+1") == "ValueError"
    assert all_together("hello") == "ValueError"
    assert all_together("") == "NoneError"
    assert all_together("(2)2+t") == "ValueError"
    assert all_together("2/0") == "ZeroDivisionError"
    assert all_together("       ") == "NoneError"
    assert all_together("10^100000") == "OverflowError"


def test_simple_expressions():
    """
    test simple math expressions
    """
    assert all_together("3+2") == "5.0"
    assert all_together("3-2") == "1.0"
    assert all_together("3*2") == "6.0"
    assert all_together("5/2") == "2.5"
    assert all_together("3^2") == "9.0"
    assert all_together("7@2") == "4.5"
    assert all_together("3$2") == "3.0"
    assert all_together("3&2") == "2.0"
    assert all_together("3%2") == "1.0"
    assert all_together("~2") == "-2.0"
    assert all_together("3!") == "6.0"
    assert all_together("333#") == "9.0"


def test_complex_expressions():
    """
    test complex math expressions
    """
    assert all_together("((3+2*4)/2)#") == "10.0"
    assert all_together("-3^2") == "-9.0"
    assert all_together("~-3^2") == "9.0"
    assert all_together("2.5* 4+ (3  !)") == "16.0"
    assert all_together("(4 !#-  -3)$  4-2") == "7.0"
    assert all_together("4!#--3$4-2") == "0.0"
    assert all_together("5!/4+9^0.5-3*2^2") == "21.0"
    assert all_together("(-3)^0.5") == "ValueError"
    assert all_together("()4+1") == "ValueError"
    assert all_together("(2+3)2") == "ValueError"
    assert all_together("5.3!@4") == "ValueError"
    assert all_together("5!@4.2*3&1+(2^3)%8") == "62.1"
    assert all_together("5!&4+9^2") == "85.0"
    assert all_together("5!/4+9^0.5-3*2^2") == "21.0"
    assert all_together("((5+-2+~-2)^2) * 41 @ -10") == "387.5"
