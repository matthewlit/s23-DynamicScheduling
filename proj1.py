import sys

#Data Structures
map_table, ready_table, free_list, reorder_buffer, load_store_queue, instructions, free = [], [], [], [], [], [], []
#Global Variables 
num_reg, issue_width, cycle, committed, fetch_index, icount = 0,0,0,0,0,0
#Scheduling Queues
fetch, decode, rename, dispatch, issue, write_back, commit = [], [], [], [], [], [], []

#Main method
def main():
    global icount
    global committed
    global instructions
    global cycle
    global issue
    global free_list
    global free

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

        #Free over-written registers
        for x in range(len(free)):
            free_list.append(free.pop(0))

        #Set registers to ready
        for instruction in issue:
            ready_table[instruction[1]] = 1

        #Next cycle
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
    global free_list
    global instructions
    global map_table

    with open(file, 'r') as input:

        # Reads the number of physical registers and the issue width
        num_reg, issue_width = map(int, input.readline().split(','))

        #Populates data structures as needed
        ready_table = [1]*num_reg
        free_list = [*range(32,num_reg,1)]
        for x in range(32):
            map_table.append(str(x))
        for x in range(num_reg-32):
            map_table.append('-1')

        # Parse each instruction and add it to the instructions list
        for line in input:
            instruction = line.strip().split(',')
            instruction.append([-1]*7)
            instruction.append(-1)
            instructions.append(instruction)

    return

#Commit Stage
def Commit():
    global committed
    global issue_width
    global cycle
    global write_back
    global commit
    global free
    global reorder_buffer

    #Add instructions to commit queue from write back queue
    for x in range(0, min(issue_width, len(reorder_buffer))):
        if reorder_buffer[0] in write_back:
            reorder_buffer[0][4][6] = cycle
            if reorder_buffer[0][5]!=-1: free.append(reorder_buffer[0][5])
            commit.append(reorder_buffer.pop(0))
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
def Issue():
    global issue_width
    global cycle
    global issue
    global dispatch
    global ready_table

    #Add instructions to issue queue from dispatch queue
    issued = 0
    index = 0
    store = 0
    while issued<issue_width and index != len(dispatch):
        if store==0 or (dispatch[index][0]!='L' and store==1):
            if ready(dispatch[index])!=-1:
                dispatch[index][4][4] = cycle
                instruction = dispatch.pop(index)
                issue.append(instruction)
                if instruction[0]=='S':
                    store = 1
                issued+=1
            #Stall
            else: index+=1
        else:
            return
    return

#Dispatch stage
def Dispatch():
    global issue_width
    global cycle
    global rename
    global dispatch
    global reorder_buffer
    global load_store_queue
    global ready_table

    #Add instructions to dispatch queue, reorder buffer, and load store queue from rename queue
    for x in range(0, min(issue_width, len(rename))):
        rename[0][4][3] = cycle

        #Clear ready bit for destination
        ready_table[rename[0][1]] = 0

        instruction = rename.pop(0)
        dispatch.append(instruction)
        reorder_buffer.append(instruction)
        if instruction[0] == 'L' or instruction[0] == 'S':
            load_store_queue.append(instruction)
    return

#Rename stage 
def Rename():
    global issue_width
    global cycle
    global rename
    global decode

    #Add instructions to rename queue from decode queue
    issued = 0
    index = 0
    while issued<issue_width and index != len(decode):
        if mapped(decode[index])!=-1:
            decode[index][4][2] = cycle
            rename.append(decode.pop(index))
            issued+=1
        #Stall
        else: return
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

#Check if registers are mapped
def mapped(instruction):
    global map_table
    global free_list

    #Get phy register numbers
    reg1 = instruction[1]
    reg2 = -1
    reg3 = -1
    if instruction[0] == 'R':
        reg2 = instruction[2]
        reg3 = instruction[3]
    elif instruction[0] == 'I':
        reg2 = instruction[2]
    else:
        reg2 = instruction[3]

    #Check if can be mapped
    num_to_be_mapped = 1
    if reg2 not in map_table: num_to_be_mapped+=1
    if reg3!=-1 and reg3 not in map_table: num_to_be_mapped+=1
    if len(free_list)<num_to_be_mapped: return -1

    #Check if reg2 is mapped
    if reg2 not in map_table:
        arch_reg = get_reg()
        if arch_reg!=-1: 
            map_table[arch_reg] = reg2
            if instruction[0] == 'I' or instruction[0] == 'R': instruction[2] = arch_reg
            else: instruction[3] = arch_reg
        else: return -1
    else:
        if instruction[0] == 'I': instruction[2] = map_table.index(reg2)
        elif instruction[0] == 'R': instruction[2] = map_table.index(reg2)
        else: instruction[3] = map_table.index(reg2)

    #Check if reg3 is mapped
    if reg3!=-1 and reg3 not in map_table:
        arch_reg = get_reg()
        if arch_reg!=-1: 
            map_table[arch_reg] = reg3
            instruction[3] = arch_reg
        else: return -1
    elif reg3!=-1 and reg3 in map_table:
        instruction[3] = map_table.index(reg3)

    #Check if reg1 is mapped
    if reg1 not in map_table:
        arch_reg = get_reg()
        if arch_reg!=-1: 
            map_table[arch_reg] = reg1
            instruction[1] = arch_reg
        else: return -1
    elif reg1 in map_table and instruction[0]!='S':
        instruction[5] = map_table.index(reg1)
        map_table[map_table.index(reg1)] = -1
        arch_reg = get_reg()
        if arch_reg!=-1:
            map_table[arch_reg] = reg1
            instruction[1] = arch_reg
        else: return -1
    elif reg1 in map_table and instruction[0]=='S':
        instruction[1] = map_table.index(reg1)

    #All registers mapped
    return 1


#Map physical register to architected register
def get_reg():
    global free_list

    if len(free_list)>0:
        return free_list.pop(0)

    #Could not be mapped
    return -1

def ready(instruction):
    global ready_table

    if instruction[0] == 'R':
        if ready_table[instruction[2]]==1 and ready_table[instruction[3]]==1: return 1
        else: return -1
    elif instruction[0] == 'I':
        if ready_table[instruction[2]]==1: return 1
        else: return -1
    elif instruction[0] == 'S':
        if ready_table[instruction[1]]==1 and ready_table[instruction[3]]==1: return 1
        else: return -1
    elif instruction[0] == 'L':
        if ready_table[instruction[3]]==1: return 1
        else: return -1

#Calls main() on run
if __name__ == '__main__':
    main()