from .substrate_interface import create_connection_by_url
from .metadata_interaction import get_properties

from substrateinterface import SubstrateInterface


class Chain():
    substrate: SubstrateInterface

    def __init__(self, arg):
        self.chainId = arg.get("chainId")
        self.parentId = arg.get("parentId")
        self.name = arg.get("name")
        self.assets = arg.get("assets")
        self.nodes = arg.get("nodes")
        self.explorers = arg.get("explorers")
        self.addressPrefix = arg.get("addressPrefix")
        self.externalApi = arg.get("externalApi")
        self.options = arg.get("options")
        self.substrate = None
        self.properties = None

    def create_connection(self, type_registry=None) -> SubstrateInterface:
        for node in self.nodes:
            try:
                print("Connecting to ", node.get('url'))
                self.substrate = create_connection_by_url(node.get('url'), type_registry=type_registry)
                print("Connected to ", node.get('url'))
                return self.substrate
                # if self.substrate.websocket.connected is True:
                #     return self.substrate
                # print(f"Can't connect to endpoint {node.get('url')} for the {self.name}")
            except:
                print("Can't connect to that node")
                continue

        print("Can't connect to all nodes of network", self.name)

    def recreate_connection(self) -> SubstrateInterface:
        if self.substrate is None:
            raise Exception("No connection was created before")

        for node in self.nodes:
            try:
                print("Connecting to ", node.get('url'))
                self.substrate.url = node.get('url')
                self.substrate.connect_websocket()
                print("Connected to ", node.get('url'))
                return self.substrate
                # if self.substrate.websocket.connected is True:
                #     return self.substrate
                # print(f"Can't connect to endpoint {node.get('url')} for the {self.name}")
            except:
                print("Can't connect to that node")
                continue

        print("Can't connect to all nodes of network", self.name)

    def close_substrate_connection(self):
        self.substrate.close()


    def init_properties(self):
        if (self.properties):
                return self.substrate
        self.properties = get_properties(self.substrate)
