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


class ProxyNodeInfo(object):

    def __init__(self):
        self.proxy_node_list_temp_proxy_suffix = None
        self.proxy_node_list_proxy_suffix = []
        self.proxy_node_list = []
        self.proxy_node_status_file = []
        self.proxy_node_list_temp = None
        self.proxy_status = None

    def read_proxy_node_list(self, data):
        self.data = data
        print "Entering the proxy node list"
        if self.read_config_data_proxy_name(self.data) is not None:
            self.proxy_node_list_temp, self.proxy_status = \
                self.read_config_data_proxy_name(self.data)
            if len(self.proxy_node_list) == 0:
                self.proxy_node_list.append(self.proxy_node_list_temp)
                self.proxy_node_list_temp_proxy_suffix = "%s:p%s" % (
                    self.proxy_node_list_temp, str(len(self.proxy_node_list)))
                self.proxy_node_list_proxy_suffix.append(
                    self.proxy_node_list_temp_proxy_suffix)
                self.proxy_node_status_file_temp = "%s,%s" % (
                    str(self.proxy_node_list_temp_proxy_suffix),
                    str(self.proxy_status))
                self.proxy_node_status_file.append(
                    self.proxy_node_status_file_temp)
            elif self.proxy_node_list_temp is not None:
                    print "the proxy node list is not appended"
            else:
                for i in self.proxy_node_list:
                    if self.proxy_node_list_temp == i:
                        self.proxy_node_list_temp_proxy_suffix = "%s:p%s" % (
                            self.proxy_node_list_temp, str(len(i)+1))
                        self.proxy_node_list_proxy_suffix[len(i)] = \
                            self.proxy_node_list_temp_proxy_suffix
                        self.proxy_node_status_file_temp = "%s,%s" % (
                            str(self.proxy_node_list_temp_proxy_suffix),
                            str(self.proxy_status))
                        self.proxy_node_status_file[len(i)] =\
                            self.proxy_node_status_file_temp
                        break
                    elif(len(i) == len(self.proxy_node_list)-1):
                        self.proxy_node_list.append(self.proxy_node_list_temp)
                        self.proxy_node_list_temp_proxy_suffix = "%s:p%s" % (
                            self.proxy_node_list_temp,
                            (str(len(self.proxy_node_list))))
                        self.proxy_node_list_proxy_suffix.append(
                            self.proxy_node_list_temp_proxy_suffix)
                        self.proxy_node_status_file_temp = "%s,%s" % (
                            str(self.proxy_node_list_temp_proxy_suffix),
                            str(self.proxy_status))
                        self.proxy_node_status_file.append(
                            self.proxy_node_status_file_temp)
                        break
        return self.proxy_node_list, self.proxy_node_status_file

    def read_config_data_proxy_name(self, data):
        data = json.loads(data)
        if not set(data['host_ip']).isdisjoint(data['conf_ring_ip']):
            if (data['services'][0] == "openstack-swift-proxy:True"):
                return str(data['hostname']), str("g")
            else:
                return str(data['hostname']), str("w")

    def append_list(self):
        print "Appending the proxy node list"
