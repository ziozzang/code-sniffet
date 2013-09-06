#!/usr/bin/env python

"""Thunder Chen<nkchenz@gmail.com> 2007.9.1"""

from __future__ import with_statement
import re

try:
    import xml.etree.ElementTree as ET
except:  # pragma: no cover
    # For Python 2.4
    import cElementTree as ET

class object_dict(dict):
    """Object view of dict, you can.
    >>> a = object_dict()
    >>> a.fish = 'fish'
    >>> a['fish']
    'fish'
    >>> a['water'] = 'water'
    >>> a.water
    'water'
    >>> a.test = {'value': 1}
    >>> a.test2 = object_dict({'name': 'test2', 'value': 2})
    >>> a.test, a.test2.name, a.test2.value
    (1, 'test2', 2)
    """

    def __init__(self, initd=None):
        if initd is None:
            initd = {}
        dict.__init__(self, initd)

    def __getattr__(self, item):
        d = self.__getitem__(item)
        # if value is the only key in object, you can omit it
        if isinstance(d, dict) and 'value' in d and len(d) == 1:
            return d['value']
        else:
            return d

    def __setattr__(self, item, value):
        self.__setitem__(item, value)

class XML2Dict(object):

    def _parse_node(self, node):
        node_tree = object_dict()
        if node.text and node.attrib:
            if node.tag in node.attrib:
                raise ValueError("Name conflict: Attribute name conflicts with "
                                 "tag name. Check the documentation.")
            node.attrib.update({node.tag: node.text})
            node.text = ''
        # Save attrs and text. Fair warning, if there's a child node with the same name
        # as an attribute, values will become a list.
        if node.text and node.text.strip():
            node_tree = node.text
        else:
            for k, v in node.attrib.items():
                k, v = self._namespace_split(k, v)
                node_tree[k] = v
            # Save children.
            for child in node.getchildren():
                tag, tree = self._namespace_split(child.tag, self._parse_node(child))
                if tag not in node_tree:  # First encounter, store it in dict.
                    node_tree[tag] = tree
                    continue
                old = node_tree[tag]
                if not isinstance(old, list):
                    # Multiple encounters, change dict to a list
                    node_tree.pop(tag)
                    node_tree[tag] = [old]
                node_tree[tag].append(tree)  # Add the new one.
        if not node_tree:
            node_tree = None
        return node_tree
        
    def _namespace_split(self, tag, value):
        """
           Split the tag  '{http://cs.sfsu.edu/csc867/myscheduler}patients'
             ns = http://cs.sfsu.edu/csc867/myscheduler
             name = patients
        """
        result = re.compile("\{(.*)\}(.*)").search(tag)
        if result:
            tag = result.groups(1)
            # value.namespace, tag = result.groups()
        return (tag, value)

    def parse(self, file):
        """Parse an XML file to a dict."""
        with open(file, 'r') as f:
            return self.fromstring(f.read())

    def fromstring(self, s):
        """Parse a string."""
        t = ET.fromstring(s)
        root_tag, root_tree = self._namespace_split(t.tag, self._parse_node(t))
        return object_dict({root_tag: root_tree})


class Dict2XML(object):
    """Turn a dictionary into an XML string."""

    def tostring(self, d, wrap=False):
        """Convert dictionary to an XML string."""
        if not isinstance(d, dict):
            raise TypeError('tostring must receive a dictionary: %r' % d)
        if len(d) != 1:
            raise ValueError('Dictionary must have exactly one root element')
        if isinstance(d.itervalues().next(), list):
            raise ValueError('Dictionary must not be a map to list: %r' % d)

        xml_list = ['<?xml version="1.0" encoding="UTF-8" ?>\n']
        xml_list.append(self.__tostring_helper(d))
        res = ''.join(xml_list)

        if wrap:
            res = res.encode("UTF-8")
            res = xml.dom.minidom.parseString(res).toprettyxml().\
                  replace(u'<?xml version="1.0" ?>',
                          u'<?xml version="1.0" encoding="UTF-8"?>')
            text_re = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)
            res = text_re.sub('>\g<1></', res)
        return res

    def __tostring_helper(self, d):
        if isinstance(d, int):
            return str(d)

        elif isinstance(d, basestring):
            return '%s' % d
            #return '<![CDATA[%s]]>' % d

        elif isinstance(d, dict):
            x = []
            for tag, content in d.iteritems():
                if content is None:
                    x.append('<%s />' % tag)
                elif isinstance(content, list):
                    for c in content:
                        if c is None:
                            x.append('<%s />' % tag)
                        else:
                            x.append('<%s>%s</%s>' %\
                                     (tag, self.__tostring_helper(c), tag))
                else:
                    x.append('<%s>%s</%s>' %\
                             (tag, self.__tostring_helper(content), tag))
            xml_string = ''.join(x)
            return xml_string

        else:
            raise ValueError('Cannot convert %r to an XML string' % d)
