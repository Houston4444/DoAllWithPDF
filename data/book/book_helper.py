#!/usr/bin/python3

import sys


#because of a weird behaviour of pdfjam, we need to give upper dimensions as wanted
def getUpperDimensions(Dimensions_list):
    UpperDimensions_list = []
    for Dimension in Dimensions_list:
        UpperDimensions_list.append(Dimension * 1.00375)
        
    return UpperDimensions_list
    
def getDimensions(Format, InputWidth, InputHeight, columns, lines):
    if Format == 'multiply':
        Dimensions = [ InputWidth * columns , InputHeight * lines ]
    
    elif Format == 'input':
        Dimensions = [ InputWidth, InputHeight ] 
            
    else:
        if Format == 'a4paper':
            Dimensions = [595.276, 841.89]
            
        elif Format == 'a3paper':
            Dimensions = [841.89, 1190.55]
                
        elif Format == 'a2paper':
            Dimensions = [1190.55, 1683.78]
        
        elif Format == 'letterpaper':
            Dimensions = [612, 792]
            
            
        if InputWidth * columns > InputHeight * lines:
            Dimensions.reverse()
            
    return Dimensions
            
def getMultiple(Format, InputWidth, InputHeight, columns, lines):
    Dimensions = getDimensions(Format, InputWidth, InputHeight, columns, lines)
    
    ratio_w = InputWidth  / (Dimensions[0] / columns)
    ratio_h = InputHeight / (Dimensions[1] / lines  )
    ratio_list = [ratio_w, ratio_h]    
    ratio_list.sort()
    
    return ratio_list[1]

def getFinalGutter(NumberOfPages, PageNumber, Multiple, Gutter):
    FinalGutter = 0.00
    NumberOfSheets = int(NumberOfPages / 4)
    
    little = 1
    big    = NumberOfPages
    sheet_list = []
    
    for x in range(NumberOfSheets):
        if RightToLeft:
            sheet_list.append([ little, big, big -1 , little +1 ])
        else:
            sheet_list.append([ big, little, little +1 , big -1 ])
        little += 2
        big    -= 2

    sheet_list.reverse()

    for x in range(len(sheet_list)):
        sheet = sheet_list[x]
        if PageNumber in sheet:
            if TopReverseLast and PageNumber == NumberOfPages:
                FinalGutter = -x * Gutter * Multiple
            elif TopFolding:
                if sheet.index(PageNumber) % 2 == 0:
                    FinalGutter = x * Gutter * Multiple
                else:
                    FinalGutter = -x * Gutter * Multiple
            else:
                if sheet.index(PageNumber) % 2 == 0:
                    FinalGutter = -x * Gutter * Multiple
                else:
                    FinalGutter = x * Gutter * Multiple
            break
    
    return FinalGutter

#######START#######
sheet_list = []  #sheet here is a final sheet of 4 pages, after cutting original sheets

arg_list = sys.argv[1:]
Option = None
Call   = None

InitialNumberOfPages = 1
Folding         = 'left'
NumberOfPages   = 4
nup             = '2x1'
gutter          = 0.00
outputformat    = 'a4paper'
InputDimensions = '595.276x841.89'
PagesPerSheet   = 4
PageNumber      = 1
PageTemplateMod = 'all'
blank_list      = []


for arg in arg_list:
    if arg.startswith('--'):
        Option = arg[2:]
        if Option in ('add_margin', 'get_page_gutter', 'get_nup', 'get_jam_dimensions', 
                      'get_pagetemplate', 'place_blanks', 'get_reversed_odd_tk'):
            Call = Option
            
    elif Option == 'folding':
        Folding = arg
    elif Option == 'numberofpages':
        NumberOfPages = int(arg)
    elif Option == 'initial_numberofpages':
        InitialNumberOfPages = int(arg)
    elif Option == 'nup':
        nup = arg
    elif Option == 'gutter':
        Gutter = float(arg)
    elif Option == 'outputformat':
        Format = arg
    elif Option == 'inputdimensions':
        InputDimensions = arg
    elif Option == 'pagespersheet':
        PagesPerSheet = int(arg)
    elif Option == 'pagenumber':
        PageNumber = int(arg)
    elif Option == 'blanklist':
        if arg in ('odd', 'even'):
            PageTemplateMod = arg
        elif not arg.isdigit():
            sys.exit(1)
        elif int(arg) in blank_list:
            sys.exit(1)
        else:
            blank_list.append(int(arg))
            
RightToLeft    = bool(Folding == 'right')
TopFolding     = bool(Folding.startswith('top'))
TopReverseLast = bool(Folding == 'top_reverse_last')
columns = int(nup.split('x')[0])
lines   = int(nup.split('x')[1])
InputWidth  = float(InputDimensions.split('x')[0])
InputHeight = float(InputDimensions.split('x')[1])


if Call == 'add_margin':
    Multiple = getMultiple(Format, InputWidth, InputHeight, columns, lines)
    MaxGutter = abs(getFinalGutter(NumberOfPages, 1, Multiple, Gutter))
    MaxGutter_pt = MaxGutter * 72 / 25.4
    if TopFolding:
        if MaxGutter_pt != 0:
            Merge_pt = InputHeight / ( (InputHeight / MaxGutter_pt) - 1)
        else:
            Merge_pt = 0
        FinalPapersize = '{' + str(InputWidth) + 'pt,' + str("%.3f" % (InputHeight + Merge_pt)) + 'pt}'
        offset_odd  = '0pt ' + str("%.3f" % (+Merge_pt / 2)) + 'pt'
        offset_even = '0pt ' + str("%.3f" % (-Merge_pt / 2)) + 'pt'
    else:
        if MaxGutter_pt != 0:
            Merge_pt = InputWidth / ((InputWidth / MaxGutter_pt) - 1)
        else:
            Merge_pt = 0
        FinalPapersize = '{' + str("%.3f" % (InputWidth + Merge_pt)) + 'pt,' + str(InputHeight) + 'pt}'
        offset_odd  = str("%.3f" % (-Merge_pt /2)) + 'pt 0pt'
        offset_even = str("%.3f" % (Merge_pt /2)) + 'pt 0pt'
            
    print(FinalPapersize)
    print(offset_odd)
    print(offset_even)
    sys.exit(0)
    
elif Call == 'get_page_gutter':
    #set gutter to 0.00 if PageNumber is an empty page        
    if PageNumber in blank_list:
        print("0.00")
        sys.exit(0)

    Multiple = getMultiple(Format, InputWidth, InputHeight, columns, lines)
    FinalGutter = getFinalGutter(NumberOfPages, PageNumber, Multiple, Gutter)
        
    print("%.2f" % FinalGutter)

elif Call == 'get_nup':
    if PagesPerSheet == 4:
        if TopFolding:
            columns = 1
            lines   = 2
        else:
            columns = 2
            lines   = 1
    
    elif PagesPerSheet == 8:
        columns = 2
        lines   = 2
        
    elif PagesPerSheet == 16:
        if InputWidth > InputHeight:
            columns = 2
            lines   = 4
        else:
            columns = 2
            lines   = 4
    
    print(str(columns) + 'x' + str(lines))
    
elif Call == 'get_jam_dimensions':
    Dimensions = getDimensions(Format, InputWidth, InputHeight, columns, lines)
    UpperDimensions = getUpperDimensions(Dimensions)
    JamDimensions = '{' + str(UpperDimensions[0]) + 'pt,' + str(UpperDimensions[1]) + 'pt} '
    print(JamDimensions)
    
elif Call == 'get_pagetemplate':
    def getOddEvenPlace(PageTemplateMod, c):
        if PageTemplateMod == 'all':
            return c
        elif PageTemplateMod == 'odd':
            return (c*2)-1
        elif PageTemplateMod == 'even':
            return c*2
        
    c=1
    while getOddEvenPlace(PageTemplateMod, c) in blank_list:
        c+=1
    
    if PageTemplateMod == 'all':
        if c > NumberOfPages:
            c=1
    else:
        if c > NumberOfPages/2:
            c=1
    
    print(c)
    
elif Call == 'place_blanks':
    class tkstring_dict_t(object):
        __slots__ = [
            'min',
            'max' ]
        
    if NumberOfPages != InitialNumberOfPages + len(blank_list):
        sys.exit(1)
        
    tkstring_list = []
    first_page_of_list = 1
    n = 0
    
    blank_list.sort()

    #make all tkstring except last
    for blank_num in blank_list:
        if blank_num > NumberOfPages:
            sys.exit(1)
        tkstring = tkstring_dict_t()
        tkstring.min = first_page_of_list
        tkstring.max = blank_num -1 - n
        tkstring_list.append(tkstring)
        first_page_of_list = tkstring.max + 1
        n+=1
        
    #make last tkstring
    tkstring = tkstring_dict_t()
    tkstring.min = first_page_of_list
    tkstring.max = InitialNumberOfPages
    tkstring_list.append(tkstring)
    
    final_string = ''
    n = 0

    #make final string
    for tkstring in tkstring_list:
        if tkstring.max > tkstring.min:
            final_string += ' A' + str(tkstring.min) + '-' + str(tkstring.max)
        elif tkstring.max == tkstring.min:
            final_string += ' A' + str(tkstring.min)
        else:
            pass
            
        if n < len(blank_list):
            final_string += ' B'
            
        n+=1    
            
    print(final_string)   
    
elif Call == 'get_reversed_odd_tk':
    NumberOfSides = NumberOfPages // (lines*columns)
    tkstring = ''
    
    for i in range(1, NumberOfSides+1):
        if i % 2 == 1:
            tkstring += str(i) + 'down '
        else:
            tkstring += str(i) + ' '
            
    print(tkstring)
            
    
    
sys.exit(0)
    
