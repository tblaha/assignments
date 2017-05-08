import numpy as np

while True:
    try:
        h_in=int(raw_input("Enter hours (Range 0-23): "))
        m=int(raw_input("Enter minutes (Range 0-59):"))
        if h_in>23 or h_in<0 or m>59 or m<0:
            print "There was at least one out of range number, try again!"
            continue
        h=h_in%12
        break
    except ValueError:
        print "There was at least one non-integer number, try again!"
        continue

a_h=360*((float(h)*60.+float(m))/(12.*60.))
a_m=360*(float(m)/60.)

print
print 'Hour hand makes the angle %.2f degree with the 12 position' % a_h
print 'Minute hand makes the angle %.2f degree with the 12 position' % a_m
