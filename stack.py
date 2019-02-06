from pylatex import Description
def format_stack(stack):
    listed = ""
    for i,item in enumerate(reversed(stack.values)):
        listed += "<pre>{}</pre>".format(hex(item) if isinstance(item,int) else "".join(("0x",item.hex())))
    return listed 
