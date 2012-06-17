#coding: utf-8
 
class FSM:
    def __init__(self):
        self.__table = {}
        self.__initial_states = set()
        self.__final_states = set()
 
    def add_transition(self, state, symbol, new_states):
        """
            state = string
            symbol = string, len = 1
            new_states = list
        """
        try:
            self.__table[state]
        except:
            self.__table[state] = {}
            
        if type(new_states) == str:
            self.__table[state][symbol] = set([new_states])
        else:
            self.__table[state][symbol] = set(new_states)
 
    def add_initial_states(self, states):
        """
            state = list or str
        """
        if type(states) == str:
            self.__initial_states.update([states])
        else:
            self.__initial_states.update(states)
 
    def add_final_states(self, states):
        """
            states = list or str
        """
        if type(states) == str:
            self.__final_states.update([states])
        else:
            self.__final_states.update(states)
 
    def __get_new_states_e(self, states):
        visited_states_a = states.copy()
        visited_states_b = set()
        current_states = visited_states_a.difference(visited_states_b)
        while current_states:
            visited_states_b.update(visited_states_a)
            for state in current_states:
                try:
                    self.__table[state][""]
                except KeyError:
                    pass
                else:
                    visited_states_a.update(self.__table[state][""])
            current_states = visited_states_a.difference(visited_states_b)
        states.update(visited_states_a)
 
    def __get_new_states(self, states, symbol):
        new_states = set()
        for state in states:
            try:
                self.__table[state][symbol]
            except KeyError:
                pass
            else:
                new_states.update(self.__table[state][symbol])
        return new_states
                
        
    def evaluate(self, string):
        """
            returns:
                0 -> Match
                1 -> No match
        """
        states = self.__initial_states.copy()
        self.__get_new_states_e(states)
        for c in string:
            new_states = self.__get_new_states(states, c)
            self.__get_new_states_e(new_states)
            states = new_states
        return bool(states.intersection(self.__final_states))
 
    def print_fsm(self):
        print "Table:"
        for state in self.__table:
            for symbol in self.__table[state]:
                print "(%s, '%s') -> %s" % (state, symbol, self.__table[state][symbol])
                
        print "\nFinal States:"
        print self.__final_states
        print "\nInitial_states"
        print self.__initial_states
        print ""
 
fsm = FSM()
 
fsm.add_initial_states("q0")
 
"""
#Language a+b*
fsm.add_transition("q0", "a", "q1")
fsm.add_transition("q1", "a", "q1")
fsm.add_transition("q2", "b", "q2")
"""
 
#(a* | b*)
fsm.add_transition("q0", "", ["q1", "q2"])
fsm.add_transition("q1", "a", "q1")
fsm.add_transition("q2", "b", "q2")
 
 
fsm.add_final_states(("q1", "q2"))
 
fsm.print_fsm()
 
print fsm.evaluate("") #True
print fsm.evaluate("a") #True
print fsm.evaluate("aa") #True
print fsm.evaluate("aaa") #True
print fsm.evaluate("aaaa") #True
print fsm.evaluate("aaaaa") #True
print fsm.evaluate("aaaaaa") #True
print fsm.evaluate("ba") #False

