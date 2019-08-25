from jinja2 import Environment

Template = Environment(extensions=['jinja2_time.TimeExtension']).from_string
