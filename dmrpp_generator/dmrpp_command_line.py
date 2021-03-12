import os
import json

payload = """
{
    "config": {
        "dmrpp": {
            "create_missing_cf" : true    
        }
    }
}
"""

class DMRPPCommandLine:

    switch_map = {
        "create_missing_cf": "-M"
    }

    def __init__(self, local, config):
        if local == False: self.data = json.loads(config)
        self.local = local

    def get_command(self):
        switches = ""
        for key in self.switch_map:
            add_switch = False
            if self.local:
                add_switch = os.getenv(key.upper(), 'False').lower() in ['true', '1']
            else:
                try:   
                    add_switch = self.data['config']['dmrpp'][key] == True
                except KeyError:
                    pass
            
            if add_switch: switches = switches.join(f" {self.switch_map[key]}")

        return f'get_dmrpp{switches} -b'

if __name__ == "__main__":
    dmrpp = DMRPPCommandLine(True, payload)
    print(dmrpp.get_command())