from passrotate.provider import Provider, ProviderOption, register_provider

class Noop(Provider):
    """
    [noop]
    username=A username for noop
    cassette=Path to file to record changes to
    """
    name = "noop"
    domains = []
    options = {
        "username": ProviderOption(str, "A username for noop"),
        "cassette": ProviderOption(str, "Path to file to record changes to"),
    }

    def __init__(self, options):
        self.username = options["username"]
        self.fh = open(options['cassette'], 'w+')

    def prepare(self, old_password):
        self.fh.write("prepare {}: {}\n".format(self.username, old_password))

    def execute(self, old_password, new_password):
        self.fh.write(
            "execute {}: {} {}\n".format(self.username, old_password, new_password))

register_provider(Noop)
