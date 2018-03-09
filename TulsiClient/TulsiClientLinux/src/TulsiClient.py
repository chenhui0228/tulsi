#!/usr/bin/env python
# Copyright (c) 2015 Vedams Software Solutions PVT LTD
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ProxyNodeInfo import ProxyNodeInfo
from StorageNodeInfo import StorageNodeInfo
from Result import Result
import logging
import ConfigParser
import socket
import os

logging.basicConfig(filename='/var/log/tulsi_client.log',level=logging.DEBUG)

CUR_PATH = os.path.abspath(__file__)
CUR_DIR = os.path.dirname(CUR_PATH)

class TulsiClient(object):

    def __init__(self):
        # Setting the logger tulsiclient
        self.logger = logging.getLogger("tulsiclient")
        # Reading configuration parameters from tulsiclient.conf
        self.conf = ConfigParser.ConfigParser()
        try
            self.conf.read(os.path.join(CUR_DIR, 'tulsiclient.conf'))
            self.udp_ip = self.conf.get('tulsi', 'host')
            self.udp_port = int(self.conf.get('tulsi', 'port'))

        # printing the host and port of tulsi
            self.logger.info('The IP of the host: %s', self.udp_ip)
            self.logger.info('The  Port number of the host :%s', self.udp_port)
        except:
            # Error message of tulsi not working
            self.logger.error('The tulsi configuration file is not found')

        # Creating objects for ProxyNodeInfo , StorageNodeInfo,
        # Result and status of node

        proxy_node = ProxyNodeInfo()
        storage_node = StorageNodeInfo()
        result = Result()

        # Initializing empty list
        self.storage_node_read = []
        self.proxy_node_read = []
        self.storage_node_drive = []
        self.storage_node_status = []
        self.storage_node_list = []
        self.proxy_node_list = []
        self.storage_node_list_storage_suffix = []
        self.storage_node_list_drive_suffix = []
        self.storage_node_list_suffix_id = []
        self.storage_node_drives_file = []
        self.storage_node_storage_file = []
        self.storage_node_status_storage_file = []
        self.proxy_node_list_proxy_suffix = []
        self.proxy_node_status_file = []

        # opening and binding the port to socket
        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        sock.bind((self.udp_ip, self.udp_port))

        # While loop to continuously receive message from Tulsi Server
        # to get update status of  storage/ proxy node

        while True:
                self.data, self.addr = sock.recvfrom(65507)
                self.storage_node_list = \
                    storage_node.read_storage_node_list(self.data,
                                                        self.storage_node_list)
                self.proxy_node_list, self.proxy_node_status_file = \
                    proxy_node.read_proxy_node_list(self.data)

                result.write_config_ui(self.proxy_node_list,
                                       self.storage_node_list,
                                       self.storage_node_drives_file)
                result.write_status_ui(self.storage_node_storage_file,
                                       self.proxy_node_status_file,
                                       self.storage_node_status_storage_file)
                self.storage_node_drives_file, self.storage_node_storage_file, self.storage_node_status_storage_file = \
                    storage_node.read_storage_node_config(
                        self.data,
                        self.storage_node_list)

