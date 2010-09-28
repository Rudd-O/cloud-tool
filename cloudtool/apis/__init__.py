'''
Created on Aug 2, 2010

@author: rudd-o
'''

# FIXME do it dynamically based on the content of cloudtool.apis module directory

def get_all_apis():
    from cloudtool.apis import amazon,cloud
    return [amazon,cloud]

