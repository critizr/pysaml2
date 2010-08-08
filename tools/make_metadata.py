#!/usr/bin/env python
import os 
import getopt

from saml2.metadata import entity_descriptor, entities_descriptor
from saml2.sigver import SecurityContext

HELP_MESSAGE = """
Usage: make_metadata [options] 1*configurationfile

Valid options:
hi:k:sv:x:
  -h            : Print this help message
  -i id         : The ID of the entities descriptor
  -k keyfile    : A file with a key to sign the metadata with
  -s            : sign the metadta
  -v            : How long, in days, the metadata is valid from the 
                    time of creation
  -x            : xmlsec1 binaries to be used for the signing
"""

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

    
def main(args):
    try:
        opts, args = getopt.getopt(args, "hi:k:sv:x:", 
                        ["help", "name", "id", "keyfile", "sign", 
                        "valid", "xmlsec"])
    except getopt.GetoptError, err:
        # print help information and exit:
        raise Usage(err) # will print something like "option -a not recognized"
        sys.exit(2)
        
    output = None
    verbose = False
    valid_for = 0
    name = ""
    id = ""
    sign = False
    xmlsec = ""
    keyfile = ""
    
    try:
        for o, a in opts:
            if o in ("-v", "--valid"):
                valid_for = int(a) * 24
            elif o in ("-h", "--help"):
                raise Usage(HELP_MESSAGE)
            elif o in ("-n", "--name"):
                name = a
            elif o in ("-i", "--id"):
                id = a
            elif o in ("-s", "--sign"):
                sign = True
            elif o in ("-x", "--xmlsec"):
                xmlsec = a
            elif o in ("-k", "--keyfile"):
                keyfile = a
            else:
                assert False, "unhandled option %s" % o
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2

    eds = []
    for conf in args:
        confd = eval(open(conf).read())
        eds.append(entity_descriptor(confd, valid_for))
    
    secc = SecurityContext(xmlsec, keyfile) 
    print entities_descriptor(eds, valid_for, name, id, sign, secc)
    
if __name__ == "__main__":
    import sys
    
    main(sys.argv[1:])
