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

    def describe_security_groups(self):
        paginator = self.client.get_paginator('describe_security_groups')
        response_iterator = paginator.paginate()
        secs = []
        for response in response_iterator:
            for sec in response['SecurityGroups']:
                secs.append(sec)
        return secs

    def describe_volumes(self):
        paginator = self.client.get_paginator('describe_volumes')
        response_iterator = paginator.paginate()
        volumes = []
        for response in response_iterator:
            for volume in response['Volumes']:
                volumes.append(volume)
        return volumes

    @property
    def instances(self):
        return self.describe_instances()

    @property
    def security_groups(self):
        return self.describe_security_groups()

    @property
    def volumes(self):
        return self.describe_volumes()
