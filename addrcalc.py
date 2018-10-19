#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      cwhite
#
# Created:     08/01/2018
# Copyright:   (c) cwhite 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()


def addrcat(snum, sdir, sname, stype):
    snum = str(snum)
    sdir = str(sdir)
    sname = str(sname)
    stype = str(stype)
    streetaddress = ""
    if len(snum)>0 and snum != 'None':
        streetaddress = streetaddress+snum
    if len(sdir)>0 and sdir != 'None':
        streetaddress = streetaddress+" "+sdir
    if len(sname)>0 and sname != 'None':
        streetaddress = streetaddress + " " + sname
    if len(stype)>0 and stype != 'None':
        streetaddress = streetaddress + " " + stype
    return streetaddress