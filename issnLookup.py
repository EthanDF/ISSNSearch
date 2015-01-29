import csv
from pymarc import *

mrcFile = 'c://Users//fenichele//Desktop//issnlookup-out.mrc'
inputFile = 'c://Users//fenichele//Desktop//ISSNSearch.csv'
outFile = 'c://Users//fenichele//Desktop//ISSNResult-out.csv'
issnResults = 'C://Users//fenichele//Desktop//issnResults2.mrc'

def holCount(holString):
    """this will cycle through the holdings count to identify the number in the string"""
    holdingInfo = holString
    c = 0
    start = 0
    end = 0

    for h in holdingInfo:
        if h.isdigit():
            if start == 0:
                start = c
                end = c
            else:
                end = c
##        print(c,start,end)
        c = c+1

    holCount = holdingInfo[start:end+1]
    return int(holCount)


def writeLog(testISSN,useOCLC):
    """Write ISSNs to log"""
    results = []
    results.append(str(testISSN))
    results.append(str(useOCLC))
    with open(outFile, 'a', newline='', encoding = 'utf-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(results)

def urlItem(item,url):
    """this function will remove any 856 values from the item
    it will then add the url passed here into the 856 as a replacement
    """

    preItem = item
    url = url

##    remove any existing 856 fields
    for f in preItem.get_fields('856'):
        preItem.remove_field(f)

##    add a new 856 field based on what was passed via 'url'
    add856 = Field(
        tag = '856',
        indicators = ['4','0'],
        subfields = ['u',url]
        )

    preItem.add_field(add856)

    updatedItem = preItem

    return updatedItem

    

def writeItem(item):
    """this will write the item to a file that can then be loaded in marc edit"""
    wItem = item
    with open(issnResults, 'ab') as x:
        try:
            x.write(wItem.as_marc())
        except UnicodeEncodeError:
            print ("couldn't write ",item['035'].value())

def readMrc(testISSN, url):
##    print("running readMrc...")
##    print("matching ",testISSN)
    url = url
    with open(mrcFile, 'rb') as fh:
        reader = MARCReader(fh)

##        issnTestVal = 
        useItem = None
##        topHols = [holdingcount, rda, has050]
        topHols = [0,0,0]
        
        for item in reader:
##            print(item.title())
    ##        we only are interesting in ISSN values of 'a', 'l', or 'y'
            issnTags = ['a','l','y']
            if item['022'] == None:
                continue
            for i in item['022']:
    #iterate through ISSN values print the result for testing              
                if i[0] in issnTags:
##                    print (i[1])
                    tempISSN = i[1]
##                    print (tempISSN)
    ##                check to see if this ISSN value matches our test value
##                    print("running testISSN")

                    if tempISSN == testISSN:
##                        print ("Match!")
                       
                        fmt = item['008'].value()[23:24]

                        catSource = []

                        cat = []
                        cat = item['040']
                            
                        langCat = None
                        catType = None

                        for e in cat:
##                            print (e[0])
##                            print (e[0] == 'a')

##                            print (e[0] == 'b')
                            if e[0] == 'b':
                                langCat = e[1]
##                            else:
##                                langCat = None

##                            print (e[0] == 'e')    
                            if e[0] == 'e':
                                catType = e[1]
##                            else:
##                                catType = None

                            if e[0] in ('a','c','d'):
                                catSource.append(e[1])

##                        if fmt in('o','s'):
##                            print ("fmt: ",fmt)
##                        if langCat == 'eng':
##                            print ("lang: ",langCat)
##                        if langCat == None:
##                            print(item['245']['h'])

                        isRDA = 0 
                        if catType == 'rda':
##                            print ("RDA!")
                            isRDA = 1
                            
##                        print("catSource: ", catSource)
                        holdingInfo = item['948'].value()
##                        print (holdingInfo)

                        if item['050'] == None:
                            has050 = 0
                        else:
                            has050 = 1


                        
                        if fmt in('o','s') and langCat == 'eng':
                            hols = holCount(holdingInfo)
                            holsList = [hols,isRDA, has050]

##                            print(hols)
##                            print (item)

##                            print ("hols=",hols," topHols=",topHols)
                            if holsList[0] - topHols[0] > 20:
                                topHols = holsList
                                useItem = item
                            elif holsList[1]+holsList[2] > topHols[1]+topHols[2]:
                                topHols = holsList
                                useItem = item
                                
##                                print("using item!")
##                                input('pause for review')
                                
                            

##                        input('pause for review')

        if useItem != None:
            useOCLC = (useItem['035']['a'])
            updateUseItem = urlItem(useItem,url)
            writeItem(updateUseItem)
##            print (useOCLC)
        else:
            useOCLC = None
            updateUseItem = None
##        write the results of the search to the log
        writeLog(testISSN,useOCLC)
        return updateUseItem

def listofISSN():
    issnList = []
    with open(inputFile, 'r') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            try:
                issnList.append(row)
            except UnicodeDecodeError:
                print("failed to load: ",row)

    return issnList


def runISSN(testISSN,url):
    """Checks a mrc file for the ISSNs matching a CSV file
    and writes the "best one" to a .mrc file
    enter a single ISSN to test it [####-####]
    or else None to run the csv file
    """
    
    issnList = []
    if testISSN == None and url == None:
        issnList = listofISSN()
    else:
        issnList.append(['',testISSN,url])

    for i in issnList:
        issn = i[1]
        url = i[2]
        result = readMrc(issn,url)

    if result == None:
        print(testISSN,None)
    else:
        print(testISSN,result['035']['a'])
        
