import sys

#Main method
def main():
    #Read input file
    input = sys.argv[1]
    num_reg, issue_width, instructions = read_file(input)

    #Write output to 'out.txt'
    output = open('out.txt', 'w')
    output.write(str(num_reg) + '\n' + str(issue_width) + '\n' + str(instructions))
    output.close()

#Reads input file
def read_file(file):
    with open(file, 'r') as input:

        # Reads the first for the number of physical registers and the issue width
        num_reg, issue_width = map(int, input.readline().split(','))

        # Check if the number of physical registers is greater than 32
        if num_reg <= 32:
            return None

        # Parse each instruction and add it to the instructions list
        instructions = []
        for line in input:
            instruction = line.split(',')
            instructions.append(instruction)

    return num_reg, issue_width, instructions

#Calls main() on run
if __name__ == '__main__':
    main()