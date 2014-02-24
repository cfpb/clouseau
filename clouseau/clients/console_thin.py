from abstract import AbstractClient
from jinja2 import Template, Environment, PackageLoader

class ConsoleThinClient(AbstractClient):
    """
    Command-line client for Clouseau that emits the bare essentials. Useful for automated environments, such as continuous integration
    """

    def __init__(self):
        pass

    def render(self, terms, data):
        """
        Emit all findings to console
        """
        matches = []
        matches = [term for term in data if term != 'meta' and len(data[term])]
        env = Environment(loader=PackageLoader('clouseau', 'templates'))
        template = env.get_template('console_thin.html')

        data_to_render = template.render(data=data, has_matches=len(matches) > 0)
        print data_to_render
