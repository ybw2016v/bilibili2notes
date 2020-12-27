import re;

def pythonReSubDemo():
    """
        demo Pyton re.sub
    """
    inputStr = "#dsd# sds #545#dds "

    def _add111(matched):
        print(matched)
        intStr = matched.group()
        intValue = str(intStr)
        # intValue[:-1]=' '
        addedValue = intValue[:-1]+' '
        addedValueStr = str(addedValue)
        return addedValueStr

    replacedStr = re.sub("#(.*?)#", _add111, inputStr)
    print("replacedStr=",replacedStr) 
pythonReSubDemo()