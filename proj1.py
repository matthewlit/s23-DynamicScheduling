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
committed = 0
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
    global committed
    global instructions
    global cycle

    #Read input file
    input = sys.argv[1]
    read_file(input)

    #Pipeline
    icount = len(instructions)
    while committed<icount:
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
    global num_reg
    global issue_width
    global ready_table
    global instructions

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

#Commit Stage
def Commit():
    global committed
    global issue_width
    global cycle
    global write_back
    global commit

    #Add instructions to commit queue from write back queue
    for x in range(0, min(issue_width, len(write_back))):
        write_back[0][4][6] = cycle
        commit.append(write_back.pop(0))
        committed+=1
    return

#Write Back stage
def WB():
    global issue_width
    global cycle
    global issue
    global write_back

    #Add instructions to write back queue from issue queue
    for x in range(0, min(issue_width, len(issue))):
        issue[0][4][5] = cycle
        write_back.append(issue.pop(0))
    return

#Issue stage
#TODO: ADD STALLS
def Issue():
    global issue_width
    global cycle
    global issue
    global dispatch

    #Add instructions to issue queue from dispatch queue
    for x in range(0, min(issue_width, len(dispatch))):
        dispatch[0][4][4] = cycle
        issue.append(dispatch.pop(0))
    return

#Dispatch stage
#TODO: ADD STALLS
def Dispatch():
    global issue_width
    global cycle
    global rename
    global dispatch

    #Add instructions to dispatch queue from rename queue
    for x in range(0, min(issue_width, len(rename))):
        rename[0][4][3] = cycle
        dispatch.append(rename.pop(0))
    return

#Rename stage 
#TODO: ADD STALLS
def Rename():
    global issue_width
    global cycle
    global rename
    global decode

    #Add instructions to rename queue from decode queue
    for x in range(0, min(issue_width, len(decode))):
        decode[0][4][2] = cycle
        rename.append(decode.pop(0))
    return

#Decode stage
def Decode():
    global issue_width
    global cycle
    global fetch
    global decode

    #Add instructions to decode queue from fetch queue
    for x in range(0, min(issue_width, len(fetch))):
        fetch[0][4][1] = cycle
        decode.append(fetch.pop(0))
    return

#Fetch stage
def Fetch():
    global fetch_index
    global issue_width
    global cycle
    global fetch
    global instructions

    #Add instructions to fetch queue
    for x in range(fetch_index, min(fetch_index+issue_width, len(instructions))):
        instructions[x][4][0] = cycle
        fetch.append(instructions[x])

    #Update fetch index
    fetch_index+=issue_width
    return

#Calls main() on run
if __name__ == '__main__':
    main()