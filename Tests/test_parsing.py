import sqlparse

def discoverComponents(sql):
    """Search for installable/removable components within a string containing
       one or more SQL statemnets"""
    components = []
    parsed = sqlparse.parse(sql)
    for statement in parsed:
        for token in statement.tokens:
            name = None
            typ = None

            # remove newlines, extra spaces for regex
            stmt = str(statement).replace("\n", " ")
            stmt = " ".join(stmt.split())

            for comp in sqlComponents:
                if token.match(Keyword, comp.typ):
                    name = comp.match(stmt)
                    typ = comp.typ

            if name is not None:
                component = AppComponent(name, typ)
                if component not in components:
                    components.append(component)

    # sort alphabetically, should fix drop issues when 'rule on table'
    # is dropped before 'table'
    return sorted(components, key=lambda x: x.typ)