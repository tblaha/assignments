from library import *

samplespath='./samples'
statspath='./samples/stats'
tobetested='./tests/test1' #w/o .txt

populatestats(samplespath,statspath)
findlanguage(tobetested,statspath)
