import json


def dice(data, schema):
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


if __name__ == '__main__':
    with open('config.json') as f:
        data = json.load(f)

    with open('schema.json') as f:
        schema = json.load(f)
    print(dice(data, schema))
