class TextProcessor():
    @staticmethod
    def camel(snake_str):
        components = snake_str.split('_')
        # We capitalize the first letter of each component except the first one
        # with the 'title' method and join them together.
        return ''.join(x.title() for x in components[0:])

class PythonTextProcessor(TextProcessor):

    @staticmethod
    def pydantic_column(column_type):
        pydantic_column_type_map = {
            'uuid': 'UUID4',
            'text': 'str',
            'varchar': 'str',
            'timestamp': 'datetime.datetime',
            'geom': 'str',
            'jsonb': 'str',
            'boolean': 'bool',
        }

        try:
            return pydantic_column_type_map[column_type]
        except KeyError:
            return column_type
