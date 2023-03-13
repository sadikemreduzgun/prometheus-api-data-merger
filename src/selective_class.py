# metric['data']['result']['0']['metric']['{upper ones}']
class Query_selector:

    def __init__(self):
        self.node_keys = ['instance', 'job', 'device', 'fstype', 'mountpoint', '__name__', 'cpu', 'name', 'type', 'collector']
        self.libv_keys = ['__name__', 'domain', 'instance', 'job', 'target_device']


    def select_node(self, query, key):
        pass

    def select_libvirt(self):
        pass
