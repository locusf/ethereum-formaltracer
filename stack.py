from pylatex import Description
def format_stack(stack):
    listed = Description()
    for i,item in enumerate(reversed(stack.values)):
        listed.add_item(i,hex(item) if isinstance(item,int) else item.hex())
    return listed 
