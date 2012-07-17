#!/usr/bin/env python

import sys
import optparse
from datetime import datetime
try:
    from scribe import scribe
except ImportError, e:
    print "CRITICAL - %s" % e
    sys.exit(2)
try:
    from thrift.transport import TTransport, TSocket
    from thrift.protocol import TBinaryProtocol
except ImportError, e:
    print "CRITICAL - %s" % e
    sys.exit(2)

#
# thanks to http://stackoverflow.com/a/1229667/72987
#
def optional_arg(arg_default):
    def func(option,opt_str,value,parser):
        if parser.rargs and not parser.rargs[0].startswith('-'):
            val=parser.rargs[0]
            parser.rargs.pop(0)
        else:
            val=arg_default
        setattr(parser.values,option.dest,val)
    return func

def main(argv):
    p = optparse.OptionParser(conflict_handler="resolve", description= "This Nagios plugin checks Scribe Server status.")
    p.add_option('-H', '--host', action='store', type='string', dest='host', default='127.0.0.1', help='Scribe host name')
    p.add_option('-P', '--port', action='store', type='int', dest='port', default=1463, help='The port Scribe is runnung on')
    p.add_option('-c', '--category', action='store', type='string', dest='category', default='test', help='Scribe category')
    p.add_option('-m', '--message', action='store', type='string', dest='message', default='this is message sent at ' + str(datetime.now()), help='Scribe message')
    
    options, arguments = p.parse_args()
    
    host = options.host
    port = options.port
    category = options.category
    message = options.message

    try:
        log_entry = scribe.LogEntry(category=category, message=message)
        socket = TSocket.TSocket(host=host, port=port)
        transport = TTransport.TFramedTransport(socket)
        protocol = TBinaryProtocol.TBinaryProtocol(trans=transport, strictRead=False, strictWrite=False)
        client = scribe.Client(iprot=protocol, oprot=protocol)
        transport.open()
        result = client.Log(messages=[log_entry])

        if result == scribe.ResultCode.OK:
            print "OK"
            sys.exit(0)
        elif result == scribe.ResultCode.TRY_LATER:
            print "CRITICAL - TRY LATER STATUS CODE RETURNED"
            sys.exit(84)
        else:
            print "CRITICAL - UNKNOWN ERROR CODE RETURNED"
            sys.exit(2)
    except Exception, e:
        print "CRITICAL - %s" % e
        sys.exit(2)

#
# entry point
#
if __name__ == "__main__":
    main(sys.argv[1:])

