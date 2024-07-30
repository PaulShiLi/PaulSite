
class util:
    def flattenDict(a: dict, parent_key='', separator='_', leaveLast: bool = True, parent: bool = True) -> dict:
        lastItems = []
        items = []
        for key, value in a.items():
            new_key = parent_key + separator + key if parent_key else key
            if isinstance(value, dict):
                nItems, nLastItems = util.flattenDict(value, new_key, separator=separator, parent=False)
                items.extend(nItems.items())
                lastItems += nLastItems
            else:
                if leaveLast:
                    lastItems.append((parent_key, {
                                key: value
                            })
                    )
                else:
                    items.append((new_key, value))
        if parent and leaveLast:
            returnItems = {}
            for key, val in lastItems:
                if key in returnItems:
                    returnItems[key].update(val)
                else:
                    returnItems[key] = val
            return returnItems
        return dict(items), lastItems if not parent else dict(items)

