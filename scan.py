import lldb
import os
import shlex
import optparse

def __lldb_init_module(debugger, dict):
    debugger.HandleCommand('command script add -f scan.scan scan')

def scan(debugger, command, exe_ctx, result, internal_dict):
    command_args = shlex.split(command)
    parser = generate_args()
    try:
        (options, args) = parser.parse_args(command_args)
    except:
        return

    expr_options = lldb.SBExpressionOptions()
    expr_options.SetFetchDynamicValue(lldb.eDynamicCanRunTarget)
    expr_options.SetLanguage (lldb.eLanguageTypeObjC_plus_plus)

    target = exe_ctx.target
    module = target.FindModule(lldb.SBFileSpec(options.module))
    symbol_context_list = [i for i in module.get_symbols_array() if i.GetType() == lldb.eSymbolTypeData and i.addr.IsValid() and i.IsValid()]
    for symbol_context in symbol_context_list:
        symbol = symbol_context.addr.GetSymbolContext(lldb.eSymbolContextEverything)
        symbol_name = symbol.symbol.name
        addr = hex(symbol.symbol.addr.GetLoadAddress(target))
        if "static" in symbol_name:
            finalStr = symbol_name
            finalStr += '\n'+addr+'\n\n'
            print(finalStr)


def generate_args():
    usage = "usage: %prog [options] path/to/item"
    parser = optparse.OptionParser(usage=usage, prog="scan")
    parser.add_option("-m", "--module",
                      action="store",
                      default=None,
                      dest="module",
                      help="")
    return parser