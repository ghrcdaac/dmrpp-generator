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
    
    def get_command(self, config, path, file_name):
        switches = ""

        data = None
        if config != None: data = json.loads(config)

        for key in self.switch_map:
            add_switch = False
            if data:
                try:   
                    add_switch = data['config']['meta']['dmrpp'][key] == True
                except KeyError:
                    pass               
            else:
                add_switch = os.getenv(key.upper(), 'False').lower() in ['true', '1']
                           
            if add_switch: switches = switches.join(f" {self.switch_map[key]}")

        return f'get_dmrpp{switches} -b {path} -o {file_name}.dmrpp {os.path.basename(file_name)}'

if __name__ == "__main__":
    generator = DMRPPCommandLine()
    print(generator.get_command(payload, "foo", "bar"))