#from bitstring import BitStream,ConstBitStream
#from eth.vm.computation import Computation
from eth.vm.forks.constantinople.computation import ConstantinopleComputation as Computation
from eth.vm.code_stream import CodeStream
from eth.vm.message import Message
from eth.vm.forks.constantinople import ConstantinopleVM
from eth.vm.forks.constantinople.opcodes import CONSTANTINOPLE_OPCODES
from eth.vm.forks.constantinople.transactions import ConstantinopleTransaction
from eth.db import get_db_backend
from eth.constants import CREATE_CONTRACT_ADDRESS,EMPTY_UNCLE_HASH
#from eth.precompiles import PRECOMPILES
from eth.rlp.headers import BlockHeader
from fn import parse_fn_computation
import data
from eth.vm import opcode_values
import markdown
import logging
from eth import constants
from eth.chains.mainnet import MainnetChain
from eth.db.atomic import AtomicDB
from eth.tools.logging import setup_extended_logging
from eth_utils import to_wei, encode_hex
import eth.exceptions
setup_extended_logging()

MOCK_ADDRESS = constants.ZERO_ADDRESS
DEFAULT_INITIAL_BALANCE = to_wei(10000, 'ether')

GENESIS_PARAMS = {
    'parent_hash': constants.GENESIS_PARENT_HASH,
    'uncles_hash': constants.EMPTY_UNCLE_HASH,
    'coinbase': constants.ZERO_ADDRESS,
    'transaction_root': constants.BLANK_ROOT_HASH,
    'receipt_root': constants.BLANK_ROOT_HASH,
    'difficulty': constants.GENESIS_DIFFICULTY,
    'block_number': constants.GENESIS_BLOCK_NUMBER,
    'gas_limit': constants.GENESIS_GAS_LIMIT,
    'extra_data': constants.GENESIS_EXTRA_DATA,
    'nonce': constants.GENESIS_NONCE
}

GENESIS_STATE = {
    MOCK_ADDRESS: {
        "balance": DEFAULT_INITIAL_BALANCE,
        "nonce": 0,
        "code": b'',
        "storage": {}
    }
}

chain = MainnetChain.from_genesis(AtomicDB(), GENESIS_PARAMS, GENESIS_STATE)

BREAK_OPCODES = {
    opcode_values.RETURN,
    opcode_values.STOP,
    opcode_values.SELFDESTRUCT,
}

def apply_latex_computation(vm, message):
    computation = Computation(vm.state, message, vm)
    stringy = ""
    with computation:
        # Early exit on pre-compiles
        if computation.msg.code_address in CONSTANTINOPLE_OPCODES:
            return CONSTANTINOPLE_OPCODES[computation.msg.code_address](computation)
        header_row1 = "<table style=\"table.border-collapse: collapse;table.border: 1px solid black; th.border: 1px solid black;td.border: 1px solid black;\"><tr><th>OPCODE</th><th>Formal</th><th>Stack</th><th>Mem</th><th>Gas</th></tr>\n"
        stringy += header_row1
        stringy += "<tr>"
        for opcode in computation.code:
           opcode_fn = computation.get_opcode_fn(opcode)
           stringy += parse_fn_computation(opcode_fn,opcode,computation) + " \n"
           try:
               opcode_fn(computation=computation)
           except eth.exceptions.Halt:
               break
           if opcode in BREAK_OPCODES:
              break
           stringy += "</tr>"
    stringy += "</table>\n"
    return stringy, computation

ADDRESS_C = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf2"
bytecode = bytes.fromhex(data.bytestr)
supergas = 100000
#ConstBitStream(data.bytestr)
if __name__ == "__main__":
    
    vm = chain.get_vm()
    geometry_options = {
        "landscape": True,
        "margin": "0.5in",
        "headheight": "20pt",
        "headsep": "10pt",
        "includeheadfoot": True
    }
    doc = ""
    message = Message(
            supergas,
            MOCK_ADDRESS,
            MOCK_ADDRESS,
            0,
            b'',
            bytecode,
            create_address=MOCK_ADDRESS,
            code_address=MOCK_ADDRESS,
            should_transfer_value=False
            )
    vm.get_state_class()
    doc, comp = apply_latex_computation(vm,message)
    md = markdown.markdown(doc,extensions=['mdx_math','markdown.extensions.extra'],output_format="html5")
    md = md.replace("<script type=\"math/tex; mode=display\">","")
    print("""<!DOCTYPE html><html><head><script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>
<style>
th, td {
  border-bottom: 1px solid #ddd;
  padding: 10px;
  text-align: center;
}
td {
  vertical-align: center;
}
</style>
 <meta charset="UTF-8">
            </head><body>""")
    print(md)
    print("</body></html>")
