def urlclean(path):
    if path[-1:] == '/':
        path = path[:-1]
    if path[:1] == '/':
        path = path[1:]
    return path
    
def urlsplit(path):
    return urlclean(path).split('/')

def urljoin(*args):
    return '/'.join([urlclean(_) for _ in args if len(_) > 0])

def parse_querystring(segment):
    try:
        idx = segment.index('?')
        qs = segment[idx + 1:]
        part_array = qs.split('&')

        results = []
        for part in part_array:
            single_part_array = part.split('=')
            name = single_part_array[0]
            value = ''
            if len(single_part_array) > 1:
                value = single_part_array[1]
            
            results.append((name, value))

        return results
    except:
        return []