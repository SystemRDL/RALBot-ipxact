
import unittest
import subprocess
import os
import logging
import filecmp

from systemrdl import RDLCompiler
from systemrdl.messages import MessagePrinter
from ralbot.ipxact import IPXACTImporter, IPXACTExporter

#===============================================================================
class TestPrinter(MessagePrinter):
    def emit_message(self, lines):
        text = "\n".join(lines)
        logging.info(text)


#===============================================================================

class IPXACTTestCase(unittest.TestCase):

    def compile(self, files, top_name=None):
        this_dir = os.path.dirname(os.path.realpath(__file__))
        rdlc = RDLCompiler(
            message_printer=TestPrinter()
        )
        ipxact = IPXACTImporter(rdlc)

        for file in files:
            if file.endswith(".rdl"):
                rdlc.compile_file(os.path.join(this_dir, file))
            elif file.endswith(".xml"):
                ipxact.import_file(os.path.join(this_dir, file))
        return rdlc.elaborate(top_name)
    
    def export(self, node, file):
        this_dir = os.path.dirname(os.path.realpath(__file__))
        ipxact = IPXACTExporter()
        ipxact.export(node, os.path.join(this_dir, file))

    def compare(self, file1, file2):
        this_dir = os.path.dirname(os.path.realpath(__file__))

        self.assertTrue(filecmp.cmp(
            os.path.join(this_dir, file1),
            os.path.join(this_dir, file2)
        ), 'file compare failed')
    
    def validate_xsd(self, file, xsd):
        this_dir = os.path.dirname(os.path.realpath(__file__))

        file = os.path.join(this_dir, file)
        xsd = os.path.join(this_dir, xsd)
        cmd = ["xmllint", "--noout", "--schema", xsd, file]

        passed = True
        stderr = ""
        try:
            subprocess.check_output(
                cmd,
                stderr=subprocess.STDOUT
            )
        except subprocess.CalledProcessError as e:
            passed = False
            stderr = e.output.decode("utf-8")
        
        if not passed:
            raise AssertionError("XML Validate failed: %s" % stderr)