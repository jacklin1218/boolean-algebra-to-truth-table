import re
import csv


def input_to_list(string):
    return_list = []
    tmp = 0
    pre_is_letter = 0
    pre_is_moon = 0

    while tmp < len(string):
        if string[tmp] == '(' and pre_is_letter:
            return_list.append("*")
        if string[tmp] == '\'':
            return_list.append("!")
            return_list.append("-1")
            tmp = tmp +1
            continue
        if string[tmp] == " " or string[tmp] == "=":
            tmp = tmp+1
            continue
        if 'A' <= string[tmp] <= 'Z' or 'a' <= string[tmp] <= 'z':

            if pre_is_letter == 1:
                return_list.append('*')
            pre_is_letter = 1
        else:
            pre_is_letter = 0
        if pre_is_moon == 1:
            return_list.append('*')
            pre_is_moon = 0
        if string[tmp] == ')':
            pre_is_moon = 1

        return_list.append(string[tmp])
        tmp = tmp + 1

    return return_list

def dectobin(num, lis):
    for i in range(len(lis) - 1, -1, -1):
        lis[i] = num % 2
        num = int(num / 2)
    return lis


def create_truth_table(string, table):
    formula = input_to_list(string)
    letter_list = check_list(formula)
    count = len(letter_list)
    for i in range(0, pow(2, count)):
        tmp = [0] * count
        table.append(dectobin(i, tmp))


def make_truth_table(string, table):
    formula = input_to_list(string)
    letter_list = check_list(formula)
    count = len(letter_list)
    prefix = infix_to_prefix(formula)

    letter = check_list(formula)
    for i in range(0, pow(2, count)):
        tmp = [0] * count
        dectobin(i, tmp)

        table[i].append(cal_prefix(letter, tmp, prefix) == 1)

    return table


def AND(in1, in2):
    return min(in1, in2)


def OR(in1, in2):
    return max(in1, in2)


def priority(op):
    if op == '+':
        return 1
    if op == '*':
        return 2
    if op == '!':
        return 3
    return 0


def infix_to_prefix(input):
    stack = list()
    answer = list()
    j = 0
    for i in range(0, len(input)):
        if input[i] == '(':
            stack.append(input[i])
        elif input[i] == '*' or input[i] == '+' or input[i] == '!':
            while len(stack)  !=  0 and priority(stack[len(stack) - 1]) >= priority(input[i]):
                answer.append(stack.pop())
            stack.append(input[i])
        elif input[i] == ')':
            while stack[len(stack) - 1]  !=  '(':
                answer.append(stack.pop())
            stack.pop()
        else:
            answer.append(input[i])
    while len(stack) - 1 > -1:
        answer.append(stack.pop())
    #print("ans",input,answer)
    return answer


def check_list(intmp):
    input = list(intmp)
    out_list = []
    for i in range(0, len(input)):
        if 'A' <= input[i] <= 'Z' or 'a' <= input[i] <= 'z':
            flag = 1
            for j in range(0, len(out_list)):
                if out_list[j] == input[i]:
                    flag = 0
                    break
            if flag == 1:
                out_list.append(input[i])
    out_list.sort()
    return out_list


def cal_prefix(number_list, value, formula):
    new_formula = list(formula)
    #print(new_formula)
    stack = []

    for i in range(0, len(new_formula)):

        if 'A' <= new_formula[i] <= 'Z' or 'a' <= new_formula[i] <= 'z':
            for j in range(0, (len(number_list))):
                if new_formula[i] == number_list[j]:
                    stack.append(value[j])
                    new_formula[i] = value[j]
                    break
        elif new_formula[i] == "-1":
            stack.append(-1)
        else:
            tmp1 = stack.pop()
            tmp2 = stack.pop()
            if tmp1 and tmp2 == -1:
                stack.append(1)
            elif tmp1 == -1 or tmp2 == -1:
                stack.append((max(tmp1,tmp2)+1) % 2)
            elif new_formula[i] == '+':
                stack.append(max(tmp1, tmp2))
            else:
                stack.append(min(tmp1, tmp2))

    return stack[0]


def make_table(input_list):
    table = []
    letter_list = []
    flag = 1
    for string in input_list:
        if flag == 1:
            create_truth_table(string,table)
            letter_list = check_list(input_to_list(string))
            flag = 0
        make_truth_table(string, table)
        letter_list.append(string)
    return [table,letter_list]


def table_to_csv(path,table):
    with open(path, 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(table[1])
        for i in range(0, len(table[0]), 1):
            wr.writerow(table[0][i])
    print("save truth table at " + path)


def print_table(table):
    print(table[1])
    for string in table[0]:
        print(string)