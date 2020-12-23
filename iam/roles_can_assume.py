import boto3, re, sys
import pprint
pp = pprint.PrettyPrinter(indent=4)

def get_statements(roles, value_to_find):
    temp = []
    for order, role in enumerate(roles):
        for state in role['AssumeRolePolicyDocument']['Statement']:
            if  'Principal' in state and 'AWS' in state['Principal']:
                temp.append(
                    (roles[order]['Arn'], roles[order]['RoleName'], state['Principal']['AWS'])
                )
    final = []
    for first,key,value in temp:
        if isinstance(value, str):
            if re.search(value_to_find, value):
                final.append(dict(Arn=first, RoleName=key))
        elif isinstance(value, list):
            for item in value:
                if re.search(value_to_find, item):
                    final.append(dict(Arn=first, RoleName=key))

    return final
if __name__ == "__main__":
    iam = boto3.client('iam')
    call = iam.list_roles()
    roles = call['Roles']
    while call['IsTruncated'] and call['Marker']:
        token = call['Marker']
        call = iam.list_roles(
                Marker = token
                )
        roles += call['Roles']
    while True:
        pp.pprint(get_statements(roles, input("\nPlease input the role you want to find: ")))
