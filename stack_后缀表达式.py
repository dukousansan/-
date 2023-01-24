# 前缀表达式转后缀表达式并计算结果
# 存在问题1、处理不了括号√
#       2、处理不了浮点数√
#       3、只能计算个位数√
#       4、处理不了分数
from decimal import Decimal


def generate_postfix(infix):    # 本函数实现了中缀表达式转后缀表达式
    """
    generate postfix expression str
    :param infix: infix expression str, like '2×3+8÷3'
    :return: postfix expression str, like '23×83÷+'
    """
    op_rank = {'×': 2, '÷': 2, '+': 1, '-': 1, '(': 0}  # 定义加减乘除括号的优先级
    stack = []  # 用list模拟栈的后进先出
    post_list = []  # 输出的后缀表达式
    num = ''
    for index, s in enumerate(infix):
        if s == '(':    # 左括号,直接进栈
            stack.append(s)
        elif s == ')':  # 右括号,将左括号及之后全部出栈
            while stack[-1] != '(':
                post_list.append(stack.pop())
            stack.pop()
        elif s in '+-×÷':
            # 栈不为空,且栈顶运算符的优先级高于当前运算符,一直退栈到循环终止
            while stack and op_rank.get(stack[-1]) >= op_rank.get(s):
                post_list.append(stack.pop())
            stack.append(s)
        else:  # 是数字，直接进后缀表达式
            if index < len(infix) - 1 and infix[index + 1] in '1234567890.':  # 如果下一位是数字或未遍历完
                num = num + s
            else:
                post_list.append(num + s)
                num = ''  # 如果下一位不是数字或已经遍历完了,则将合成的数字作为一个元素存进列表中,中间变量清空
    while stack:    # 中缀表达式遍历完了，stack所有元素出栈
        post_list.append(stack.pop())
    return post_list


def calculate_postfix(postfix):  # 本函数实现了后缀表达式的求值运算
    """
    calculate postfix expression
    :param postfix: postfix expression str, like '23×83÷+'
    :return: int result, like 2×3+8÷3=6+2=8
    """
    stack = []  # 用list模拟栈的后进先出
    for p in postfix:
        if p in '+-×÷':
            value_2 = float(stack.pop())  # 第二个操作数
            value_1 = float(stack.pop())  # 第一个操作数
            if p == '+':
                result = round(value_1 + value_2, 3)
            elif p == '-':
                result = round(value_1 - value_2, 3)
            elif p == '×':
                result = round(value_1 * value_2, 3)
            else:  # 整除
                result = round(value_1 / value_2, 3)
            stack.append(result)
        else:
            stack.append(p)

    return stack.pop()


if __name__ == "__main__":
    file_deal = './eval.txt'
    equation = open(file_deal, 'r', encoding='utf-8').readlines()
    for item in equation:   # 遍历列表中每个元素
        item1 = item[0: item.index('=')]  # 得到算式
        item2 = item[item.index('=') + 1: item.index('\n')]
        result1 = generate_postfix(item1)   # 得到后缀表达式
        print(item[0: item.index('\n')], end="   ")
        result2 = calculate_postfix(result1)    # 得到计算结果,会给无小数的结果补0
        # print('item={} Decimal_result={}'.format(item2, result2), end=" ")
# 如果无小数,进行去0操作
        if int(result2) == result2:
            if Decimal(result2) == Decimal(result2).to_integral():
                result2 = Decimal(result2).to_integral()
            else:
                result2 = Decimal(result2).normalize()  # 计算结果舍弃小数点后多余的0
# 计算结果与原结果比较
        if float(item2) == result2 and item2 != str(result2):  # 0.0与0的数值相同但是形式错误
            print("True,but formal error")
        elif float(item2) == result2 and item2 == str(result2):
            print("True")
        else:
            print("False")
