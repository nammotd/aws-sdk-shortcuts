import boto3, re, click, json, datetime
from base import Ec2

def convert_time_to_string(value):
    if isinstance(value, datetime.datetime):
        return value.__str__()

@click.command()
@click.option("--ip", help="A desired ip to search for")
@click.option('--filter-keys', help="A list of key to extract only, seperate by a comma")
def by_ip(ip, filter_keys):
    """
        This command lists all Ec2 instances which possess an Ip matched your input Ip
    """
    ec2 = Ec2("ap-southeast-1", "default")
    origin = []
    for instance in ec2.instances:
        if (instance_ip := instance.get("PublicIpAddress")) is not None and re.search(ip, instance_ip):
            origin.append(instance)
        elif (instance_ip := instance.get("PrivateIpAddress")) is not None and re.search(ip, instance_ip):
            origin.append(instance)

    if filter_keys:
        final = []
        return_items = filter_keys.split(',')
        for unit in origin:
            _dict = {}
            for key,value in unit.items():
                if key in return_items:
                    _dict[key] = value
            if _dict:
                final.append(_dict)
        final = json.dumps(final, sort_keys=True, indent=2, default = convert_time_to_string,
                )
        click.echo(final)
    else:
        origin = json.dumps(origin, sort_keys=True, indent=2, default = convert_time_to_string)
        click.echo(origin)

if __name__ == "__main__":
    by_ip()
