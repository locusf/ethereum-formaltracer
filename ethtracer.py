from bitstring import BitStream,ConstBitStream
from evm.vm.computation import Computation
from evm.vm.code_stream import CodeStream
from evm.vm.message import Message
from evm.vm.forks.frontier import FrontierVM
from evm.vm.forks.frontier.transactions import FrontierTransaction
from evm.db import get_db_backend
from evm.constants import CREATE_CONTRACT_ADDRESS,EMPTY_UNCLE_HASH
from evm.precompile import PRECOMPILES
from evm.rlp.headers import BlockHeader
from fn import parse_fn_computation
import data
from evm import opcode_values
from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat, LongTabu, HFill
import logging
BREAK_OPCODES = {
    opcode_values.RETURN,
    opcode_values.STOP,
    opcode_values.SUICIDE,
}

def apply_latex_computation(vm, message,document):
    computation = Computation(vm, message)

    with computation:
        # Early exit on pre-compiles
        if computation.msg.code_address in PRECOMPILES:
            return PRECOMPILES[computation.msg.code_address](computation)
        with doc.create(LongTabu("X[r] X[r] X[r] X[r] X[r]",booktabs=True,spread="5mm",to="5mm")) as data_table:
            header_row1 = ["OPCODE", "Formal", "Stack", "Mem", "Gas"] 
            data_table.add_row(header_row1)
            data_table.add_hline()
            data_table.add_empty_row()
            data_table.end_table_header()
            for opcode in computation.code:
                opcode_fn = computation.vm.get_opcode_fn(opcode)
                parse_fn_computation(opcode_fn,opcode,computation,data_table)
                opcode_fn(computation=computation)
                if opcode in BREAK_OPCODES:
                    break

    return computation

ADDRESS_C = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf2"
bytecode = bytes.fromhex(data.bytestr)
supergas = 100000
#ConstBitStream(data.bytestr)
if __name__ == "__main__":
    header = BlockHeader(100,1,supergas,uncles_hash=EMPTY_UNCLE_HASH)
    vm = FrontierVM(header,get_db_backend())
    geometry_options = {
        "landscape": True,
        "margin": "0.5in",
        "headheight": "20pt",
        "headsep": "10pt",
        "includeheadfoot": True
    }
    doc = Document(geometry_options=geometry_options)
    message = Message(
            supergas,
            100,
            ADDRESS_C,
            ADDRESS_C,
            0,
            b'',
            bytecode,
            create_address=ADDRESS_C,
            code_address=ADDRESS_C,
            should_transfer_value=False
            )
    apply_latex_computation(vm,message,doc)
    doc.generate_pdf("longtabu",compiler_args=["-f"])
