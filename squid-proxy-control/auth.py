#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import ldap
import ConfigParser
config = ConfigParser.ConfigParser()
config.read('/etc/squid-proxy-control/spc.cfg')

def bind(username, password):
    try:
        l = ldap.open(config.get("auth_ldap","server"),389,0,sys.stderr,0)
        l.simple_bind_s(username + config.get("auth_ldap","domain"), password)
        return l
    except ldap.LDAPError, error_message:
        return False

def validate(username, password):
    # We need to bind to the LDAP server. Doing so creates an object named "l" that is then used throughout the program.
    l = bind(username, password)
    if l:
    #We're now ready to query the server.
        for group in config.get("auth_ldap","group_path").split(";"):
            if search(l, username, group):
                return True
            else:
                continue
        else:
            return False
    else:
        return False


def search(l, keyword, group):
    '''
    Tests whether the user exists in the given group or not
    '''
    #In a moment we will be calling python-ldap's built-in search method on our l object. Four variables--sigconfig.ldapbase, scope, filter and retrieve_attributes--are the parameters of that search method. sigconfig.ldapbase is used for the DN (distinguished name) of the entry where the search should start. You can leave it blank for this example:
    #For scope we use SCOPE_SUBTREE to search the object and all its descendants:
    scope = ldap.SCOPE_SUBTREE
    #Our search filter consists of a cn (common name) and our keyword. Putting asterisks around our keyword (ryan) will match anything with the string ryan, such as Bryant.
    filter = "(&(objectclass=person)(sAMAccountName=" + keyword + ")(memberof=" + group + "))"

    #The last argument we pass to the search method is used to return all the attributes of each entry:
    retrieve_attributes = None

    #Now, let's setup a few more variables, including a counter to keep track of the number of results returned:
    #count = 0

    #a list to append the results to:
    result_set = []

    #and a variable to specify the length, in seconds, we're willing to wait for a response from the server:
    timeout = 0

    #Now we can begin our search by calling python-ldap's search method on our l object:
    try:
        result_id = l.search(config.get("auth_ldap","base_dn"), scope, filter, retrieve_attributes)

        #Store any results in the result_set list
        while 1:
            result_type, result_data = l.result(result_id, timeout)
            if (result_data == []):
                break
            else:
                if result_type == ldap.RES_SEARCH_ENTRY:
                    result_set.append(result_data)

        #If there are no result --> False
        if len(result_set) == 0:
            return False
        else:
            return True
    except ldap.LDAPError, error_message:
        return False        

def getdata(username, password):
    '''
    Retrieve Data for the given user, Name, and maybe later permissions
    '''
    l = bind(username, password)
    #For scope we use SCOPE_SUBTREE to search the object and all its descendants:
    scope = ldap.SCOPE_SUBTREE
    #Our search filter consists of a cn (common name) and our keyword. Putting asterisks around our keyword (ryan) will match anything with the string ryan, such as Bryant.
    filter = "(&(objectclass=person)(sAMAccountName=" + username + ")(memberof=" + config.get("auth_ldap","group_path") + "))"

    #The last argument we pass to the search method is used to return all the attributes of each entry:
    retrieve_attributes = None

    #Now, let's setup a few more variables, including a counter to keep track of the number of results returned:
    #count = 0

    #a list to append the results to:
    result_set = []

    #and a variable to specify the length, in seconds, we're willing to wait for a response from the server:
    timeout = 0

    #Now we can begin our search by calling python-ldap's search method on our l object:
    try:
        result_id = l.search(config.get("auth_ldap","base_dn"), scope, filter, retrieve_attributes)

        #Store any results in the result_set list
        while 1:
            result_type, result_data = l.result(result_id, timeout)
            if (result_data == []):
                break
            else:
                if result_type == ldap.RES_SEARCH_ENTRY:
                    result_set.append(result_data)

        #If we were to print result_set now, it might look like a big list of tuples and dicts. Instead, step through it and select only the data we want to see
        if len(result_set) == 0:
            return [ False, "No Results." ]
        for i in range(len(result_set)):
            for entry in result_set[i]:                 
                try:
                    #Return the common name
                    name = entry[1]['cn'][0]
                    return name
                except:
                    pass
    except ldap.LDAPError, error_message:
        return ""



