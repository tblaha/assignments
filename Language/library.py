from matplotlib import pyplot as plt
import os

def getattributes(name,path='.'): ## get all characteristic attributes of the sample text
    with open('{0}/{1}'.format(path,name), 'r') as myfile:
        fileasstring=myfile.read().replace('\n', ' ')
    fileasstring=fileasstring.replace('.', ' ')
    fileasstring=fileasstring.replace(',', ' ')
    fileasstring=fileasstring.replace(';', ' ')
    # --- char freq ---
    chars={}
    length=len(fileasstring)
    for a in range(0,256): # all chars
        chars[a] = float(fileasstring.count(chr(a)))/float(length)
    # --- word length ---
    spaces=fileasstring.count(' ')
    ratio=float(len(fileasstring)-float(spaces))/(float(spaces)+1)
    return [chars,ratio,name]

def stat(attributes,statspath): ## generate the stats file
    chars=attributes[0]
    ratio=attributes[1]
    name=attributes[2]
    with open('{0}/{1}_stats.txt'.format(statspath,name), 'w') as myfile:
        for key in chars.keys():
            myfile.write('{0} | {1}\n'.format(key, chars[key]))
        myfile.write('wl | {0}\n'.format(ratio))

def plot(name,statspath): ## plot a stats file
    attributes=readattributes(name,statspath)
    chars=attributes[0]
    ratio=attributes[1]
    name=attributes[2]
    plt.close()
    plt.plot(chars.keys(),chars.values())
    plt.title(name)
    plt.savefig('{0}/{1}_stats.png'.format(statspath,name))

def populatestats(samplespath,statspath):
    lst = os.listdir(samplespath)
    lst = lst
    for name in lst:
        if name.find('.txt') != -1:
            name = name.rstrip('.txt')
            stat(getattributes('{0}.txt'.format(name),samplespath),statspath)
            plot(name,statspath)

def readattributes(name,statspath): ## read the stats file to an attribute list
    chars={}
    with open('{0}/{1}_stats.txt'.format(statspath,name), 'r') as myfile:
        lines = myfile.readlines()
    for line in lines:
        line=line.strip()
        line = line.lower()
        # Check for wordlength line (wl) or  blank line
        if (line[0]+line[1])!='wl' and not line=="":
            words=line.split(' | ')
            chars[int(words[0])] = float(words[1])
        if (line[0]+line[1])=='wl':
            words=line.split(' | ')
            ratio=float(words[1])
    return [chars,ratio,name]

def compare(name_test,name_stats,statspath): ## compare existing sample file of language "name_stats" to attributes of the test text with name "name_test"
    attributes_stats = readattributes(name_stats,statspath) ## use existing list
    chars_stats      = attributes_stats[0]
    ratio_stats      = attributes_stats[1]
    attributes_test = getattributes(name_test) ## generate new list
    chars_test  = attributes_test[0]
    ratio_test  = attributes_test[1]
    sumofsquares=0
    i=0
    while i<len(chars_stats):
        sumofsquares += (chars_stats[i]-chars_test[i])**2
        i += 1
    return sumofsquares

def findlanguage(tobetested,statspath):
    lst = os.listdir(statspath)
    lst = lst
    squares = {}
    for name in lst:
        if name.find('_stats.txt') != -1:
            name = name.rstrip('_stats.txt')
            squares[name]=compare(tobetested,name,statspath)
    return min(squares, key=squares.get)
