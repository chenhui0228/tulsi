#!/usr/bin/env python

# Copyright (c) 2015 Vedams Software Solutions PVT LTD
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import logging.handlers
import logging
import socket
import ConfigParser
import time
from gzip import GzipFile
from io import BufferedReader
import struct
from MessageEncode import MessageEncode
from HostInfo import HostInfo
import json

logging.basicConfig(filename='/var/log/tulsi_server.log',level=logging.DEBUG)

class Server():
    """
    classdocs
    """

    def __init__(self):
        """
        Constructor
        """
        # Read the configuration parameters from tulsi.conf
        self.timestr = time.strftime("%Y:%m:%d-%H:%M:%S")
        self.conf = ConfigParser.ConfigParser()
        try:
            self.conf.read('/etc/tulsi/tulsi.conf')
            self.udp_ip = self.conf.get('tulsi', 'host')
            self.udp_port = int(self.conf.get('tulsi', 'port'))

            # printing the host and port of tulsi

            logging.info('%s The IP of the host: %s' % (self.timestr, self.udp_ip))
            logging.info('%s The  Port number of the host :%s' %  (self.timestr, self.udp_port))
        except:
            # Error message of tulsi not working
            logging.error('The tulsi configuration file is not found')

        # Creating objects of MessageEncode and HostInfo
        msg_encode = MessageEncode()
        host_info = HostInfo()

        # Initializing empty lists
        self.drives = []
        self.service = []
        self.ip_array = []
        self.ring_ip = []
        self.ring_conf_ip = []
        self.ring_drives = []
        self.ip_set_array = []
        self.my_ring_conf = dict()
        # Read the ring Configuration file
        self.gz_file = GzipFile("/etc/swift/container.ring.gz", 'rb')
        if hasattr(self.gz_file, '_checkReadable'):
            self.gz_file = BufferedReader(self.gz_file)
        magic = self.gz_file.read(4)
        if magic == 'R1NG':
            version, = struct.unpack('!H', self.gz_file.read(2))
            if version == 1:
                #self.ring_data = self.read_ring_file(self.gz_file)
                self.read_ring_file(self.gz_file)
            else:
                logging.error('%s Unknown ring format version %d' % (self.timestr,version))
                raise Exception('Unknown ring format version %d' % version)

        # While loop to continuously check the status of  swift services and
        # drives and send information to tulsi client
        while True:
            self.ip_array = host_info.read_ip()
            self.service = host_info.read_services()
            self.drives = host_info.read_drives(self.drives)
            self.message = msg_encode.create_message(self.my_ring_conf,
                                                     self.ring_conf_ip,
                                                     self.ip_array,
                                                     self.service, self.drives)
            sock = socket.socket(socket.AF_INET,  # Internet
                                 socket.SOCK_DGRAM)  # UDP
            sock.sendto(self.message, (self.udp_ip,self.udp_port))
            time.sleep(5)
            self.ip_array = []
            self.service = []
            self.drives = []

    #  Function to extract the ip  and devices from container.ring.gz
    def read_ring_file(self, sgz_file):
        self.json_len, = struct.unpack('!I', self.gz_file.read(4))
        self.ring_dict = json.loads(self.gz_file.read(self.json_len))
        logging.info('Extracted Ring data : %s', self.ring_dict)
        self.ring_dict['replica2part2dev_id'] = []
        self.partition_count = 1 << (32 - self.ring_dict['part_shift'])
        #logging.info('%s The Ip from ring file %s' % (self.timestr, self.ring_conf_ip[]]))
        #logging.info('%s The IP of host machine %s' %(self.timestr, self.ip_array))  
        for x in self.ring_dict['devs']:
            self.mystring = x
            if self.mystring['ip'] in self.my_ring_conf:
                # append the new number to the existing array at this slot
                self.my_ring_conf[
                    self.mystring['ip']].append(self.mystring['device'])
            else:
                # create a new array in this slot
                self.my_ring_conf[self.mystring['ip']] = [self.mystring
                                                          ['device']]
                self.ring_conf_ip.append(self.mystring['ip'])
                logging.info('%s The Ip from ring file %s' % (self.timestr, self.ring_conf_ip))
                logging.info('%s The IP of host machine %s' %(self.timestr, self.ip_array))
