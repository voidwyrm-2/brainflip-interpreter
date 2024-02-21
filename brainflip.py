from pathlib import Path



ASCIIDICT = {i: chr(i) for i in range(128)}



def listclamp(value, max):
    if value > max: return max
    elif value < 0: return 0
    else: return value

def zeroin(value): return 0 if value < 0 else value

def lenroof(value, listlen): return listlen - 1 if value > listlen else value


debug = False


startingbytes = 30000
databytes = []
for i in range(startingbytes): databytes.append(0)

datapointer = 0



def processcodeline(line: str | list[str]):
    global datapointer
    if type(line) == str: line = list(line)
    line.insert(0, ' ')
    pairnests = 0
    jumps = {}
    curbegins = []
    for p in range(len(line)):
        pc = line[p]
        if pc == '[': pairnests += 1; curbegins.append(p)
        elif pc == ']' and pairnests > 0:
            pairnests -= 1
            jumps[curbegins[-1]] = p
            jumps[p] = curbegins[-1]
            del curbegins[-1]

    #cutoff = 0
    c = 0
    while c != len(line):
        char = line[c]
        if debug:
            print('char:', char + '; cn:', c + 1)
            #print('dp, b:', str(datapointer) + ',', str(databytes[datapointer]))
        if char == '+': databytes[datapointer] += 1; c += 1
        elif char == '-': databytes[datapointer] -= 1; c += 1
        elif char == '>': datapointer += 1; c += 1
        elif char == '<': datapointer -= 1; c += 1
        elif char == '[':
            if databytes[datapointer] == 0: c = jumps[c] + 1 # command after the matching ]
            else: c += 1
            #continue
        elif char == ']':
            if databytes[datapointer] != 0: c = jumps[c] + 1 # command after the matching [
            else: c += 1
            #continue
        elif char == '.': print(ASCIIDICT[databytes[datapointer]]); c += 1
        elif char == ',':
            waiting = True
            while waiting:
                useinp = input('waiting for user input...\n')
                if useinp.isdigit(): databytes[datapointer] == int(useinp); waiting = False; break
                else: print('that\'s not a digit!')
            c += 1
        else: c += 1
        #cutoff += 1
        #if cutoff >= 1000: raise SystemExit()



def processcode(lines: str | list[str]):
    lines = lines.strip()
    global value
    if lines.count('[') != lines.count(']'): print('Error: expected "[" to close "]"'); raise SystemExit()
    if type(lines) != list: lines = lines.split('\n')
    for l in range(len(lines)): processcodeline(lines[l])

helloworld = '++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.'

def shell():
    running = True
    while running:
        inp = input('>>> ')
        if inp == 'exit': raise SystemExit()
        elif inp.startswith('run '): processcode(inp.removeprefix('run '))
        elif inp in ('hw', 'helloworld', 'hello world'): processcode(helloworld)
        elif inp in ('hwi', 'helloworldindex', 'hello world index'):
            hw = list(helloworld)
            for cha in range(len(hw)):
                ch = hw[cha]
                print(f'{cha + 1}: {ch}')
        elif inp.startswith('file '):
            path = inp.removeprefix('file ')
            path = path.strip('.b').strip('.bf')
            if Path(path + '.b').exists(): path = path + '.b'
            else:
                if Path(path + '.bf').exists(): path = path + '.bf'
                else: print(f'file "{path}" does not exist'); raise SystemExit()
            fin = ''
            with open(path, 'rt') as file: fin = file.read()
            processcode(fin)
        else: print(f'unknown command "{inp.split(" ")[0]}"')



if __name__ == '__main__': shell()