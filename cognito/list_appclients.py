import boto3, re, click, json, datetime
from base import Cognito

def convert_time_to_string(value):
    if isinstance(value, datetime.datetime):
        return value.__str__()

@click.command()
@click.option("--name", help="name of the required Cognito")
def by_cognito_name(name):
    cognito = Cognito("ap-soutehast-1", "default")
    return_items = []
    origin = cognito.list_user_pool_clients(name)
    final = []
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
    by_cognito_name()
