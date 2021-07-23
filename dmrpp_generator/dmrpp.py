import logging
import re

import boto3
import requests


class DMRpp:
    def __init__(self) -> None:
        self.s3_client = boto3.client('s3')
        self.session = requests.Session()

    def get_http_file(self, url, host_path="/tmp"):
        """
        Downloads a file from the provided url.
        :param url: Location to find the file to download http or https
        :param host_path: Where to store the downloaded file
        """
        filename = url.rsplit('/', 1)[-1]
        try:
            response = self.session.get(url)
            with open(f'{host_path}/{filename}', 'wb') as file:
                file.write(response.content)
        except Exception as e:
            logging.log(level=20, msg=str(e))

    def get_s3_file(self, s3_link, host_path="/tmp"):
        """
        Downloads a file from the provided url.
        :param url: Location to find the file to download from S3
        :param host_path: Where to store the downloaded file
        """
        filename = s3_link.rsplit('/', 1)[-1]
        reg_res = re.match(rf'^.*://([^/]*)/(.*)', s3_link)
        bucket_name = reg_res.group(1)
        key = reg_res.group(2)
        try:
            self.s3_client.download_file(bucket_name, key, f'{host_path}/{filename}')
        except Exception as e:
            logging.log(level=20, msg=str(e))

    def get_dmrpp_option(self, dmrpp_meta):
        """
        :param dmrpp_meta: DMR meta string
        :return A sequential string with the flags and URLs in order
        """
        res_str = ''
        for option in dmrpp_meta.get('options'):
            flag = option.get('flag', '')
            res_str = f'{res_str}{flag} '
            file_link = option.get('opt', '')
            if file_link:
                res_str = f'{res_str}{file_link} '
                download = option.get('download', '')
                if download and download == 'true':
                    protocol = re.match(rf'http|s3', file_link).group()
                    self.__getattribute__(f'get_{protocol}_file')(file_link)

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
