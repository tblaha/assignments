from library import *

samplespath='./samples'
statspath='./samples/stats'
tobetested='./moretests/test2.txt'

populatestats(samplespath,statspath)
print findlanguage(tobetested,statspath)
