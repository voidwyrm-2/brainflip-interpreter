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

def stringify(list):
    out = ''
    for l in list: out += list
    return out

def processcode(line: str | list[str] | tuple[str] | dict[any, str]):
    if type(line) == dict: line = list(line.values())
    if type(line) in (list, tuple): line = stringify(line)
    line = truncatecode(line)
    if debug: print('truncated code:\n' + line)
    line = line.replace('\n', '').replace(' ', '').strip()
    global value
    if line.count('[') != line.count(']'): print('Error: expected "[" to close "]"'); raise SystemExit()
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
        if datapointer > len(databytes) - 1: datapointer = 0
        if datapointer < -(len(databytes) - 1): datapointer = len(databytes) - 1
        char = line[c]
        #if debug:
        #   print('char:', char + '; cn:', c + 1)
        #   print('dp, b:', str(datapointer) + ',', str(databytes[datapointer]))
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
                if useinp.isdigit(): databytes[datapointer] = int(useinp); waiting = False; break
                else: print('that\'s not a digit!')
            if not waiting: c += 1
        else: c += 1
        #cutoff += 1
        #if cutoff >= 1000: raise SystemExit()


def truncatecode(inp: str):
    inp = inp.replace('\n', '').replace(' ', '')
    out = ''
    for char in inp:
        if char in '+-><[].,': out += char
    return out



helloworld = '++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.'



commandcache = ''
uselast = False
truncate = False
def shell():
    global truncate
    global uselast
    global commandcache
    running = True
    while running:
        if uselast and commandcache not in (' ', '', None): inp = commandcache
        else: inp = input('>>> ')
        if inp != (' ', '', None): commandcache = inp
        if inp.endswith((' --trunc', ' --truncate')): truncate = True; inp = inp.removesuffix(' --trunc').removesuffix(' --truncate')
        #print('trunc:', truncate)
        if inp == 'exit': raise SystemExit()
        elif inp.startswith('run '):
            if truncate: print(truncatecode(inp.removeprefix('run ')))
            else: processcode(inp.removeprefix('run '))
        elif inp in ('hw', 'helloworld', 'hello world'): processcode(helloworld)
        elif inp.startswith('file '):
            path = inp.removeprefix('file ')
            path = path.strip('.b').strip('.bf')
            if Path(path + '.b').exists(): path = path + '.b'
            else:
                if Path(path + '.bf').exists(): path = path + '.bf'
                else: print(f'file "{path}" does not exist'); raise SystemExit()
            fin = ''
            with open(path, 'rt') as file: fin = file.read()
            if truncate: print(truncatecode(fin))
            else: processcode(fin)
        #elif inp == 'last': uselast = True; truncate = False; continue
        elif inp.startswith('search '):
            term = inp.removeprefix('search ')
            for key in ASCIIDICT.keys():
                if ASCIIDICT[key] == term: print(f'{key}: "{ASCIIDICT[key]}"')
        elif inp == 'listascii':
            for key in ASCIIDICT.keys(): print(f'{key}: "{ASCIIDICT[key]}"')
        else: print(f'unknown command "{inp.split(" ")[0]}"')
    uselast = False
    truncate = False



if __name__ == '__main__': shell()