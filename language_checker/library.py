from matplotlib import pyplot as plt
import os

##############################################################################
# Standalone functions
##############################################################################

#--- General: get attribute of any text. ---
def getattributes(name,path='.'): ## get all characteristic attributes of the sample text
    with open('{0}/{1}.txt'.format(path,name), 'r') as myfile:                                     ## <---- NEW
        fileasstring=myfile.read().replace('\n', ' ')                                     ## <---- NEW
    fileasstring=fileasstring.replace('.', ' ')                                     ## <---- NEW
    fileasstring=fileasstring.replace(',', ' ')                                     ## <---- NEW
    fileasstring=fileasstring.replace(':', ' ')                                     ## <---- NEW
    fileasstring=fileasstring.replace(';', ' ')                                     ## <---- NEW
    fileasstring=fileasstring.replace('?', ' ')                                     ## <---- NEW
    fileasstring=fileasstring.replace('!', ' ')                                     ## <---- NEW
    fileasstring=fileasstring.replace(chr(34), ' ')                                     ## <---- NEW
    fileasstring=fileasstring.replace(chr(39), ' ')                                     ## <---- NEW
    # --- word length ---
    spaces=fileasstring.count(' ')                                     ## <---- NEW
    ratio=float(len(fileasstring)-float(spaces))/(float(spaces)+1)
    # --- char freq ---
    fileasstring=fileasstring.replace(' ', '')                                     ## <---- NEW
    chars={}
    length=len(fileasstring)
    for a in range(0,256): # all chars
        chars[a] = float(fileasstring.count(chr(a)))/float(length)
    return [name,chars,ratio]

#--- Make a stats file for an analysed text, ie learn a language
def stats(attributes,statspath): ## generate the stats file
    name=attributes[0]
    chars=attributes[1]
    ratio=attributes[2]
    with open('{0}/{1}_stats.txt'.format(statspath,name), 'w') as myfile:                                     ## <---- NEW
        for key in chars.keys():                                     ## <---- NEW
            myfile.write('{0} | {1}\n'.format(key, chars[key]))                                     ## <---- NEW
        myfile.write('wl | {0}\n'.format(ratio))                                     ## <---- NEW

#--- make a single png plot for a fingerprint of a leant language
def plot(attributes,statspath): ## plot a stats file
    name=attributes[0]
    chars=attributes[1]
    ratio=attributes[2]
    plt.clf()
    plt.plot(chars.keys(),chars.values())                                     ## <---- NEW
    plt.title(name)                                     ## <---- NEW
    plt.savefig('{0}/{1}_stats.png'.format(statspath,name))                                     ## <---- NEW

#--- append to dynamic plot for user output
def plot_append(attributes,rows,columns,location,fig,color=None):
    name=attributes[0]
    chars=attributes[1]
    ratio=attributes[2]
    sc = fig.add_subplot(rows,columns,location)
    if color:
        sc.plot(chars.keys(),chars.values(),'C1')
    else:
        sc.plot(chars.keys(),chars.values())
    sc.set_title(name)
    return fig


#--- read attributes from an already existing language stats file ("fingerprint" file)
def readattributes(name,statspath): ## read the stats file to an attribute list
    chars={}
    with open('{0}/{1}_stats.txt'.format(statspath,name), 'r') as myfile:
        lines = myfile.readlines()                                     ## <---- NEW

    for line in lines:
        line=line.strip()                                     ## <---- NEW
        line = line.lower()                                     ## <---- NEW
        if not line=="":
            words=line.split(' | ')
            if (line[0]+line[1])=='wl':
                ratio=float(words[1])
            else:
                chars[int(words[0])] = float(words[1])
    return [name,chars,ratio]



##############################################################################
# Composite functions
##############################################################################

#--- routine that populates the directiory with the fingerprints of the languages (in .txt and .png) ---
def populatestats(samplespath,statspath):
    lst = os.listdir(samplespath)
    lst = lst
    for name in lst:
        if name.find('.txt') != -1:
            name = name.rstrip('.txt')                                     ## <---- NEW
            attributes = getattributes(name,samplespath)
            stats(attributes,statspath)
            plot(attributes,statspath)

#--- compare a test text and a known language and output the sum of the squares of the differences ---
def compare(name_test,name_stats,statspath): ## compare existing sample file of language "name_stats" to attributes of the test text with name "name_test"
    attributes_stats = readattributes(name_stats,statspath) ## use existing stats of known languages
    attributes_test  = getattributes(name_test) ## generate new stats for the test text
    chars_stats      = attributes_stats[1]
    ratio_stats      = attributes_stats[2]
    chars_test  = attributes_test[1]
    ratio_test  = attributes_test[2]
    sumofsquares=0
    i=0
    while i<len(chars_stats):
        sumofsquares += (chars_stats[i]-chars_test[i])**2
        i += 1
    return sumofsquares

#--- find the most probable language and also plot the stuff ---
def findlanguage(tobetested,statspath):
    lst = os.listdir(statspath)
    lst = lst
    squares = {}
    for statsfile in lst:
        if statsfile.find('_stats.txt') != -1:
            statsfile = statsfile.rstrip('_stats.txt')
            squares[statsfile]=compare(tobetested,statsfile,statspath)
    print "Based on the frequency of the characters occuring, the language of {0}.txt is most probably:".format(tobetested) + "\n             ",
    print min(squares, key=squares.get)   ## <---- NEW

    plt.close('all')
    fig = plt.figure()
    fig = plot_append(getattributes(tobetested),4,3,1,fig,'red')
    k=4
    for statsfile in lst:
        if statsfile.find('_stats.txt') != -1:
            statsfile = statsfile.rstrip('_stats.txt')
            fig = plot_append(readattributes(statsfile,statspath),4,3,k,fig)
            k += 1
    fig.tight_layout()
    plt.savefig('{0}_compare.png'.format(tobetested))
    plt.show()





