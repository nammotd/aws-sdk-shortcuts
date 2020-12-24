import re, click, json, datetime
from base import Iam

def convert_time_to_string(value):
    if isinstance(value, datetime.datetime):
        return value.__str__()

@click.command()
@click.option('--name', help="a part of a Role's name")
def by_role_statements(name):
    iam = Iam("ap-southeast-1", "default")
    origin = []
    return_items = ["Arn", "RoleName", "Description"]
    for role in iam.roles:
        for state in role['AssumeRolePolicyDocument']['Statement']:
            for item in state['Principal'].values():
                if isinstance(item, str):
                    if re.search(name, item):
                        origin.append(role)
                elif isinstance(item, list):
                    for elem in item:
                        if re.search(name, elem):
                            origin.append(role)
    if return_items:
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
    by_role_statements()
