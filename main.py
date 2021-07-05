import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.properties import StringProperty
import math

Window.size = (300, 500)

def numCon(s, calc=False):
    if s == '':
        return s
    elif s == '.':
        return 0.
    elif s == '-':
        return s
    else:
        if float(s).is_integer():
            if str(s)[-1] == '.' and not calc:
                return s
            else:
                try:
                    return int(s)
                except ValueError:
                    return float(s)
        else:
            return float(s)

class Calculator(App):
    total, oper, numb, mem, m = 0, '', '', None, StringProperty()
    
    def operate(self, operand, number=None):
        if self.oper == '':
            if operand == 'num':
                if self.total == 0 and number != '.':
                    self.total = number
                elif '.' in str(self.total) and number == '.':
                    pass
                else:
                    self.total = str(self.total) + str(number)
            elif operand == 'del':
                if self.total != 0:
                    self.total = numCon(str(self.total)[:-1])
            elif operand == '-' and self.total == 0:
                self.total = '-'
            else:
                self.oper = operand
        else:
            if operand == 'num':
                if self.numb == 0 and number != '.':
                    self.numb = number
                elif self.numb == '' and number == '.':
                    self.numb = 0.
                elif '.' in str(self.numb) and number == '.':
                    pass
                else:
                    self.numb = str(self.numb) + str(number)
            elif operand == 'del':
                if self.numb != 0:
                    self.numb = numCon(str(self.numb)[:-1])
            else:
                self.oper = operand
        self.update()

    def calculate(self, operand=None):
        try:
            self.total = numCon(self.total, True)
            self.numb = numCon(self.numb, True)
            if operand != None:
                if operand == 'sqrt':
                    self.total = math.sqrt(self.total)
                elif operand == '!':
                    self.total = math.factorial(self.total)
            else:
                if self.oper == '+':
                    self.total += self.numb
                elif self.oper == '-':
                    self.total -= self.numb
                elif self.oper == '*':
                    self.total *= self.numb
                elif self.oper == '/':
                    self.total /= self.numb
                elif self.oper == '^':
                    self.total **= self.numb
                elif self.oper == 'floor':
                    self.total = math.floor(self.total / self.numb)
                elif self.oper == 'ceil':
                    self.total = math.ceil(self.total / self.numb)
                elif self.oper == 'mod':
                    self.total %= self.numb
            self.oper, self.numb = '', ''
            self.update()
        except Exception as e:
            self.root.ids.txt.text = f'Error: {e}'

    def update(self, reset=False):
        if not reset:
            self.total, self.numb = numCon(self.total), numCon(self.numb)
            self.root.ids.txt.text = str(self.total) + self.oper + str(self.numb)
        else:
            self.total, self.oper, self.numb = 0, '', ''
            self.root.ids.txt.text = str(self.total) + self.oper + str(self.numb)

    def memory(self, choice, ret=False):
        if ret and self.mem != None:
            self.m = 'M'
        elif ret and self.mem == None:
            self.m = ''
        else:
            if choice == 'MC':
                self.mem = None
            elif choice == 'MR':
                if self.oper == '' and self.mem != None:
                    self.total = self.mem
                    self.update()
                elif self.oper != '' and self.mem != None:
                    self.numb = self.mem
                    self.update()
            elif choice == 'M+':
                self.mem += numCon(self.total)
            elif choice == 'MS':
                self.mem = numCon(self.total)
            self.memory(None, True)

    def build(self):
        self.title = 'Calculator'
        return FloatLayout()

if __name__ == "__main__":
    Calculator().run()