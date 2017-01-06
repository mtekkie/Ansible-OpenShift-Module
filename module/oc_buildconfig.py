#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) Robert Forsström, robert@middleware.se


DOCUMENTATION = '''
---
module: oc_buildconfig
short_description: Open Shift BuildConfig
description:
    - Build Config in Open Shift Enterprise.
    - The module is using the REST Interface to interact with the Open Shift Master.

author: "Robert Forsström, @mtekkie"
notes:
    - In order for this module to work a service account needs to be created.
    - It is up to you to decide which project it should have access to.
    - In the following example it is given the maximum permissions (cluster admin):
    - oc project default
    - oc create serviceaccount ansible
    - oadm policy add-cluster-role-to-user cluster-admin system:serviceaccount:default:ansible
    - To get the JWT token to authenticate to the API:
    - oc describe serviceaccount ansible
    - Find the relevant token.
    - oc describe secret ansible-token-xxxx

requirements:
    - A authentication token for an Open Shift Service Account.

options:
    state:
        description:
            - If it should be present or absent.
        required: true
        default: present
        choices: [present, absent]
        version_added: 1.0

    master_url:
        description:
            - URL to Open Shift Master server
        required: true
        default: null

    auth_token:
        description:
            - Security Token token for a service account.
        required: true
        default: null

    project:
        description:
            - Open Shift Project
        required: true
        default: null

    name:
        description:
            - Name of build config.
        required: true
        default: null

    triggers:
        description:
            - Triggers determine how new Builds can be launched from a BuildConfig.
            - If no triggers are defined, a new build can only occur as a result
            - of an explicit client build creation (v1.BuildTriggerPolicy).
        required: false
        default: null

    runPolicy:
        description:
            - RunPolicy describes how the new build created from this build
            - configuration will be scheduled for execution.
            - This is optional, if not specified we default to "Serial".
        required: false
        default: Serial

    serviceAccount:
        description:
            - serviceAccount is the name of the ServiceAccount to use to run
            - the pod created by this build. The pod will be allowed to use
            - secrets referenced by the ServiceAccount
        required: false
        default: null

    source:
        description:
            -  source describes the SCM in use.
            - (v1.BuildSource)
        required: false
        default: null

    # revision:
    #     description:
    #         - revision is the information from the source for a specific repo snapshot. This is optional.
    #         - (v1.SourceRevision)
    #     required: false
    #     default: null

    strategy:
        description:
            - Build strategy
        required: false
        default: null


    output:
        description:
            - output describes the Docker image the Strategy should produce.
            - List of v1.BuildOutput attributes:
            - to (v1.ObjectReference), pushSecret (v1.LocalObjectReference),
            - imageLabels(array of v1.ImageLabel)
        required: false
        default: null

    resources:
        description:
            - resources computes resource requirements to execute the build.
            - List of v1.ResourceRequirements attributes:
            - limits, requests
        required: false
        default: null

    postCommit:
        description:
            - postCommit is a build hook executed after the build output image
            - is committed, before it is pushed to a registry.
            - List of v1.BuildPostCommitSpec attributes:
            - command, args, script.
        required: false
        default: null

    # completionDeadlineSeconds:
    #     description:
    #         - completionDeadlineSeconds is an optional duration in seconds,
    #         - counted from the time when a build pod gets scheduled in the system,
    #         - that the build may be active on a node before the system actively
    #         - tries to terminate the build; value must be positive integer
    #     required: false
    #     default: null

    # nodeSelector:
    #     description:
    #         - nodeSelector is a selector which must be true for the build pod
    #         - to fit on a node If nil, it can be overridden by default build
    #         - nodeselector values for the cluster. If set to an empty map or a
    #         - map with any values, default build nodeselector values are ignored.
    #     required: false
    #     default: null

'''


EXAMPLES = '''
- oc_buildconfig:
    master_url: https://funnybunny.middleware.se:8443
    auth_token: eyJhbGciOiJSUzI1NiIsInR5.....
    name: abba
    project: downloader
    triggers: []
    source:
      type: Dockerfile
      dockerfile: 'FROM centos:7\n ENV LANG en_US.UTF-8 \n RUN yum install -y epel-release....'
      secrets: null
    strategy:
      type: Docker
      dockerStrategy:
        env:
          - name: MY_BUILD_VAR
            value: Sierra Mike Echo
    output:
      to:
        kind: ImageStreamTag
        namespace: downloader
        name: 'abba:latest'
'''

RETURN = '''

'''



import urllib2
import ssl
import json
from string import Template
import types

## Constants:
API_BASE = "/oapi/v1"


def main():
    module = AnsibleModule(
        argument_spec = dict(
            state                   = dict(default='present', choices=['present', 'absent']),
            master_url              = dict(required=True),
            auth_token              = dict(required=True),
            project                 = dict(required=True),
            name                    = dict(required=True),
            triggers                = dict(required=False, default='[]', type='list'),
            runPolicy               = dict(required=False),
            serviceAccount          = dict(required=False),
            source                  = dict(required=False, default='{}', type='dict'),
            revision                = dict(required=False, default='{}', type='dict'),
            strategy                = dict(required=False, default='{}', type='dict'),
            output                  = dict(required=False, default='{}', type='dict'),
            resources               = dict(required=False),
            postCommit              = dict(required=False),
            completionDeadlineSeconds = dict(required=False),
            nodeSelector            = dict(required=False)

        )
    )

    SERVICE  = "namespaces/"+module.params.get("project")+"/buildconfigs/"
    PATH = SERVICE+module.params.get("name")

    TEMPLATE = '''
    {
      "kind": "BuildConfig",
      "apiVersion": "v1",
      "metadata": {
        "name": "$name",
        "namespace": "$project"
      },
      "spec": {
        "triggers": $triggers,
        "source": $source,
        "strategy": $strategy,
        "output":   $output,
        "resources": "$resources",
        "postCommit": "$postCommit"
      }
    }
    '''

    cfg = template_to_dict(TEMPLATE, module.params)
    should_be = clean_dict_from_nones(cfg)
    should_be_json = dict_to_json(should_be)

    try:
        current_json = http_get(PATH, module)
        current = json_to_dict(current_json)
        # Only If resource exists on server ...
        if module.params.get("state") == "absent":
            http_delete(PATH,module)
            module.exit_json(changed=True)
            return

        if compliant (current,should_be):
            module.exit_json(changed=False, ansible_facts=current)
        else:
            #Set resourceVersion in should_be.
            should_be['metadata']['resourceVersion']=current['metadata']['resourceVersion']
            result = http_put(PATH, module, dict_to_json(should_be))
            facts = json_to_dict(result)
            module.exit_json(changed=True, ansible_facts=facts)

    except urllib2.HTTPError as sc:

        if not has_project(module):
            module.fail_json(msg="Project does not exist")

        if sc.code == 404 and module.params.get("state") == "present":
            result = http_post(SERVICE, module, should_be_json)
            facts = json_to_dict(result)
            module.exit_json(changed=True, ansible_facts=facts)

        if sc.code == 404 and module.params.get("state") == "absent":
            module.exit_json(changed=False)




########################### Helper functions ###################################
#
# This section contains helper fuctions
#
################################################################################


def dict_to_json(in_dict):
    return json.dumps(in_dict)

def json_to_dict(in_json):
    return json.loads(in_json)

# Cleans up dict. Removes entries that have a value of None.
# Mainly used for cleaning up Templates with have vaules that are not set in the
# module.
# Consumes Dict, Returns Dict.
def clean_dict_from_nones(in_dict):
    return __clean_dict_from_nones_recursive(in_dict)


def __clean_dict_from_nones_recursive(in_dict):
    new_dict = dict ()
    for key in in_dict:
        if isinstance(in_dict[key], dict):
            ret=__clean_dict_from_nones_recursive(in_dict[key])
            if len(ret) > 0:
                new_dict[key] = ret
        elif in_dict[key] != 'None':
            new_dict[key]=in_dict[key]
    return new_dict

def template_to_dict(template, params):
    # First: Create vaild json-strings from dicts that are nested.
    fixed_params= dict();
    for key in params:
        if isinstance(params[key], dict) or isinstance(params[key], list) :
            fixed_params[key] = json.dumps(params[key])
        else:
            fixed_params[key] = params[key]

    jsonified = Template(template).substitute(fixed_params)
    #print jsonified
    return json.loads(jsonified)


# Takes two Python Dicts and compare them
# If the should_be objects value is different then the is_obj then
# the function returns False
# is_obj MAY contain more attributes then should_be. Thoose are never checked.
# Returns True or False.
def compliant (is_obj, should_be):
    if not isinstance(is_obj, dict):
        return False

    is_compliant = True
    for key in should_be:
        # Recursiv processing of dicts.
        if isinstance(should_be[key], dict):
            is_compliant = compliant (is_obj[key], should_be[key])
            if not is_compliant:
                return False
        else:
            # Check values.
                #print "Checking if should_be[key] != is_obj[key]: " + should_be[key] +":"+ is_obj[key]
            if should_be[key] != is_obj[key]:
                    is_compliant = False
                    return False
    return is_compliant

# Checks if project exist.
# Returns True/False
def has_project(module):
    try:
        path = "projects/"+module.params["project"]
        http_get(path, module)
    except urllib2.HTTPError as sc:
        if sc.code == 404:
            return False
        else:
            raise
    return True

def get_message_from_v1status(body):
    if isinstance(body,list):
        body=''.join(body)
    #json to obj.
    status = json.loads(body)
    return status['message']

#####################################
# HTTP Helper functions
# Takes cares of GET/POST/PUT/DELETE
# Generic fault-handling for standard errors in OSE.
# Code: Fail:
# 401   Authentication issues
# 409   Conflict, Can not update resouce
#
#####################################
def http_get(path, module):
    return http_request("GET", path, module, "")

def http_post(path, module, data):
    return http_request("POST", path, module, data)

def http_put(path, module, data):
    return http_request("PUT", path, module, data)

def http_delete(path, module):
    return http_request("DELETE", path, module, "")

def http_request(method, path, module, data):
    try:
        url = module.params.get("master_url")+API_BASE+"/"+path
        #opener = urllib2.build_opener(urllib2.HTTPHandler)
        headers = {'Authorization': 'Bearer '+module.params.get("auth_token")}

        #GET
        req = urllib2.Request(url=url, headers=headers)

        if method == "DELETE":
            req = urllib2.Request(url=url, headers=headers)
            req.get_method = lambda: 'DELETE'

        elif method == "POST":
            req = urllib2.Request(url=url, headers=headers, data=data)
            req.add_header("Content-Type", "application/json")

        elif method == "PUT":
            req = urllib2.Request(url=url, headers=headers, data=data)
            req.add_header("Content-Type", "application/json")
            req.get_method = lambda: 'PUT'

        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

        content = urllib2.urlopen(req, context=gcontext).read()
        return content

    except urllib2.HTTPError as sc:
        if sc.code == 401:
            msg = "Open Shift authenication error (401):"
            msg = msg + get_message_from_v1status(sc.readlines())
            module.fail_json(msg=msg)

        elif sc.code == 409:
            msg = "Open Shift Reports Conflict (409). Can't update resource:"
            msg = msg + get_message_from_v1status(sc.readlines())
            module.fail_json(msg=msg)
        elif sc.code == 422:
            msg = "Open Shift Reports Unprocessable Enitiy (422):"
            msg = msg + get_message_from_v1status(sc.readlines())
            module.fail_json(msg=msg)
        else:
            raise sc

    except urllib2.URLError as ue:
module.fail_json(msg="Open Shift Master is unreachable. Check connection and master_url setting.")
########################### End of helper functions ############################


from ansible.module_utils.basic import AnsibleModule
if __name__ == '__main__':
    main()
