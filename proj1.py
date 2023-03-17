import sys

#Data Structures
map_table = [-1]*32
ready_table = []
free_list = []
reorder_buffer = []
instructions = []

#Global Variables 
num_reg = 0
issue_width = 0 
cycle = 0
commited = 0
fetch_index = 0
icount = 0

#Scheduling Queues
fetch = []
decode = []
rename = []
dispatch = []
issue = []
write_back = []
commit = []

#Main method
def main():
    global icount
    global commited
    global instructions
    global cycle

    #Read input file
    input = sys.argv[1]
    read_file(input)

    #Pipeline
    icount = len(instructions)
    while commited<icount:
        Commit()
        WB()
        Issue()
        Dispatch()
        Rename()
        Decode()
        Fetch()
        cycle+=1

    #Write output to 'out.txt'
    open('out.txt', 'w').close
    output = open('out.txt', 'a')
    for instruction in instructions:
        cycle_num = instruction[4]
        output.write(','.join(map(str,cycle_num)) + '\n')
    output.close()

#Reads input file
def read_file(file):
    with open(file, 'r') as input:

        # Reads the number of physical registers and the issue width
        num_reg, issue_width = map(int, input.readline().split(','))

        #Populates data structures as needed
        ready_table = [0]*num_reg

        # Parse each instruction and add it to the instructions list
        for line in input:
            instruction = line.strip().split(',')
            instruction.append([-1]*7)
            instructions.append(instruction)

    return

def Commit():
    global commited

    commited+=1
    return

def WB():
    return

def Issue():
    return

def Dispatch():
    return

def Rename():
    return

def Decode():
    return

def Fetch():
    global fetch_index

    fetch_index+=issue_width
    return

#Calls main() on run
if __name__ == '__main__':
    main()