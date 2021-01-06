import boto3, re, click, json, datetime
from base import Ec2

def convert_time_to_string(value):
    if isinstance(value, datetime.datetime):
        return value.__str__()

def check_input(ctx, param, value):
    failed_statement = "Input need to be in forms of Id:vol-123123 or Name:kubernetes"
    try:
        prefix,suffix = value.split(":")
        if prefix in ['Id', 'Name']:
            return suffix
        else:
            raise click.BadParameter(failed_statement)
    except ValueError:
        raise click.BadParameter(failed_statement)

@click.command()
@click.option("--value", default="Name", help="Either Id:vol-123123 or Name:kubernetes", callback=check_input)
@click.option('--filter-keys', help="A list of key to extract only, seperate by a comma")
def by(value, filter_keys):
    """
        This command lists all EBS Volumes which is matched your input
    """
    ec2 = Ec2("ap-southeast-1", "default")
    origin = []
    for volume in ec2.volumes:
        if re.search(value, volume['VolumeId']):
            origin.append(volume)
        elif (tags := volume.get("Tags", None)):
            for tag in tags:
                if tag['Key'] == "Name" and re.search(value, tag['Value']):
                    origin.append(volume)

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
    by()
