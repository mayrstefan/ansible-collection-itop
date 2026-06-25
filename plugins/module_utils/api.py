#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.errors import AnsibleParserError
import requests
import json

class ItopApi(object):
    """
    The base class for deriving off module classes
    """
    def __init__(self, url, username, password, verify):
        self.url = url
        self.username = username
        self.password = password
        self.verify = verify

    def list_operations(self):
        return self._request({ "operation": "list_operations" })
    
    def core_get(self, class_name, key, output_fields="*", page=1, limit=0):
        return self._request({ 
            "operation": "core/get",
            "class": class_name,
            "key": key,
            "output_fields": output_fields,
            "page": page,
            "limit": limit
        })
    
    def core_create(self, class_name, output_fields="*", comment="", fields={}):
        return self._request({ 
            "operation": "core/create",
            "class": class_name,
            "output_fields": output_fields,
            "comment": comment,
            "fields": fields
        })

    def core_delete(self, class_name, comment="", key={}):
        return self._request({ 
            "operation": "core/delete",
            "class": class_name,
            "key": key,
            "comment": comment,
            "simulate": False
        })

    def core_update(self, class_name, output_fields="*", comment="", fields={}, key={}):
        return self._request({ 
            "operation": "core/update",
            "class": class_name,
            "output_fields": output_fields,
            "key": key,
            "fields": fields,
            "comment": comment
        })
 
    def _request(self, payload):
        encoded_data = json.dumps(payload)

        response = requests.post(   
            self.url, 
            verify=self.verify, 
            data={
                'auth_user': self.username, 
                'auth_pwd': self.password,
                'json_data': encoded_data
            }
        )

        itop_data = response.json()
        if itop_data['code'] != 0:
            raise AnsibleParserError(
                f"Query error { itop_data['code'] }: { itop_data['message'] }"
            )

        return itop_data


    def request(self, _operation, _class=None, _key=None, _output_fields=None, _page=None, _limit=None):

        payload = { "operation": _operation }
        
        if _class is not None:
            payload["class"] = _class
    
        if _key is not None:
            payload["key"] = _key

        if _key is not None:
            payload["output_fields"] = _output_fields

        if _key is not None:
            payload["page"] = _page

        if _key is not None:
            payload["limit"] = _limit

        encoded_data = json.dumps(payload)

        response = requests.post(   
            self.url, 
            verify=self.verify, 
            data={
                'auth_user': self.username, 
                'auth_pwd': self.password,
                'json_data': encoded_data
            }
        )

        itop_data = response.json()
        if itop_data['code'] != 0:
            raise AnsibleParserError(
                f"Query error { itop_data['code'] }: { itop_data['message'] }"
            )

        return itop_data
