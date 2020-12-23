import boto3, re, sys, itertools
import pprint
pp = pprint.PrettyPrinter(indent=4)

def get_rolename(roles, value_to_find):
    temp = []
    return_items = ["Arn", "RoleName"]

    for role in roles:
        if re.search(value_to_find, role['RoleName']):
            temp.append(role)

    if return_items:
        final = []
        for role in temp:
            _dict = {}
            for key,value in role.items():
                if key in return_items:
                    _dict[key] = value
            if _dict:
                final.append(_dict)

        return final

    return temp

if __name__ == "__main__":
    iam = boto3.client('iam')
    paginator = iam.get_paginator('list_roles')
    response_iterator = paginator.paginate()

    roles = []
    for response in response_iterator:
        for role in response['Roles']:
            roles.append(role)

    while True:
        pp.pprint(get_rolename(roles, input("\nPlease input the role you want to find: ")))
