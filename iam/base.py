import boto3

class Iam(object):
    def __init__(self, region, profile):
        self.region = region
        self.profile = profile
        self.client = boto3.client('iam')

    def list_roles(self):
        paginator = self.client.get_paginator('list_roles')
        response_iterator = paginator.paginate()
        roles = []
        for response in response_iterator:
            for role in response['Roles']:
                roles.append(role)

        return roles

    @property
    def roles(self):
        return self.list_roles()
