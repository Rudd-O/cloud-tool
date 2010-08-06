'''Implements the Cloud.com API'''


from cloud_tool.utils import describe
import urllib
import urllib2
import os
import xml.dom.minidom

class CloudAPI:
    
	@describe("server", "Management Server host name or address")
	@describe("format", "Response format: xml or json")
	def __init__(self,
			server="127.0.0.1:8096",
			format="xml",
			):
		self.__dict__.update(locals())
        
	def _make_request(self,command,parameters=None):
		'''Command is a string, parameters is a dictionary'''
		if ":" in self.server:
			host,port = self.server.split(":")
			port = int(port)
		else:
			host = self.server
			port = 8096
		
		url = "http://" + self.server + "/?"
		
		if not parameters: parameters = {}
		parameters["command"] = command
		parameters["response"] = self.format
		querystring = urllib.urlencode(parameters)
		url += querystring
		
		f = urllib2.urlopen(url)
		
		data = f.read()
		
		return data


def load_dynamic_methods():
	'''creates smart function objects for every method in the commands.xml file'''
	
	def getText(nodelist):
		rc = []
		for node in nodelist:
			if node.nodeType == node.TEXT_NODE: rc.append(node.data)
		return ''.join(rc)
	
	# FIXME figure out installation and packaging
	xmlfile = os.path.join(os.path.dirname(__file__),"commands.xml")
	dom = xml.dom.minidom.parse(xmlfile)
	
	for cmd in dom.getElementsByTagName("command"):
		name = getText(cmd.getElementsByTagName('name')[0].childNodes).strip()
		assert name
		
		description = cmd.getElementsByTagName('name')[0].getAttribute("description")
		if description: description = '"""%s"""' % description
		else: description = ''
		arguments = []
		options = []
		descriptions = []
	
		for param in cmd.getElementsByTagName('arg'):
			argname = getText(param.childNodes).strip()
			assert argname
			
			required = param.getAttribute("required").strip()
			if required == 'true': required = True
			elif required == 'false': required = False
			else: raise AssertionError, "Not reached"
			if required: arguments.append(argname)
			else: options.append(argname)
			
			description = param.getAttribute("description").strip()
			if description: descriptions.append( (argname,description) )
		
		funcparams = ["self"] + arguments + [ "%s=None"%o for o in options ]
		funcparams = ", ".join(funcparams)
		
		code = """
		def %s(%s):
			%s
			parms = locals()
			del parms["self"]
			output = self._make_request("%s",parms)
			print output
		"""%(name,funcparams,description,name)
		
		namespace = {}
		exec code.strip() in namespace
		
		func = namespace[name]
		for argname,description in descriptions:
			func = describe(argname,description)(func)
		
		yield (name,func)


for name,meth in load_dynamic_methods(): setattr(CloudAPI,name,meth)

implementor = CloudAPI