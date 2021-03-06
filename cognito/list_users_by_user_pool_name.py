import boto3, re, click, json, datetime
from base import Cognito

cognito = Cognito("ap-soutehast-1", "default")
def convert_time_to_string(value):
    if isinstance(value, datetime.datetime):
        return value.__str__()

@click.command()
@click.option("--name", help="Name of the Cognito User Pool to get all users")
@click.option('--filter-keys', help="A list of key to extract only, seperate by a comma")
def by_cognito_name(name, filter_keys):
    """
        This command extracts all Users within a Cognito
    """
    origin = cognito.list_users(name)
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
