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
import json
from Service import Service
from copy import deepcopy


class StorageNodeInfo(object):

    def __init__(self):
        print "Main class "
        self.service = Service()
        self.storage_node_list = []
        self.storage_node_list_temp = None
        self.storage_node_list_temp_drive_suffix = None
        self.storage_node_list_temp_storage_suffix = None
        self.storage_node_list_storage_suffix = []
        self.storage_node_list_drive_suffix = []
        self.storage_node_drives_file = []
        self.storage_node_storage_file = []
        self.status_drives = []
        self.status_drives1 = None
        self.storage_node_read_value_temp = None
        self.number_drives = None
        self.hostname = None
        self.service_status = None
        self.status = None
        self.storage_node_status_storage_file = []
        storage_node_list = []

# Function to generate the storage node list

    def read_storage_node_list(self, data, storage_node_list):
        self.storage_node_list = storage_node_list
        self.data = data
        if (self.read_config_data_storage_name(self.data) is not None):
            self.storage_node_list_temp = \
                self.read_config_data_storage_name(self.data)
        self.storage_node_list_temp_storage_suffix = None
        self.storage_node_list_temp_drive_suffix = None
        if len(self.storage_node_list) == 0 \
                and str(self.read_config_data_storage_name(data)) != "None":

            self.append_list(self.storage_node_list_temp,
                             self.storage_node_list)

        elif self.storage_node_list_temp is None:
                print "the storage_list is not appended"
        else:
            if self.storage_node_list_temp in self.storage_node_list:
                print "The name is present"
            else:
                self.append_list(self.storage_node_list_temp,
                                 self.storage_node_list)
        return self.storage_node_list

# Function to read data packet from tulsi server and find the presence of
# storage node name and return it
    def read_config_data_storage_name(self, data):
        data = json.loads(data)
        if not set(data['host_ip']).isdisjoint(data['conf_ring_ip']):
                    self.storage_node = str(data['hostname'])
                    storage_node_list = str(self.storage_node)
                    return storage_node_list

    def append_list(self, storage_node_list_temp, storage_node_list):
            self.storage_node_list = []
            self.storage_node_list = storage_node_list
            self.storage_node_list_temp = storage_node_list_temp
            self.storage_node_list_temp_storage_suffix = \
                "%s:s%s" % (self.storage_node_list_temp,
                            str(len(self.storage_node_list)+1))
            self.storage_node_list_temp_drive_suffix = \
                "%s:ds%s" % (self.storage_node_list_temp,
                             (str(len(self.storage_node_list)+1)))

            self.storage_node_list_storage_suffix.append(
                self.storage_node_list_temp_storage_suffix)
            self.storage_node_list_drive_suffix.append(
                self.storage_node_list_temp_drive_suffix)
            self.storage_node_list.append(
                self.storage_node_list_temp
            )

    def read_config_data_storage(self, data):
        self.storage_node = self.service.STORAGE_NODE
        self.services_status_down = []
        self.num_drives = 0
        self.data = json.loads(data)
        self.status_drives = []
        for l in self.data['host_ip']:
            for m in self.data['conf_ring_ip']:
                if(l == m):
                    self.ip_host = str(l)
                    self.list_drives_ip = " "
                    for n in self.data['conf_ring'][self.ip_host]:
                            self.list_drives = str(n)
                            if(len(self.list_drives_ip)) == 0:
                                self.list_drives_ip = self.list_drives
                            else:
                                self.list_drives_ip = "%s,%s" % (
                                    self.list_drives_ip, self.list_drives)
                    self.list_drives = self.data['conf_ring'][self.ip_host]
                    for n in self.list_drives:
                        for l in self.data['drives']:
                            if n == l:
                                self.status_drives.append('g')
                                break
                            #elif(l == (len(self.data['drives']))-1):
                            elif (self.data['drives'].index(l) == (len(self.data['drives']))-1):
                                self.status_drives.append('b')
                                break
                    # Loop dealing with status of services
                    self.status_services_flag = "g"
                    self.services_status_down = []
                    for n in self.data['services']:
                        if n == self.service.STORAGE_NODE[
                                self.data['services'].index(n)]:
                            continue
                        else:
                            self.status_services_flag = "w"
                            self.services_status_down.append(n)

                    # Loop Dealing with status of drives
                    for i in self.status_drives:
                        if i == "b":
                            self.status_services_flag = "b"

                    for i in range(0, len(self.status_drives)):
                        if(i == 0):
                            self.status_drives1 = self.status_drives[i]
                        else:
                            self.status_drives1 = \
                                "%s,%s" % (self.status_drives1,
                                           self.status_drives[i]
                                           )

                    self.storage_node = \
                        "%s %s:%s,%s,%s" % (str(self.data['hostname']),
                                            self.list_drives_ip,
                                            str(self.data['hostname']),
                                            self.status_services_flag,
                                            self.status_drives1)
                    self.storage_node_list = str(self.storage_node)

                    return str(self.storage_node_list), str(len(
                        self.data['conf_ring'][self.ip_host])),\
                        str(self.list_drives_ip),\
                        str(self.data['hostname']),\
                        str(self.status_services_flag),\
                        "%s,%s" % (str(self.status_services_flag),
                                   self.status_drives1),\
                        str(self.services_status_down)

    def read_storage_node_config(self, data, storage_node_list):

        """

        :type self: object
        """
        #print storage_node_list

        if self.read_config_data_storage(data) is not None:

            (self.storage_node_read_value_temp,
             self.number_drives,
             self.list_drives,
             self.hostname, self.service_status, self.status,
             self.service_down) = self.read_config_data_storage(data)
            # print len(self.storage_node_list)
            # self.storage_node_drives_file = storage_node_storage_file
            # Read   configuration of cluster
            if len(self.storage_node_drives_file) == 0:
                for i in storage_node_list:
                    if(self.hostname == i):
                        print "entering the appending loop"
                        len_i = storage_node_list.index(i)
                        k = "%s,%s" % (
                            str(self.storage_node_list_drive_suffix[len_i]),
                            str(self.number_drives))
                        self.storage_node_drives_file.append(str(k))
                        m = "%s Names%s" % (
                            str(self.storage_node_list_storage_suffix[len_i]),
                            str(self.list_drives)
                        )
                        self.storage_node_storage_file.append(str(m))
                        n = "%s,%s,%s" % (
                            str(self.storage_node_list_drive_suffix[len_i]),
                            str(self.service_down), self.status)
                        self.storage_node_status_storage_file.append(str(n))

            elif len(self.storage_node_drives_file) != 0:
                print "Entering block with more size"
                for i in range(0,len(storage_node_list)):
                    if(self.hostname == storage_node_list[i]):
                        l = str(self.storage_node_list_drive_suffix[i]) + "," +str(self.number_drives)
                        m = str(self.storage_node_list_storage_suffix[i])+" "+"Names"+str(self.list_drives)
                        n = str(self.storage_node_list_storage_suffix[i])+","+str(self.service_down)+","+self.status
                        p = storage_node_list[i]

                for i in range(0,len(self.storage_node_status_storage_file)):
                    if((self.storage_node_status_storage_file[i].find(p))!=-1):
                        self.storage_node_drives_file[i] = l
                        self.storage_node_storage_file[i] = m
                        self.storage_node_status_storage_file[i] = n
                        print "the loop to write number of disks is broken"
                        break
                    elif(i == (len(self.storage_node_status_storage_file)-1)):
                        self.storage_node_drives_file.append(str(l))
                        self.storage_node_storage_file.append(str(m))
                        self.storage_node_status_storage_file.append(str(n))
            else:
                print "It is not storage node"
            print self.storage_node_status_storage_file
        return self.storage_node_drives_file, self.storage_node_storage_file, \
               self.storage_node_status_storage_file
