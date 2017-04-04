#!/usr/bin/python3

import sys

sheetside_list = []
tkstring = ''

class sheetside_dict_t(object):
    __slots__ = [
        'pages',    #for  4 pages per sheet
        'top',      #for  8 pages per sheet
        'bottom',
        'left',
        'right',
        'top_left', #for 16 pages per sheet, input portrait
        'top_right',
        'bottom_left', 
        'bottom_right',
        'top_up',   #for 16 pages per sheet, input landscape
        'top_middle',
        'bottom_middle',
        'bottom_down',
        'left_middle',
        'right_middle' ]
    
RightToLeft    = bool(str(sys.argv[1]) == 'right')
FoldingTop      = bool(str(sys.argv[1]).startswith('top'))
TopReverseLast = bool(str(sys.argv[1]) == 'top_reverse_last')
NumberOfPages  = int(sys.argv[2])
nup            = str(sys.argv[3])

nup_list = nup.split('x') 
PagesPerSheet = int(nup_list[0]) * int(nup_list[1]) * 2


NumberOfSides = int(NumberOfPages / (PagesPerSheet/2))
#print(Landscape, PagesPerSheet, NumberOfPages, NumberOfSides)

little = 1
big    = NumberOfPages

if nup == '1x2':
    #induces FoldingTop = True 
    for c in range(NumberOfSides):
        sheetside = sheetside_dict_t()
        sheetside.pages = [ little, big ]
        sheetside_list.append(sheetside)
        
        little += 1
        big    -= 1
    
    for c in range(len(sheetside_list)):
        sheetside = sheetside_list[c]
        
        if c % 2 == 0:
            for page_num in sheetside.pages:
                if TopReverseLast and page_num == NumberOfPages:
                    tkstring += str(page_num) + ' '
                else:
                    tkstring += str(page_num) + 'down '
        else:
            for page_num in sheetside.pages:
                tkstring += str(page_num) + ' '
         
elif nup == '2x1':
    #induces FoldingTop = False
    for c in range(NumberOfSides):
        sheetside = sheetside_dict_t()
        
        d = c+1 if RightToLeft else c
        
        if d % 2 == 0:
            sheetside.pages = [ big, little ]
        else:
            sheetside.pages = [ little, big ]
            
        sheetside_list.append(sheetside)
        
        little += 1
        big    -= 1
    
    for sheetside in sheetside_list:
        for page_num in sheetside.pages:
            tkstring += str(page_num) + ' '
                        

elif nup == '2x2':
    if FoldingTop:
        for c in range(NumberOfSides):
            sheetside = sheetside_dict_t()
            
            if c % 2 == 0:
                sheetside.left  = [ little, big ]
            else:
                sheetside.right = [ little, big ]
                
            sheetside_list.append(sheetside)
            
            little += 1
            big    -= 1
            
        sheetside_list.reverse()
        
        for c in range(len(sheetside_list)):
            sheetside = sheetside_list[c]
            
            if c % 2 == 0:
                sheetside.left  = [ little, big ]
            else:
                sheetside.right = [ little, big ]
                
            little += 1
            big    -= 1
            
        sheetside_list.reverse()
        
        for sheetside in sheetside_list:
            for page_num in sheetside.left:
                if TopReverseLast and page_num == NumberOfPages:
                    tkstring += str(page_num) + ' '
                else:
                    tkstring += str(page_num) + 'down '
                    
            for page_num in sheetside.right:
                tkstring += str(page_num) + ' '
            
    else:
        for c in range(NumberOfSides):
            sheetside = sheetside_dict_t()
            d = c+1 if RightToLeft else c
            
            if d % 2 == 0:
                sheetside.bottom = [ big, little ]
            else:
                sheetside.bottom = [ little, big ]
                
            sheetside_list.append(sheetside)
            
            little += 1
            big    -= 1

        sheetside_list.reverse()

        for c in range(len(sheetside_list)):
            sheetside = sheetside_list[c]
            d = c+1 if RightToLeft else c
            
            if d % 2 == 0:
                sheetside.top = [ little, big ]
            else:
                sheetside.top = [ big, little ]
                
            little += 1
            big    -= 1
                
        sheetside_list.reverse()

        for sheetside in sheetside_list:    
            for page_num in sheetside.top:
                tkstring += str(page_num) + 'down '
                
            for page_num in sheetside.bottom:
                tkstring += str(page_num) + ' '
        
            
elif nup == '4x2':
    if FoldingTop:
        for c in range(NumberOfSides):
            sheetside = sheetside_dict_t()
            
            if c % 2 == 0:
                sheetside.left  = [ little, big ]
            else:
                sheetside.right = [ little, big ]
                
            sheetside_list.append(sheetside)
            
            little += 1
            big    -= 1
            
        sheetside_list.reverse()
        
        for c in range(len(sheetside_list)):
            sheetside = sheetside_list[c]
            
            if c % 2 == 0:
                sheetside.left  = [ little, big ]
            else:
                sheetside.right = [ little, big ]
    
            little += 1
            big    -= 1
            
        sheetside_list.reverse()
        
        for c in range(len(sheetside_list)):
            sheetside = sheetside_list[c]
            
            if c % 2 == 0:
                sheetside.right_middle = [ little, big ]
            else:
                sheetside.left_middle  = [ little, big ]
    
            little += 1
            big    -= 1
            
        sheetside_list.reverse()
        
        for c in range(len(sheetside_list)):
            sheetside = sheetside_list[c]
            
            if c % 2 == 0:
                sheetside.right_middle = [ little, big ]
            else:
                sheetside.left_middle  = [ little, big ]
    
            little += 1
            big    -= 1
            
        sheetside_list.reverse()
        
        for sheetside in sheetside_list:
            for page_num in sheetside.left:
                if TopReverseLast and page_num == NumberOfPages:
                    tkstring += str(page_num) + ' '
                else:
                    tkstring += str(page_num) + 'down '
                    
            for page_num in sheetside.left_middle:
                tkstring += str(page_num) + ' '
                
            for page_num in sheetside.right_middle:
                tkstring += str(page_num) + 'down '
                
            for page_num in sheetside.right:
                tkstring += str(page_num) + ' '
            
    else:
        for c in range(NumberOfSides):
            sheetside = sheetside_dict_t()
            d = c+1 if RightToLeft else c
            
            if d % 2 == 0:
                sheetside.bottom_right = [ big, little ]
            else:
                sheetside.bottom_left  = [ little, big ]
                
            sheetside_list.append(sheetside)
            
            little += 1
            big    -= 1
            
        sheetside_list.reverse()
        
        for c in range(len(sheetside_list)):
            sheetside = sheetside_list[c]
            d = c+1 if RightToLeft else c
            
            if d % 2 == 0:
                sheetside.bottom_right = [ big, little ]
            else:
                sheetside.bottom_left  = [ little, big ]
                
            little += 1
            big    -= 1
        
        sheetside_list.reverse()
        
        for c in range(len(sheetside_list)):
            sheetside = sheetside_list[c]
            d = c+1 if RightToLeft else c
            
            if d % 2 == 0:
                sheetside.top_left  = [ little, big ]
            else:
                sheetside.top_right = [ big, little ]
                
            little += 1
            big    -= 1
        
        sheetside_list.reverse()
        
        for c in range(len(sheetside_list)):
            sheetside = sheetside_list[c]
            d = c+1 if RightToLeft else c
            
            if d % 2 == 0:
                sheetside.top_left  = [ little, big ]
            else:
                sheetside.top_right = [ big, little ]
                
            little += 1
            big    -= 1
            
        sheetside_list.reverse()
        
        for sheetside in sheetside_list:    
            for page_num in sheetside.top_left:
                tkstring += str(page_num) + 'down '
                
            for page_num in sheetside.top_right:
                tkstring += str(page_num) + 'down '
                
            for page_num in sheetside.bottom_left:
                tkstring += str(page_num) + ' '
        
            for page_num in sheetside.bottom_right:
                tkstring += str(page_num) + ' '

elif nup == '2x4':
    if FoldingTop:
            for c in range(NumberOfSides):
                sheetside = sheetside_dict_t()
                
                if c % 2 == 0:
                    sheetside.top_left  = [ little, big ]
                else:
                    sheetside.top_right = [ little, big ]
                    
                sheetside_list.append(sheetside)
                
                little += 1
                big    -= 1
                
            sheetside_list.reverse()
            
            for c in range(len(sheetside_list)):
                sheetside = sheetside_list[c]
                
                if c % 2 == 0:
                    sheetside.bottom_right = [ big, little ]
                else:
                    sheetside.bottom_left  = [ big, little ]
        
                little += 1
                big    -= 1
                
            sheetside_list.reverse()
            
            for c in range(len(sheetside_list)):
                sheetside = sheetside_list[c]
                
                if c % 2 == 0:
                    sheetside.bottom_right = [ big, little ]
                else:
                    sheetside.bottom_left  = [ big, little ]
        
                little += 1
                big    -= 1
                
            sheetside_list.reverse()
            
            for c in range(len(sheetside_list)):
                sheetside = sheetside_list[c]
                
                if c % 2 == 0:
                    sheetside.top_left  = [ little, big ]
                else:
                    sheetside.top_right = [ little, big ]
        
                little += 1
                big    -= 1
                
            sheetside_list.reverse()
            
            for sheetside in sheetside_list:
                for page_num in sheetside.top_left:
                    if TopReverseLast and page_num == NumberOfPages:
                        tkstring += str(page_num) + ' '
                    else:
                        tkstring += str(page_num) + 'down '
                        
                for page_num in sheetside.bottom_left:
                    tkstring += str(page_num) + 'down '
                    
                for page_num in sheetside.top_right:
                    tkstring += str(page_num) + ' '
                    
                for page_num in sheetside.bottom_right:
                    tkstring += str(page_num) + ' '
    
    else:
        for c in range(NumberOfSides):
            sheetside = sheetside_dict_t()
            d = c+1 if RightToLeft else c
            
            if d % 2 == 0:
                sheetside.bottom_down = [ big, little ]
            else:
                sheetside.bottom_down = [ little, big ]
                
            sheetside_list.append(sheetside)
            
            little += 1
            big    -= 1
            
        sheetside_list.reverse()
        
        for c in range(len(sheetside_list)):
            sheetside = sheetside_list[c]
            d = c+1 if RightToLeft else c
            
            if d % 2 == 0:
                sheetside.top_up = [ big, little ]
            else:
                sheetside.top_up  = [ little, big ]
                
            little += 1
            big    -= 1
        
        sheetside_list.reverse()
        
        for c in range(len(sheetside_list)):
            sheetside = sheetside_list[c]
            d = c+1 if RightToLeft else c
            
            if d % 2 == 0:
                sheetside.top_middle  = [ big, little ]
            else:
                sheetside.top_middle = [ little, big ]
                
            little += 1
            big    -= 1
        
        sheetside_list.reverse()
        
        for c in range(len(sheetside_list)):
            sheetside = sheetside_list[c]
            d = c+1 if RightToLeft else c
            
            if d % 2 == 0:
                sheetside.bottom_middle  = [ big, little ]
            else:
                sheetside.bottom_middle = [ little, big ]
                
            little += 1
            big    -= 1
            
        sheetside_list.reverse()
        
        for sheetside in sheetside_list:
            for page_num in sheetside.top_up:
                tkstring += str(page_num) + 'down '
                
            for page_num in sheetside.top_middle:
                tkstring += str(page_num) + ' '
                
            for page_num in sheetside.bottom_middle:
                tkstring += str(page_num) + 'down '
        
            for page_num in sheetside.bottom_down:
                tkstring += str(page_num) + ' '
                
            
print(tkstring)
