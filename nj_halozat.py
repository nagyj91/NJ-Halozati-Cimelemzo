import ipaddress


def nj_elemzes(cim):
    kapcsolat = ipaddress.ip_interface(cim.strip())
    halozat = ipaddress.ip_network(cim.strip(), strict=False)
    ip = ipaddress.ip_address(str(kapcsolat.ip))
    if halozat.version == 4 and halozat.prefixlen < 31:
        elso = halozat.network_address + 1
        utolso = halozat.broadcast_address - 1
        darab = halozat.num_addresses - 2
    else:
        elso = halozat.network_address
        utolso = halozat.broadcast_address
        darab = halozat.num_addresses
        if halozat.version == 6 and halozat.prefixlen < 127:
            elso += 1
            darab -= 1
    return {
        'IP-cím': str(ip),
        'IP-verzió': f'IPv{ip.version}',
        'Hálózati cím': str(halozat.network_address),
        'Prefix': f'/{halozat.prefixlen}',
        'Hálózati maszk': str(halozat.netmask),
        'Broadcast': str(halozat.broadcast_address) if ip.version == 4 else 'IPv6 esetén nincs broadcast',
        'Első használható cím': str(elso),
        'Utolsó használható cím': str(utolso),
        'Használható címek száma': str(darab),
        'Címtípus': 'Privát' if ip.is_private else 'Globális' if ip.is_global else 'Speciális',
        'Visszacsatolási cím': 'Igen' if ip.is_loopback else 'Nem',
        'Hálózat CIDR alakban': str(halozat),
    }


class NJHalozat:
    def __init__(self):
        self.eredmeny = {}

    def nj_vizsgal(self, cim):
        eredmeny = nj_elemzes(cim)
        self.eredmeny = eredmeny
        return eredmeny

    def nj_torol(self):
        self.eredmeny = {}
