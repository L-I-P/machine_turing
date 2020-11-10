class State:
    def __init__(self, q, sym):
        self.q = q  # state
        self.sym = sym  # symbol


class Rule:
    def __init__(self, text, cur_q, next_q, cur_sym, next_sym, cmd):
        self.text = text  # content of rules
        self.cur_q = cur_q  # current state
        self.next_q = next_q  # next state
        self.cur_sym = cur_sym  # current symbol
        self.next_sym = next_sym  # next symbol
        self.cmd = cmd  # move command


class MT:
    rules = []
    cur_state = State('', '')

    def __init__(self, mem, beg_state, width):
        self.mem = mem
        self.width = width
        self.cur_pos = 0
        self.cur_state.q = beg_state
        self.cur_state.sym = mem[self.cur_pos]
        self.r_num = 0

    def get_sym(self):
        return self.mem[self.cur_pos]

    def get_state(self):
        return self.cur_state.q

    def get_mem(self):
        return self.mem

    def add_rule(self, rule):
        self.rules.append(Rule(rule, rule[0:self.width],
                               rule[(rule.find('->') + 2):((rule.find('->') + 2) + self.width)],
                               rule[self.width], rule[len(rule) - 2], rule[len(rule) - 1]))
        self.r_num += 1
        return True

    def process(self, i):
        if self.rules[i].cmd == 'L':
            self.cur_pos += -1
        elif self.rules[i].cmd == 'R':
            self.cur_pos += 1
        self.cur_state.q = self.rules[i].next_q

        if self.cur_pos < 0:
            return False

        if self.cur_pos >= len(self.mem):
            self.mem = self.mem + " "
        self.cur_state.sym = self.mem[self.cur_pos]

    def step(self):
        i = 0
        while i < self.r_num:
            if self.cur_state.q == self.rules[i].cur_q and self.cur_state.sym == self.rules[i].cur_sym:
                with open("C:/Users/Admin/PycharmProjects/tvp2/result.txt", "a") as file:
                    file.write('Before: {} {} {}\n'.format(self.get_mem(), self.get_state(), self.get_sym()))
                self.mem = self.mem[0:self.cur_pos] + self.rules[i].next_sym \
                        + self.mem[self.cur_pos + 1:len(self.mem)]

                with open("C:/Users/Admin/PycharmProjects/tvp2/result.txt", "a") as file:
                    file.write('After:  {} {} {} {}\n'.format(self.get_mem(), self.get_state(), self.get_sym(), self.rules[i].cmd))

                self.process(i)
            i += 1


if __name__ == '__main__':
    with open('C:/Users/Admin/PycharmProjects/tvp2/entrance_tape.txt') as in_file:
        for line in in_file:
            line = line.replace('\n', '')
            mt = MT(line, 'q00', 3)

    print('{} {} {}'.format(mt.get_mem(), mt.get_state(), mt.get_sym()))

    with open('C:/Users/Admin/PycharmProjects/tvp2/rules.txt') as in_file:
        for line in in_file:
            line = line.replace('\n', '')
            mt.add_rule(line)

    while mt.get_state() != 'q09':
        mt.step()
