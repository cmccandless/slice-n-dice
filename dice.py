def dice(data, schema):
    if 'select' in schema:
        schema = schema['select']
        if not isinstance(data, dict):
            raise TypeError('can only select from a dictionary')
        return dice(data[schema['skey']], schema)
    elif not isinstance(data, list):
        raise TypeError('data is not a list')
    for key in reversed(schema.get('sort', [])):
        reverse = key[:1] == '-'
        key = key.lstrip('-')
        print(key, reverse)
        data = sorted(
            data,
            key=lambda e: e[key],
            reverse=reverse
        )
    if 'keys' in schema:
        if len(schema['keys']) == 1:
            data = [
                e[schema['keys'][0]] for e in data
            ]
        else:
            data = [
                {
                    k2: v for k2, v in e.items()
                    if k2 in schema['keys']
                }
                for e in data
            ]
    if 'groupby' in schema:
        schema = schema['groupby']
        key = schema['gkey']
        keys = set()
        list_key = schema.get('list_key', False)
        for e in data:
            if key in e:
                if list_key:
                    for k in e[key]:
                        keys.add(k)
                else:
                    keys.add(e[key])
        if not keys:
            raise KeyError('unknown gkey ' + key)
        data = {
            k: dice(
                [
                    e for e in data
                    if (not list_key and e[key] == k) or
                    (list_key and k in e[key])
                ],
                schema
            )
            for k in keys
        }
    return data
