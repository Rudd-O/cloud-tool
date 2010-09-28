'''
Created on Aug 2, 2010

@author: rudd-o
'''

# FIXME do it dynamically based on the content of cloud_tool.apis module directory

def get_all_apis():
    from cloud_tool.apis import amazon,cloud
    return [amazon,cloud]

