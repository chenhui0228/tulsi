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

# Class to write the strings to logfile.txt

import os
import time
from Metric import Metric
from MachineLearning import MachineLearning


class Log(object):

    def __init__(self):
        print "the log class"
        self.metric = Metric()
        self.mach_learn = MachineLearning()
        self.storage_nodes = []
        self.normal_value_count = []
        self.metrics = []
        self.anomaly_value_count = []
        self.thresholds_values = []
        self.thresholds_lines = []
        self.no_of_lines = 200

    def write_data_to_file(self, file_name, line):
        file_name.write(line)
        file_name.write("\n")
        file_name.flush()

    def create_log_files(self, prefix):
        self.prefix = prefix
        if not os.path.exists("Metric\\" + self.prefix):
            os.makedirs("Metric\\"+self.prefix)
        return open(os.path.join("Metric\\"+self.prefix, "log.txt"), "a+")

    def check_file(self, file_name, prefix):
        self.prefix = prefix
        self.filename = file_name+".txt"
        filepath = os.path.join("Metric\\"+self.prefix, self.filename)
        if ((os.path.exists(filepath)) == False):
            open(os.path.join("Metric\\"+self.prefix, self.filename),"a")
        else:
            pass

    def setmessagelevel(self,
                        line_data,
                        local_time,
                        storage_nodes,
                        normal_value_count,
                        metrics, anomaly_value_count,
                        thresholds_values, thresholds_lines, fo, lo,
                        metric_name,
                        prefix,
                        ):
        self.metric_name = metric_name
        self.fo = fo
        self.log_files = lo
        self.anomaly_value_count = anomaly_value_count
        self.line_data = line_data
        self.local_time = local_time
        self.storage_nodes = storage_nodes
        self.normal_value_count = normal_value_count
        self.thresholds_values = thresholds_values
        self.thresholds_lines = thresholds_lines
        self.metrics = metrics
        self.prefix = prefix
        if self.line_data.find("errors.timing") > 0:
            str_data = self.local_time, 'E: ', self.line_data
            self.join_line = ''.join(str_data)
            self.metric.write_data_to_file(self.fo, self.join_line)
            self.metric.write_data_to_file(self.log_files, self.join_line)

        elif (((self.line_data.find("errors")) > 0) | ((self.line_data.find("quarantines")) > 0)):
                    str_data = self.local_time, 'C: ', self.line_data
                    self.join_line = ''.join(str_data)
                    self.metric.write_data_to_file(self.fo,  self.join_line)
                    self.metric.write_data_to_file(self.log_files,
                                                   self.join_line)

        elif self.line_data.find("timing") > 0:
            str_data = self.local_time, 'I: ', self.line_data
            self.join_line = ''.join(str_data)
            self.metric.parsing_line(self.join_line)

            if len(self.storage_nodes) == 0:
                self.storage_nodes.append(self.prefix)
                self.normal_value_count.append([0*x for x in range(
                    0, len(self.metrics))])
                self.anomaly_value_count.append([0*x for x in range(0, len(self.metrics))])
                self.thresholds_values.append([0 for x in range(0, len(self.metrics))])
                self.thresholds_lines.append([self.no_of_lines for x in range(0,len(self.metrics))])
                self.mach_learn.anomaly_detection(0, self.metrics, self.fo, self.log_files, self.metric_name, self.prefix, self.local_time, self.line_data, self.normal_value_count, self.thresholds_lines, self.thresholds_values) # calling function code to detect anomaly values
                self.storage_nodes_count = 1
            else:
                for i in range(0, len(self.storage_nodes)):
                    if self.prefix == self.storage_nodes[i]:
                        self.mach_learn.anomaly_detection(i, self.metrics, self.fo, self.log_files, self.metric_name, self.prefix, self.local_time,self.line_data, self.normal_value_count, self.thresholds_lines, self.thresholds_values) # calling function code to detect anomaly values
                        self.storage_nodes_count = 1

            if self.storage_nodes_count == 0:
                self.storage_nodes.append(self.prefix)
                self.normal_value_count.append([0*x for x in range(0,len(self.metrics))])
                self.anomaly_value_count.append([0*x for x in range(0,len(self.metrics))])
                self.thresholds_values.append([0 for x in range(0,len(self.metrics))])
                self.thresholds_lines.append([self.no_of_lines for x in range(0,len(self.metrics))])
                self.mach_learn.anomaly_detection(len(self.storage_nodes)-1, self.metrics, self.fo, self.log_files, self.metric_name, self.prefix, self.local_time,self.line_data, self.normal_value_count, self.thresholds_lines, self.thresholds_values) # calling function code to detect anomaly values
            self.storage_nodes_count = 0

        else:
            str_data = self.local_time, 'I: ', self.line_data
            self.join_line = ''.join(str_data)
            self.metric.write_data_to_file(self.fo,  self.join_line)
            self.metric.write_data_to_file(self.log_files, self.join_line)
        return self.storage_nodes, self.normal_value_count, self.anomaly_value_count, self.thresholds_values, self.thresholds_lines

    def create_new_file(self):
        self.timestr = time.strftime("%Y%m%d-%H%M%S")
        self.filename = "logfile.txt"
        if not os.path.exists("log"):
            os.makedirs("log")
        return open(os.path.join("log", self.filename), "a")