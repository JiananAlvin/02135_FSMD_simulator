#!/usr/bin/env python3

import sys
import xmltodict

print("Welcome to the FSMD simulator! - Version ?? - Designed by ??")
# Make sure input 3 or 4 arguments: <fsmd-sim.py> <max_cycles> <description_file> <stimuli_file>
if len(sys.argv) < 3:
    print('Too few arguments.')
    sys.exit(-1)
elif (len(sys.argv) >4):
    print('Too many arguments.')
    sys.exit(-1)

iterations = int(sys.argv[1]) # Ensure the second argument <max_cycles> is int, not string

# Parsing the FSMD description file
with open(sys.argv[2]) as fd:
    fsmd_des = xmltodict.parse(fd.read())
# print("[fsmd_des]++++++++++++++++++++++++++++++++++++++++++++++")
# print(fsmd_des)
# print("[fsmd_des]++++++++++++++++++++++++++++++++++++++++++++++")

# Parsing the stimuli file
fsmd_stim = {}
if len(sys.argv) == 4:
    with open(sys.argv[3]) as fd:
        fsmd_stim = xmltodict.parse(fd.read())
# print("[fsmd_stim]++++++++++++++++++++++++++++++++++++++++++++++")
# print(fsmd_stim)
# print("[fsmd_stim]++++++++++++++++++++++++++++++++++++++++++++++")

print("\n--FSMD description--")

#
# Description:
# The 'states' variable of type 'list' contains the list of all states names.
#
states = fsmd_des['fsmddescription']['statelist']['state'] # Nested dict, ["key"]
print("States:")
for state in states:
    print('  ' + state)
#
# Description:
# The 'initial_state' variable of type 'string' contains the initial_state name.
#
initial_state = fsmd_des['fsmddescription']['initialstate']
print("Initial state:")
print('  ' + initial_state)   # INITIALIZE

#
# Description:
# The 'inputs' variable of type 'dictionary' contains the list of all inputs
# names and value. The default value is 0.
#
inputs = {}
if(fsmd_des['fsmddescription']['inputlist'] is None):
    inputs = {}
    # No elements
else:
    if type(fsmd_des['fsmddescription']['inputlist']['input']) is str:
        # 'str' means one element
        # Otherwise, should be a list ['in_A', 'in_B',...]
        # If one element, for example, 'in_A', inputs={'in_A':0}
        inputs[fsmd_des['fsmddescription']['inputlist']['input']] = 0
    else:
        # More elements
        for input_i in fsmd_des['fsmddescription']['inputlist']['input']:
            # inputs={'in_A':0, 'in_B':0, 'in_C':0,...}
            inputs[input_i] = 0
print("Inputs:")
for input_i in inputs:
    print('  ' + input_i)
"""print
Inputs:
  in_A
  in_B
"""
#
# Description:
# The 'variables' variable of type 'dictionary' contains the list of all variables
# names and value. The default value is 0.
#
variables = {}
if(fsmd_des['fsmddescription']['variablelist'] is None):
    variables = {}
    # No elements
else:
    if type(fsmd_des['fsmddescription']['variablelist']['variable']) is str:
        # One element
        variables[fsmd_des['fsmddescription']['variablelist']['variable']] = 0
    else:
        # More elements
        for variable in fsmd_des['fsmddescription']['variablelist']['variable']:
            variables[variable] = 0
# variables={'var_A':0, 'var_B':0, 'var_C':0,...}
print("Variables:")
for variable in variables:
    print('  ' + variable)

#
# Description:
# The 'operations' variable of type 'dictionary' contains the list of all the
# defined operations names and expressions.
#
operations = {}
if(fsmd_des['fsmddescription']['operationlist'] is None):
    operations = {}
    # No elements
# If one element, traverse dictionary, get each key of the dictionary.
# If more elements, traverse list, get each element(dict) of the list.
else:
    for operation in fsmd_des['fsmddescription']['operationlist']['operation']:
        # print("[dict]---------------------------------------------")
        # print(fsmd_des['fsmddescription']['operationlist']['operation'])
        # print("[dict]---------------------------------------------")
        if type(operation) is str:  # Judgement # operation is key
            # Only one element
            operations[fsmd_des['fsmddescription']['operationlist']['operation']['name']] = \
                fsmd_des['fsmddescription']['operationlist']['operation']['expression']
            # print("[key]++++++++++++++++++++++++++++++++++++++++++++++")
            # print(operation)
            # print("[key]++++++++++++++++++++++++++++++++++++++++++++++")
            break  # avoid repeated assignment. Otherwise, we will get two outputs "init_A : var_A = in_A"

        else:
            # More than 1 element
            # Operation is dict in this case "OrderedDict([('name', 'init_A'), ('expression', 'var_A = in_A')])"
            operations[operation['name']] = operation['expression']
print("Operations:")
for operation in operations:
    print('  ' + operation + ' : ' + operations[operation])

#
# Description:
# The 'conditions' variable of type 'dictionary' contains the list of all the
# defined conditions names and expressions.
#
conditions = {}
if(fsmd_des['fsmddescription']['conditionlist'] is None):
    conditions = {}
    #No elements
else:
    for condition in fsmd_des['fsmddescription']['conditionlist']['condition']:
        if type(condition) is str:
            #Only one element
            conditions[fsmd_des['fsmddescription']['conditionlist']['condition']['name']] = fsmd_des['fsmddescription']['conditionlist']['condition']['expression']
            break
        else:
            #More than 1 element
            conditions[condition['name']] = condition['expression']
print("Conditions:")
for condition in conditions:
    print('  ' + condition + ' : ' + conditions[condition])

#
# Description:
# The 'fsmd' variable of type 'dictionary' contains the list of dictionaries,
# one per state, with the fields 'condition', 'instruction', and 'nextstate'
# describing the FSMD transition table.
#
fsmd = {}
for state in states:   # state=INITIALIZE
    fsmd[state] = []   # fsmd{'INITIALIZE':[]}
    for transition in fsmd_des['fsmddescription']['fsmd'][state]['transition']:   # 3 key:value 'condition':'True', 'instructin':'init_A init_B', nextstate:'TEST'
        if type(transition) is str:    # transition is a dict, traverse each key
            #Only one element
            fsmd[state].append({'condition': fsmd_des['fsmddescription']['fsmd'][state]['transition']['condition'],
                                'instruction': fsmd_des['fsmddescription']['fsmd'][state]['transition']['instruction'],
                                'nextstate': fsmd_des['fsmddescription']['fsmd'][state]['transition']['nextstate']})
            # fsmd{'INITIALIZE':[{'condition':'True', 'instructin':'init_A init_B', nextstate:'TEST'}]}
            break
        else:
            #More than 1 element   # transition is a dict list, traverse each dict
            fsmd[state].append({'condition' : transition['condition'],
                                'instruction' : transition['instruction'],
                                'nextstate' : transition['nextstate']})
            # see 'TEST' output
print("FSMD transitions table:")
for state in fsmd:
    print('  ' + state)
    for transition in fsmd[state]:
        print('    ' + 'nextstate: ' + transition['nextstate'] + ', condition: ' + transition['condition'] + ', instruction: ' + transition['instruction'])

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#
# Description:
# This function executes a Python compatible operation passed as string
# on the operands stored in the dictionary 'inputs'
#
def execute_setinput(operation):   # in_A = 100
    operation_clean = operation.replace(' ', '')   # in_A=100
    operation_split = operation_clean.split('=')   # in_A    100
    target = operation_split[0]   # 'in_A'
    expression = operation_split[1]   # '100'
    inputs[target] = eval(expression, {'__builtins__': None}, inputs)   # execute expression eval(...)=100
    # 2nd {'__builtins__': None} ,  restrict the use of __builtins__ in the expression
    # 3rd inputs , In this program, expression can access to @inputs only. All other methods and variables are unavailable.
    # inputs={'in_A':100, 'in_B':0, 'in_C':0,...}
    return


#
# Description:
# This function executes a Python compatible operation passed as string
# on the operands stored in the dictionaries 'variables' and 'inputs'
#
def execute_operation(operation):  # var_A = 100(in_A)
    operation_clean = operation.replace(' ', '')
    operation_split = operation_clean.split('=')
    target = operation_split[0]   # var_A
    expression = operation_split[1]   # 100
    variables[target] = eval(expression, {'__builtins__': None}, merge_dicts(variables, inputs))
    # variables={'var_A':100, 'var_B':0, 'var_C':0,...}  # var_A = in_A
    return


#
# Description:
# This function executes a list of operations passed as string and spaced by
# a single space using the expression defined in the dictionary 'operations'
#
def execute_instruction(instruction):   # "init_A init_B A_minus_B B_minus_A"  # contain the operation(s) of the cycle
    # print("[instruction]++++++++++++++++++++++++++++++++++++++++++++++")
    # print(instruction)
    # print("[instruction]++++++++++++++++++++++++++++++++++++++++++++++")
    if instruction == 'NOP' or instruction == 'nop':   # no operations are performed in a given state
        return
    instruction_split = instruction.split(' ')   # ["init_A", "init_B", "A_minus_B", "B_minus_A"]
    for operation in instruction_split:  # for example, "init_A"
        execute_operation(operations[operation])   # execute "var_A = in_A"
    return


#
# Description:
# This function evaluates a Python compatible boolean expressions of
# conditions passed as string using the conditions defined in the variable 'conditions'
# and using the operands stored in the dictionaries 'variables' and 'inputs
# It returns True or False
#
def evaluate_condition(condition):  # condition: "True" "False" "A_equal_B" "A_greater_B" "B_greater_A "
    if condition == 'True' or condition=='true' or condition == 1:  # < <max_cycles> finish
        return True
    if condition == 'False' or condition=='false' or condition == 0:  # > <max_cycles>
        return False
    condition_explicit = condition  # condition: "A_equal_B" "A_greater_B" "B_greater_A "
    for element in conditions:   # element is key # conditions: {"A_equal_B": "var_A == var_B", "A_greater_B": "var_A > var_B", "B_greater_A": "var_A < var_B"}
        condition_explicit = condition_explicit.replace(element, conditions[element])
        # For example, replace ""A_equal_B" with "var_A == var_B"
    #print('----' + condition_explicit)
    return eval(condition_explicit, {'__builtins__': None}, merge_dicts(variables, inputs))


#
# Description:
# Support function to merge two dictionaries.
#
def merge_dicts(*dict_args):   # arbitrary numbers of arguments, *args tuple form, **kwargs dic form
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)   # add "dictionary" into result
    return result


#######################################
# Start to simulate
cycle = 0
state = initial_state   # will be changed with the cycle
repeat = True

print('\n---Start simulation---')

######################################
for cycle in range(iterations+1):
    try:
        if (not(fsmd_stim['fsmdstimulus']['setinput'] is None)):
            for setinput in fsmd_stim['fsmdstimulus']['setinput']:
                # print("[setinput]+++++++++++++++++++++++++++++++++++++++++")
                # print(setinput)
                # print("[setinput]+++++++++++++++++++++++++++++++++++++++++")
                if type(setinput) is str:
                    #Only one element
                    if int(fsmd_stim['fsmdstimulus']['setinput']['cycle']) == cycle:
                        execute_setinput(fsmd_stim['fsmdstimulus']['setinput']['expression'])
                    break
                else:
                    #More than 1 element
                    if int(setinput['cycle']) == cycle:
                        execute_setinput(setinput['expression'])
    except:
        pass


    try:
        if (not(fsmd_stim['fsmdstimulus']['endstate'] is None)):
            if state == fsmd_stim['fsmdstimulus']['endstate']:
                print('End-state reached.')
                repeat = False
    except:
        pass

    #Print information for each cycle:
    print('Cycle: ' + cycle)
    print('Current state: ' + state)
    condition = fsmd[state]['conditions']
    # for transition in fsmd[state]:
    #     if fsmd_des['fsmddescription']['fsmd'][state]['transition']['condition'] =



######################################
# Write your code here!
# WE CAN ONLY ONLY ONLY CHANGE CHILD TAGS!!!
######################################
######################################

print('\n---End of simulation---')

#
# Description:
# This is a code snippet used to update the inputs values according to the
# stimuli file content. You can see here how the 'fsmd_stim' variable is used.
#
'''
try:
    if (not(fsmd_stim['fsmdstimulus']['setinput'] is None)):
        for setinput in fsmd_stim['fsmdstimulus']['setinput']:
            if type(setinput) is str:
                #Only one element  # dict, traverse key
                if int(fsmd_stim['fsmdstimulus']['setinput']['cycle']) == cycle:
                    execute_setinput(fsmd_stim['fsmdstimulus']['setinput']['expression'])
                break
            else:
                #More than 1 element  # dict list, traverse dict
                if int(setinput['cycle']) == cycle:   #if cycle is 0
                    execute_setinput(setinput['expression'])   # execute "in_A=100"
except:
    pass
'''

#
# Description:
# This is a code snipppet used to check the endstate value according to the
# stimuli file content. You can see here how the 'fsmd_stim' variable is used.
#
'''
try:
    if (not(fsmd_stim['fsmdstimulus']['endstate'] is None)):
        if state == fsmd_stim['fsmdstimulus']['endstate']:
            print('End-state reached.')
            repeat = False
except:
    pass
'''
