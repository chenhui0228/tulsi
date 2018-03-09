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

# Class to seperate different metrics and save them in file
import os


class Metric(object):

    def __init__(self):
        print "Metric class"

    def node_files(self, metric_value):
        self.metric_value = metric_value
        if not os.path.exists("Metric\\" +self.prefix ):
            os.makedirs("Metric\\"+self.prefix)
        nf = open(os.path.join("Metric\\"+self.prefix, self.metric_name+".txt"), "a+")
        nf.write(str(self.metric_value))
        nf.write("\n")
        nf.flush()
        nf.close()

    def write_data_to_file(self, file_name, line):
        file_name.write(line)
        file_name.write("\n")
        file_name.flush()

    def parsing_line_name(self, line):
        list2 = (line.split(":"))[3].split(" ")[1].split(".") # saving metric name
        self.prefix = list2[0]
        list2.pop(0)
        self.metric_name = " ".join(list2)
        return self.metric_name

    def parse_line_value(self,line):
        self.time_graph = (line.split(" "))[2].split(":")
        self.time_seconds = int(self.time_graph[0])*3600 + int(self.time_graph[1])*60+int(self.time_graph[2])
        # to get metric name and metric prefix
        list1 = (line.split(":"))[3].split(" ")[1].split(".")
        # saving metric name
        self.prefix = list1[0]
        list1.pop(0)
        self.metric_name = " ".join(list1)

        # to get metric values
        if self.metric_name.find('timing'):
            self.metric_value = float((line.split(":"))[4].split("|")[0])# saving metric value
            return self.metric_value
        else:
            self.metric_value = int((line.split(":"))[4].split("|")[0])
            return self.metric_value

    def parsing_line(self, line):
        self.time_graph = (line.split(" "))[2].split(":")
        self.time_seconds = int(self.time_graph[0])*3600 + int(self.time_graph[1])*60+int(self.time_graph[2])
        # to get metric name and metric prefix
        list1 = (line.split(":"))[3].split(" ")[1].split(".") # saving metric name
        self.prefix = list1[0]
        list1.pop(0)
        self.metric_name = " ".join(list1)
        # to get metric values
        if self.metric_name.find('timing'):
            self.metric_value = float((line.split(":"))[4].split("|")[0]) # saving metric value
        else:
            self.metric_value = int(float((line.split(":"))[4].split("|")[0]))
        return self.prefix, self.metric_value, self.metric_name
