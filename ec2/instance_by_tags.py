import boto3, re, click, json
from base import Ec2

def convert_time_to_string(value):
    if isinstance(value, datetime.datetime):
        return value.__str__()

@click.command()
@click.option("--key", default="Name", help="Key of the Tags to filter")
@click.option("--value", help="Value of the Tags to filter")
def by_tag(key, value):
    ec2 = Ec2("ap-southeast-1", "default")
    origin = []
    return_items = ["PrivateIpAddress", "PublicIpAddress", "KeyName"]
    for instance in ec2.instances:
        for tag in instance.get('Tags', {}):
            if tag['Key'] == key and re.search(value, tag['Value']):
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
        final = json.dumps(final, sort_keys=True, indent=2, default = convert_time_to_string)
        click.echo(final)
    else:
        origin = json.dumps(origin, sort_keys=True, indent=2, default = convert_time_to_string)
        click.echo(origin)

if __name__ == "__main__":
    by_tag()
