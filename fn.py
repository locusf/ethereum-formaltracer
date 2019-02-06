from formal import get_formula
from stack import format_stack
def parse_fn_computation(fn,op, comp):
    return "{} | {} | {} | {} | {}".format(fn.mnemonic, get_formula(op, comp), format_stack(comp._stack), len(comp._memory._bytes),comp.get_gas_used())

