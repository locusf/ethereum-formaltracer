from formal import get_formula
from stack import format_stack
def parse_fn_computation(fn,op, comp, table):
    table.add_row([fn.mnemonic, get_formula(op, comp), format_stack(comp.stack), len(comp.memory.bytes),comp.get_gas_used()])
