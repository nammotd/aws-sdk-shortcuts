import boto3, re, click, json
from base import Iam

def convert_time_to_string(value):
    if isinstance(value, datetime.datetime):
        return value.__str__()

@click.command()
@click.option('--name', help="a part of a Role's name")
@click.option('--filter-keys', help="a part of a Role's name")
def by_role_name(name, filter_keys):
    iam = Iam("ap-southeast-1", "default")
    origin = []
    return_items = ["Arn", "RoleName", "Description"]
    for role in iam.roles:
        if re.search(name, role['RoleName']):
            origin.append(role)

    if filter_keys:
        return_items = filter_keys.split(",")
        final = []
        for unit in origin:
            _dict = {}
            for key,value in unit.items():
                if key in return_items:
                    _dict[key] = value
            if _dict:
                final.append(_dict)
        click.echo(
                json.dumps(final, sort_keys=True, indent=2, default = convert_time_to_string)
                )
    else:
        click.echo(
                json.dumps(origin, sort_keys=True, indent=2, default=convert_time_to_string)
                )

if __name__ == "__main__":
    by_role_name()
