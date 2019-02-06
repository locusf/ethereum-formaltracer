from pylatex import Description
def format_stack(stack):
    listed = ""
    for i,item in enumerate(reversed(stack.values)):
        listed += "* {}, {} <br/>".format(i,hex(item) if isinstance(item,int) else item.hex())
    return listed 
