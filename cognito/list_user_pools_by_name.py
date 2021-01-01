import boto3, re, click, json, datetime
from base import Cognito

def convert_time_to_string(value):
    if isinstance(value, datetime.datetime):
        return value.__str__()

@click.command()
@click.option("--name", help="Part of a Cognito's name")
@click.option('--filter-keys', help="A list of key to extract only, seperate by a comma")
def by_cognito_name(name, filter_keys):
    """
        This command lists all Cognito matched an string
    """
    cognito = Cognito("ap-soutehast-1", "default")
    origin = []
    for user_pool in cognito.user_pools:
        if re.search(name, user_pool['Name']):
            origin.append(cognito.describe_user_pool(user_pool))

    if filter_keys:
        final = []
        return_items = filter_keys.split(",")
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
    by_cognito_name()
