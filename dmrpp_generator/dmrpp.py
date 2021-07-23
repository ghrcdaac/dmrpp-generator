import logging
import os
import re

import boto3
import requests


class DMRpp:
    def __init__(self, host_path='/tmp') -> None:
        self.s3_client = boto3.client('s3')
        self.session = requests.Session()
        self.host_path = host_path

    def get_https_file(self, url, local_path):
        self.get_http_file(url, local_path)

    def download_files(self, url):
        """
        Calls the corresponding download function for the url's protocol. Function names must be of the form
        get_{protocol}_file.
        :param url: Location to find the file to download
        """
        filename = os.path.basename(url)
        local_path = f'{self.host_path}/{filename}'
        protocol = re.match(rf'.+?(?=:)', url).group()
        if not os.path.isfile(local_path):
            self.__getattribute__(f'get_{protocol}_file')(url, local_path)

        return local_path

    def get_http_file(self, url, local_path):
        """
        Downloads the file at the url and stores it at the local path.
        :param url: Url of the file to download.
        :param local_path: Location to write the downloaded file to.
        """
        try:
            response = self.session.get(url)
            with open(local_path, 'wb') as file:
                file.write(response.content)
        except Exception as e:
            logging.error(msg=str(e))
        pass

    def get_s3_file(self, s3_link, local_path):
        """
        Downloads the file at the s3_link and stores it at the local path.
        :param s3_link: s3 link of the file to download.
        :param local_path: Location to write the downloaded file to.
        """
        reg_res = re.match(rf'^.*://([^/]*)/(.*)', s3_link)
        bucket_name = reg_res.group(1)
        key = reg_res.group(2)
        try:
            self.s3_client.download_file(bucket_name, key, local_path)
        except Exception as e:
            logging.error(msg=str(e))
        pass

    def get_dmrpp_option(self, dmrpp_meta):
        """
        :param dmrpp_meta: DMR meta string
        :return A sequential string with the flags and URLs in order
        """
        res_str = '-b '
        for option in dmrpp_meta.get('options'):
            flag = option.get('flag', '')
            res_str = f'{res_str}{flag} '
            file_link = option.get('opt')
            if file_link:
                location = file_link
                download = option.get('download')
                if download == 'true':
                    location = self.download_files(file_link)

                res_str = f'{res_str}{location} '

        return res_str.rstrip(' ')


if __name__ == '__main__':
    test_dict = {
          "options": [
            {
              "flag": "-M"
            },
            {
              "flag": "-s",
              "opt": "https://catalog.uah.edu/grad/colleges-departments/science/earth-system-science/earth-system-science.pdf",
              "download": "true"
            },
            {
              "flag": "-c",
              "opt": "s3://ghrcsbxw-public/aces1cont__1/aces1cont_2002.212_v2.50.tar.cmr.json",
              "download": "true"
            },
            {
              "flag": "-k",
              "opt": "<file3_link_to_s3_or_http>"
            }
          ]
        }

    sn = DMRpp()
    print(f'[{sn.get_dmrpp_option(test_dict)}]')
    # sn.get_http_file(url='https://catalog.uah.edu/grad/colleges-departments/science/earth-system-science/earth-system-science.pdf', host_path='.')
    # sn.get_s3_file(s3_link='s3://ghrcsbxw-public/aces1cont__1/aces1cont_2002.212_v2.50.tar.cmr.json', host_path='.')
    pass
