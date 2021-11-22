import random
import re
import sys
number_pattern = re.compile(r'\(?(?:[0-9]+,)?[0-9]+\)?')
operator_pattern = re.compile(r'(\+|\-|\*|\/)')
formula_pattern = re.compile(r'(\(?[0-9]+)(.*)([0-9]+\)?)')
ADD = '+'
SUB = '-'
ADD_SUB = '+-'
MUL = '*'
DIV = '/'
MUL_DIV = '*/'
LEFT_BRACKET = "("
RIGHT_BRACKET = ")"

def getStartAndEndValue(s):
    start_end_values = dict()
    start, end = 0, 0
    if s.startswith(LEFT_BRACKET):
        s = s.replace(LEFT_BRACKET, '')
        start_end_values['left_bracket'] = LEFT_BRACKET
    elif s.endswith(RIGHT_BRACKET):
        s = s.replace(RIGHT_BRACKET, '')
        start_end_values['right_bracket'] = RIGHT_BRACKET
    if ',' in s:
        t = s.split(',')
        start = int(t[0].strip())
        end = int(t[1].strip())
    else:
        start = 1
        end = int(s.strip())
    start_end_values['start_end'] = (start, end)
    return start_end_values

def add_bracket(s, start_end_values, pos):
    m = formula_pattern.match(s)
    if m:
        first, operator, second = m.group(1), m.group(2),m.group(3)
        if 'left_bracket' in start_end_values:
            if pos == 1:
                s = LEFT_BRACKET + first + operator + second
            elif pos == 2:
                s = first + operator + LEFT_BRACKET + second
        elif 'right_bracket' in start_end_values:
            if pos == 1:
                s = first + RIGHT_BRACKET + operator + second
            elif pos == 2:
                s = first + operator + second + RIGHT_BRACKET
    else:
        if 'left_bracket' in start_end_values:
            if pos == 1:
                s = LEFT_BRACKET + s
            elif pos == 2:
                s = s + LEFT_BRACKET
        elif 'right_bracket' in start_end_values:
            if pos == 1:
                s = s + RIGHT_BRACKET
            elif pos == 2:
                s = RIGHT_BRACKET + s
    return s

class calculate:
    def __init__(self, formula, formulaNumber):
        self.formulaNumber = formulaNumber
        self.formula = re.sub('\s+', '' ,formula)
        self.result = set()
        self.numbers, self.operators = self.parseFormula()

    def parseFormula(self):
        numbers = number_pattern.findall(self.formula)
        operators = number_pattern.split(self.formula)
        operators = [ x for x in operators if x ]
        # numbers ['10', '10', '10', '10', '10', '10']
        # operators ['+-', '-', '*', '/', '=']
        if operators[-1] == '=':
            self.result_limit = getStartAndEndValue(numbers.pop())['start_end']
            operators.pop()
        return numbers, operators

    def do_task(self):
        count = 0
        while count <= 1000 and len(self.result) < self.formulaNumber:
            number_point = len(self.numbers) - 1
            operator_point = len(self.operators) -1
            temp = None
            while number_point >= 0:
                limit_j = getStartAndEndValue(self.numbers[number_point])
                number_point = number_point - 1
                operator = self.operators[operator_point]
                operator_point = operator_point - 1
                if temp:
                    if operator == ADD_SUB:
                        if random.randint(1,100) %2 == 0:
                            temp = self._add(limit_j, temp)
                        else:
                            temp = self._sub(limit_j, temp)
                    elif operator == MUL_DIV:
                        if random.randint(1,100) %2 == 0:
                            temp = self._mul(limit_j, temp)
                        else:
                            temp = self._div(limit_j, temp)
                    elif operator == ADD:
                        temp = self._add(limit_j, temp)
                    elif operator == SUB:
                        temp = self._sub(limit_j, temp)
                    elif operator == MUL:
                        temp = self._mul(limit_j, temp)
                    elif operator == DIV:
                        temp = self._div(limit_j, temp)
                else:
                    limit_i = getStartAndEndValue(self.numbers[number_point])
                    number_point = number_point - 1
                    if operator == ADD_SUB:
                        if random.randint(1,100) %2 == 0:
                            temp = self._add(limit_i, limit_j)
                        else:
                            temp = self._sub(limit_i, limit_j)
                    elif operator == MUL_DIV:
                        if random.randint(1,100) %2 == 0:
                            temp = self._mul(limit_i, limit_j)
                        else:
                            temp = self._div(limit_i, limit_j)
                    elif operator == ADD:
                        temp = self._add(limit_i, limit_j)
                    elif operator == SUB:
                        temp = self._sub(limit_i, limit_j)
                    elif operator == MUL:
                        temp = self._mul(limit_i, limit_j)
                    elif operator == DIV:
                        temp = self._div(limit_i, limit_j)
            if eval(temp) < self.result_limit[0] or  eval(temp) > self.result_limit[1]:
                continue
            else:
                temp = temp.replace('*', '×')
                temp = temp.replace('/', '÷')
                self.result.add(temp + ' =')
            count = count + 1

    def _add(self, parse_result1, parse_result2):
        limit_i = parse_result1['start_end']
        while len(self.result) < self.formulaNumber:
            new_formula = None
            i = random.randint(limit_i[0], limit_i[1])
            if isinstance(parse_result2, dict):
                limit_j = parse_result2['start_end']
                j = random.randint(limit_j[0], limit_j[1])
                if self.result_limit and i + j >= self.result_limit[0] and i + j <= self.result_limit[1]:
                    new_formula =  '%s + %s' % (i, j)
            else:
                new_formula =  '%s + %s' % (i, parse_result2)
            new_formula = add_bracket(new_formula, parse_result1, 1)
            new_formula = add_bracket(new_formula, parse_result2 ,2)
            return new_formula

    def _mul(self, parse_result1, parse_result2):
        limit_i = parse_result1['start_end']
        while len(self.result) < self.formulaNumber:
            new_formula = None
            i = random.randint(limit_i[0], limit_i[1])
            if isinstance(parse_result2, dict):
                limit_j = parse_result2['start_end']
                j = random.randint(limit_j[0], limit_j[1])
                if self.result_limit and i * j >= self.result_limit[0] and i * j <= self.result_limit[1]:
                    new_formula =  '%s * %s' % (i, j)
            else:
                new_formula = '%s * %s' % (i, parse_result2)
            new_formula = add_bracket(new_formula, parse_result1, 1)
            new_formula = add_bracket(new_formula, parse_result2, 2)
            return new_formula

    def _sub(self, parse_result1, parse_result2):
        limit_i = parse_result1['start_end']
        while len(self.result) < self.formulaNumber:
            new_formula = None
            i = random.randint(limit_i[0], limit_i[1])
            if isinstance(parse_result2, dict):
                limit_j = parse_result2['start_end']
                j = random.randint(limit_j[0], limit_j[1])
                if i > j:
                    new_formula =  '%s - %s' % (i, j)
                else:
                    continue
            else:
                new_formula = '%s - %s' % (i, parse_result2)
            new_formula = add_bracket(new_formula, parse_result1, 1)
            new_formula = add_bracket(new_formula, parse_result2, 2)
            return new_formula

    def _div(self, parse_result1, parse_result2):
        limit_i = parse_result1['start_end']
        count  = 0
        while len(self.result) < self.formulaNumber or count < 1000:
            count = count + 1
            new_formula = ''
            i = random.randint(limit_i[0], limit_i[1])
            if isinstance(parse_result2, dict):
                limit_j = parse_result2['start_end']
                j = random.randint(limit_j[0], limit_j[1])
                if i > j and i % j == 0:
                    new_formula = '%s / %s' % (i, j)
                else:
                    continue
            else:
                t = eval(parse_result2)
                # parse_result1没有括号的算式
                if (not ('left_bracket' in parse_result1))  and (not ('right_bracket' in parse_result1)):
                    if i > t and i % t == 0:
                        new_formula =  '%s / %s' % (i, parse_result2)
                    else:
                        continue
                # parse_result1有括号的非算式
                else:
                    new_formula = '%s / %s' % (i, parse_result2)
            new_formula = add_bracket(new_formula, parse_result1, 1)
            new_formula = add_bracket(new_formula, parse_result2, 2)
            return new_formula

    def print_result(self):
        for index, i in enumerate(self.result):
            if index % 5 == 0:
                print()
            print(i + "\t\t\t", end='')


if __name__ == '__main__':
    cal = calculate( '2,81 / 1,9 = 1,9', 10)
    cal = calculate( '(100 + 100) / 2 + 9 = 10000', 10)
    cal = calculate( '(10 + 100) / (2 + 9) = 10000', 10)
    # cal = calculate('(1,5 + 1,5) * (7,9 + 2,7) / (3 + 2) = 10000', 100)
    # cal = calculate('3,9 / 3,9 = 100', 10)
    cal.do_task()
    cal.print_result()