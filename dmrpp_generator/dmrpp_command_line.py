import os
import json

"""
Example Cumulus configuration for supported get_dmrpp switches
"""
payload = """
{
    "config": {
        "meta": {
            "hyrax_processing": true,
            "dmrpp": {
                "create_missing_cf" : true    
        }
    }
}
"""
class DMRPPCommandLine:
    """
    Class to generate dmrpp optional command line arguments either from 
    - environment variable settings (config=None) or 
    - Cumulus configuration (config=str)
    """

    """
    Supported get_dmrpp switches
    """
    switch_map = {
        "create_missing_cf": "-M"
    }
    
    def __init__(self, config):
        """
        :param config: Cumulus configuration in json format. If this is null or empty environment variables are used.
        """
        self.data = None
        if config != None: self.data = json.loads(config)

    """
        Generates base get_dmrpp command based on configuration/environment
    """
    def get_command(self):
        switches = ""
        for key in self.switch_map:
            add_switch = False
            if self.data:
                try:   
                    add_switch = self.data['config']["meta"]['dmrpp'][key] == True
                except KeyError:
                    pass               
            else:
                add_switch = os.getenv(key.upper(), 'False').lower() in ['true', '1']
                           
            if add_switch: switches = switches.join(f" {self.switch_map[key]}")

        return f'get_dmrpp{switches} -b'

if __name__ == "__main__":
    generator = DMRPPCommandLine(payload)
    print(generator.get_command())