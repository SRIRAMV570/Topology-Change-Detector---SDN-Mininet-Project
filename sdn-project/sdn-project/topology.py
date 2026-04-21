from mininet.topo import Topo

class MyTopo(Topo):
    def build(self):
        # Switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        # Hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        # Host connections
        self.addLink(h1, s1)
        self.addLink(h2, s2)

        # Primary link
        self.addLink(s1, s2)

        # Backup path
        self.addLink(s1, s3)
        self.addLink(s3, s2)

topos = {'mytopo': (lambda: MyTopo())}
