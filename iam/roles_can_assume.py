import boto3, re, sys, itertools
import pprint
pp = pprint.PrettyPrinter(indent=4)

def get_statements(roles, value_to_find):
    temp = []
    for order, role in enumerate(roles):
        for state in role['AssumeRolePolicyDocument']['Statement']:
            for value in state['Principal'].values():
                if isinstance(value, str):
                    temp.append(
                        (roles[order]['Arn'], roles[order]['RoleName'], list(value))
                    )
                elif isinstance(value, list):
                    temp.append(
                        (roles[order]['Arn'], roles[order]['RoleName'], value)
                    )
    final = []
    for arn, role, principals in temp:
        for item in principals:
            if re.search(value_to_find, item):
                final.append(
                        {
                            'Arn': arn,
                            'RoleName':role
                        }
                    )
    return final

if __name__ == "__main__":
    iam = boto3.client('iam')
    paginator = iam.get_paginator('list_roles')
    response_iterator = paginator.paginate()

    roles = []
    for response in response_iterator:
        for role in response['Roles']:
            roles.append(role)

    while True:
        pp.pprint(get_statements(roles, input("\nPlease input the role you want to find: ")))
