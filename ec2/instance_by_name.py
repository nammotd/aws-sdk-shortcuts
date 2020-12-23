import boto3, re
import pprint
pp = pprint.PrettyPrinter(indent=4)

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

    def by_tag(self, _key, _value):
        origin = []
        return_items = ["PrivateIpAddress", "PublicIpAddress", "Tags", "KeyName"]
        for instance in self.instances:
            for tag in instance.get('Tags', {}):
                if tag['Key'] == _key and re.search(_value, tag['Value']):
                    origin.append(instance)

        if return_items:
            final = []
            for unit in origin:
                _dict = {}
                for key,value in unit.items():
                    if key in return_items:
                        _dict[key] = value
                if _dict:
                    final.append(_dict)

            return final
        return origin

if __name__ == "__main__":
    all_ec2 = Ec2("ap-southeast-1", "default")
    while True:
        pp.pprint(all_ec2.by_tag(input("Please input tag.Key: "), input("Please input tag:Value: ")))
