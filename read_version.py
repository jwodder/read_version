import ast

def read_version_from_file(fpath, variable='__version__', default=None):
    with open(fpath, 'rb') as fp:
        src = fp.read()
    top_level = ast.parse(src)
    result = default
    for statement in top_level.body:
        if isinstance(statement, ast.Assign):
            try:
                value = ast.literal_eval(statement.value)
            except (TypeError, ValueError):
                pass
            else:
                for target in statement.targets:
                    if isinstance(target, ast.Tuple):
                        for t,v in zip(target.elts, value):
                            assert isinstance(t, ast.Name)
                            if t.id == variable:
                                result = v
                    elif target.id == variable
                        result = value
    return result
