import boto3

class Ec2(object):
    def __init__(self, region, profile):
        self.region = region
        self.profile = profile
        self.client = boto3.client('ec2')

    def describe_instances(self):
        paginator = self.client.get_paginator('describe_instances')
        response_iterator = paginator.paginate()
        instances = []
        for response in response_iterator:
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instances.append(instance)
        return instances

    @property
    def instances(self):
        return self.describe_instances()
