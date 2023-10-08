file = open("ramp.txt")
possible = []
for line in file:
    if len(line.strip("\n")) == 7 and 'l' not in line:
        possible.append(line)
print(possible)