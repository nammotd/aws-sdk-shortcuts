def filter_keys():
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
