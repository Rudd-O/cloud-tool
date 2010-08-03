'''
Created on Aug 2, 2010

@author: rudd-o
'''

import sys
import cloud_tool.apis as apis
apis = apis
import cloud_tool.utils as utils

    
def main():
    
    prelim_args = [ x for x in sys.argv[1:] if not x.startswith('-') ]
    parser = utils.get_parser()
    
    if len(prelim_args) == 0:
        apilist = utils.get_api_list()
        parser.error("you need to specify an API as the first argument\n\nSupported APIs:\n" + "\n".join(apilist))
    elif len(prelim_args) == 1:
        api = utils.lookup_api(prelim_args[0])
        commandlist = utils.get_command_list(api)
        parser.error("you need to specify a command name as the second argument\n\nCommands supported by the %s API:\n"%prelim_args[0] + "\n".join(commandlist))

    api = utils.lookup_api(prelim_args[0])
    if not api:     parser.error("API %r not supported"%prelim_args[0])
    
    command = utils.lookup_command_in_api(api,prelim_args[1])
    if not command: parser.error("command %r not supported by the %s API"%(prelim_args[1],prelim_args[0]))

    parser = utils.get_parser(api.__init__,command)
    opts,args,api_optionsdict,cmd_optionsdict = parser.parse_args()
    
    api = utils.lookup_api(args[0])
    
    try:
        api = api(**api_optionsdict)
    except utils.OptParseError,e:
        parser.error(str(e))
    
    command = utils.lookup_command_in_api(api,args[1])

    # we now discard the first two arguments as those necessarily are the api and command names
    args = args[2:]

    return command(*args,**cmd_optionsdict)


if __name__ == '__main__':
    main()