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
import ConfigParser
from socket import *
import time
from datetime import datetime
from Log import Log
from Metric import Metric
import os

CUR_PATH = os.path.abspath(__file__)
CUR_DIR = os.path.dirname(CUR_PATH)

class TulsiStatsdClient(object):

    def __init__(self):
        # Reading the configuration file of HMS
        self.metrics = ["account-auditor failures",
                        "account-auditor timing",
                        "account-reaper timing",
                        "account-reaper container_failures",
                        "account-reaper object-failures",
                        "account-server GET timing",
                        "account-server HEAD timing",
                        "account-server PUT timing",
                        "account-server POST timing",
                        "account-server DELETE timing",
                        "account-server REPLICATE timing",
                        "account-replicator failures",
                        "account-replicator timing ",
                        "container-auditor failures",
                        "container-auditor timing",
                        "container-replicator failures",
                        "container-replicator timing",
                        "container-server GET timing",
                        "container-server HEAD timing",
                        "container-server PUT timing",
                        "container-server POST timing",
                        "container-server DELETE timing",
                        "container-server REPLICATE timing",
                        "container-sync deletes timing",
                        "container-sync puts timing",
                        "container-updater failures",
                        "container-updater timing",
                        "object-auditor timing",
                        "object-expirer timing",
                        "object-replicator partition delete timing",
                        "object-replicator partition update timing",
                        "object-server GET timing",
                        "object-server HEAD timing",
                        "object-server PUT timing",
                        "object-server POST timing",
                        "object-server DELETE timing",
                        "object-server REPLICATE timing",
                        "object-updater timing"]

        self.thresholds_lines = []
        self.thresholds_values = []
        self.local_time = time.time()
        self.line_data = ""
        self.no_of_lines = 200
        self.warning_dynamic_metric_name = []
        self.warning_dynamic_thresholds_values = []
        self.warning_dynamic_thresholds_lines = []
        self.threshold_count = 0
        self.metric_name = ""
        self.prefix = " "
        self.metric_value = 0.0
        self.normal_value_count = []
        self.anomaly_value_count = []
        self.storage_nodes = []
        self.storage_nodes_count = 0
        self.now1 = datetime.now()
        self.join_line = ""

        # Creating objects for Log.py, MachineLearning.py and Metric.py
        log = Log()
        metric = Metric()

        # Reading the file
        log.create_new_file()
        self.fo = open(os.path.join("log", "logfile.txt"), "a+")

        # Read the configuration file
        self.conf = ConfigParser.ConfigParser()
        #self.conf.read(os.path.join(CUR_DIR, 'tulsiclient.conf'))
        self.conf.read(os.path.join('/etc/tulsi', 'tulsi.conf'))
        try:
            print "Reading conf parameters "
            self.host = self.conf.get('tulsistatsd', 'host')
            log_duration = self.conf.get('tulsistatsd' , 'log_duration')
            self.port = int( self.conf.get('tulsistatsd', 'port'))
            self.log_duration = log_duration
        except:
            print "Conf not able to read"
            self.host = gethostbyname(gethostname())
            self.log_duration = 9
            self.port = 8125
        self.buf = 105600
        self.addr = (self.host, self.port)
        self.UDPSock = socket(AF_INET, SOCK_DGRAM)
        self.UDPSock.bind((self.host,self.port))
        self.now = int(time.time())

        # Starting the Infinite while loop
        while True:
            data = self.recv_msg()
            self.line_data = str(data)
            self.later = int(time.time())
            if(self.fo.tell()) > 524288000:
                self.fo.close()
                self.fo = log.create_new_file()
                self.now = int(time.time())
            else:
                self.fo.close()
                self.fo = open(os.path.join("log", "logfile.txt"), "a+")

                # Condition to check the number of lines for logfiles
                # If they exceed beyond 10000 a new file will be created
                # backing up the exisiting file with timestamp

                if len(list(self.fo)) > 10000:
                    timestr = time.strftime("%Y_%m_%d-%H_%M_%S")
                    filename = "logfile_"+timestr+".txt"
                    self.fo.close()
                    os.rename(os.path.join("log", "logfile.txt"),
                              os.path.join("log", filename))
                    self.fo = log.create_new_file()
                else:
                    self.fo = log.create_new_file()
                self.local_time = time.strftime("%d %a %H:%M:%S - ",
                                                time.localtime(time.time()))
                self.test_time = datetime.now().strftime("%H:%M:%S.%f")
                str_data = self.local_time, 'I: ', self.line_data
                self.join_line = ''.join(str_data)
                (self.prefix, self.metric_value,
                 self.metric_name) = metric.parsing_line(
                    self.join_line)
                print self.storage_nodes
                metric.node_files(self.metric_value)
                self.log_files = log.create_log_files(self.prefix)
                (self.storage_nodes,
                 self.normal_value_count,
                 self.anomaly_value_count,
                 self.thresholds_values,
                 self.thresholds_lines) = log.setmessagelevel(
                    self.line_data,
                    self.local_time,
                    self.storage_nodes,
                    self.normal_value_count,
                    self.metrics,
                    self.anomaly_value_count,
                    self.thresholds_values,
                    self.thresholds_lines,
                    self.fo,
                    self.log_files,
                    self.metric_name,
                    self.prefix)
                #print self.storage_nodes
    def recv_msg(self):
        data = self.UDPSock.recv(self.buf)
        return data
