#!/usr/bin/env python3

import sys

from systemrdl import RDLCompiler, RDLCompileError
from ralbot.ipxact import IPXACTExporter

#===============================================================================
input_files = sys.argv[1:]

rdlc = RDLCompiler()

try:
    for input_file in input_files:
        rdlc.compile_file(input_file)
    root = rdlc.elaborate()
except RDLCompileError:
    sys.exit(1)

ipxact = IPXACTExporter()
ipxact.export(root, "out.xml")