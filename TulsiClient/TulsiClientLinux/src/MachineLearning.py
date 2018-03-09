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
# Class to implement functions of Anamoly detection and its dependent
from numpy import genfromtxt
import numpy as np
import math
import scipy.stats
import os


class MachineLearning(object):

    def __init__(self):
        print "Machine learning class"
        self.metrics = []
        self.no_of_lines = 200

    def write_data_to_file(self, file_name, line):
        file_name.write(line)
        file_name.write("\n")
        file_name.flush()

    def check_file(self, file_name, prefix):
        self.prefix = prefix
        self.filename = file_name+".txt"
        filepath = os.path.join("Metric\\"+self.prefix, self.filename)
        if ((os.path.exists(filepath)) == False):
            open(os.path.join("Metric\\"+self.prefix, self.filename),"a")
        else:
            pass

    def measure_number_lines(self, filename):
        self.file_name = filename+".txt"
        filepath = os.path.join("Metric\\" + self.prefix, self.file_name)
        fopen = open(filepath)
        l = [x for x in fopen.readlines() if x != "\n"]
        return len(l)

    def anomaly_detection(self,
                          s_i,
                          metrics,
                          fo,
                          log_files,
                          metric_name,
                          prefix,
                          local_time,
                          line_data,
                          normal_value_count,
                          thresholds_lines, thresholds_values):

        self.log_files = log_files
        self.fo = fo
        self.metrics = metrics
        self.check_loop_entry = False
        self.metric_name = metric_name
        self.prefix = prefix
        self.local_time = local_time
        self.line_data = line_data
        self.normal_value_count = normal_value_count
        self.thresholds_lines = thresholds_lines
        self.thresholds_values = thresholds_values

        for j in range(0, len(self.metrics)):
            if(self.metric_name == self.metrics[j]):
                self.check_loop_entry = True
                metric_check = self.metric_name
                self.check_file(metric_check, self.prefix)
                number_lines = self.measure_number_lines(metric_check)
                # print number_linesr
                if number_lines < self.no_of_lines:
                    # print "Printing in section number of lines Less than 10"
                    #str_data = self.local_time, 'I: ', self.line_data
                    #self.join_line = ''.join(str_data)
                    #self.write_data_to_file(self.fo,  self.join_line)
                    str_data = self.local_time, 'I: ', self.line_data
                    self.join_line = ''.join(str_data)
                    self.write_data_to_file(self.log_files, self.join_line)
                    self.normal_value_count[s_i][j] +=1  # incrementing normal value counter

                    break
                elif number_lines >= self.thresholds_lines[s_i][j]:
                    self.thresholds_lines[s_i][j] = number_lines + self.no_of_lines
                    filepath = os.path.join("Metric\\"+self.prefix,
                                            self.metric_name+".txt")
                    X = self.readvalues(filepath,'/n')
                    mean1 = self.cali_mean(X)
                    std_1 = self.cali_std(X)
                    Z = len(X)
                    # print Z
                    M = X
                    L = []
                    for i in range(Z):
                        K = self.standard_norm_distribution(X[i], mean1, std_1)
                        if(K<=0.6):
                            L = np.append(L, M[i])
                            continue
                        else:
                            continue
                        U = len(L)
                        M = L
                        mean2 = self.cali_mean(L)
                        std_2= self.cali_std(L)
                        K1 = self.standard_norm_distribution(self.metric_value, mean2, std_2)
                        z_value = 1.644853
                        KB = []
                        #Detecting threshold
                        ######### loop for remove metric values which were not covered in 95% area
                        for i in range(U):
                            K1=self.standard_norm_distribution(L[i], mean2, std_2)
                                    #print "probability of value", K1
                            if (K1 <= 0.95):
                                KB = np.append(KB, M[i])

                                mean3 = self.cali_mean(KB)

                                self.thresholds_values[s_i][j] = mean3 + ((np.amax(KB)-np.amin(KB))/(1.5))

                                if(self.metric_value <= self.thresholds_values[s_i][j]):

                                    self.normal_value_count[s_i][j] +=1  # incrementing normal value counter

                                    str_data = self.local_time, 'I: ', self.line_data
                                    self.join_line = ''.join(str_data)
                                    self.write_data_to_file(self.fo,  self.join_line)
                                    self.write_data_to_file(self.log_files, self.join_line)

                                    break

                                else:
                                    # print M
                                    self.anomaly_value_count [s_i][j]+=1  # incrementing anomaly value count
                                    str_data = self.local_time, 'W: ', self.line_data
                                    self.join_line = ''.join(str_data)
                                    self.write_data_to_file(self.fo,  self.join_line)
                                    self.write_data_to_file(self.log_files, self.join_line)
                                    break
                            elif number_lines < self.thresholds_lines[s_i][j]:
                                if(self.metric_value <= self.thresholds_values[s_i][j]):
                                    self.normal_value_count[s_i][j] +=1  # incrementing normal value counter
                                    str_data = self.local_time, 'I: ', self.line_data
                                    self.join_line = ''.join(str_data)
                                    self.write_data_to_file(self.fo,  self.join_line)
                                    self.write_data_to_file(self.log_files, self.join_line)
                                    break

                                else:
                                    if self.normal_value_count [s_i][j] > 0:
                                        self.anomaly_value_count[s_i][j] +=1  # incrementing anomaly value count
                                        false_positive = round((float)(self.anomaly_value_count[s_i][j])/(self.normal_value_count[s_i][j] + self.anomaly_value_count[s_i][j]) *100, 2)
                                        false_negative = round((float)(self.normal_value_count[s_i][j])/(self.normal_value_count[s_i][j] + self.anomaly_value_count[s_i][j]) *100, 2)
                                        self.create_sheet(self.normal_value_count[s_i][j], self.anomaly_value_count[s_i][j], str(false_positive),str(false_negative))
                                    str_data = self.local_time, 'W: ', self.line_data
                                    self.join_line = ''.join(str_data)
                                    self.write_data_to_file(self.fo,  self.join_line)
                                    self.write_data_to_file(self.log_files, self.join_line)
                                    break
                        else:
                            continue

                    # Dynamic metric name values loo[
                    if(self.check_loop_entry == False):

                        if len(self.warning_dynamic_metric_name)==0:
                                # print "The area is supposed to be appended"

                                self.warning_dynamic_metric_name.append(self.prefix +" "+self.metric_name)

                                str_data = self.local_time, 'W: ', self.line_data
                                self.join_line = ''.join(str_data)
                                self.write_data_to_file(self.fo,  self.join_line)
                                str_data = self.local_time, 'W: ', self.line_data
                                self.join_line = ''.join(str_data)
                                self.write_data_to_file(self.log_files, self.join_line)

                                self.warning_dynamic_thresholds_lines.append(self.no_of_lines)
                                self.warning_dynamic_thresholds_values.append(0)
                        else:
                                # print "Else loop of null matrix"
                                pass

                        self.status = False
                        for k in range(0,len(self.warning_dynamic_metric_name)):

                            self.my_metric_name =self.prefix +" "+self.metric_name
                            self.string_metric_split = self.my_metric_name.split(" ")
                            self.string_split= self.warning_dynamic_metric_name[k].split(" ")

                            if(self.status == True):
                                break

                            if( self.my_metric_name== self.warning_dynamic_metric_name[k]):
                                metric_check = self.metric_name
                                self.check_file(metric_check)
                                number_lines = self.measure_number_lines(metric_check)
                                self.status = True

                                if number_lines  < self.no_of_lines :
                                    #print "Printing in section number of lines Less than 10"
                                    str_data = self.local_time, 'I: ', self.line_data
                                    self.join_line = ''.join(str_data)

                                    self.write_data_to_file(self.fo,  self.join_line)
                                    str_data = self.local_time, 'I: ', self.line_data
                                    self.join_line = ''.join(str_data)
                                    self.write_data_to_file(self.log_files, self.join_line)
                                    self.normal_value_count[s_i][j] +=1  # incrementing normal value counter


                                    break


                                elif number_lines >= self.warning_dynamic_thresholds_lines[k]:
                                    self.warning_dynamic_thresholds_lines[k]=number_lines + self.no_of_lines
                                    filepath = os.path.join("Metric\\"+self.prefix, self.metric_name+".txt")

                                    X= self.readvalues(filepath, '/n')
                                    mean1 = self.cali_mean(X)
                                    std_1 = self.cali_std(X)

                                    Z=len(X)

                                    M=X
                                    L = []

                                    for i in range(Z):

                                        K=self.standard_norm_distribution(X[i], mean1, std_1)
                                        if(K<=0.6):
                                            L = np.append(L, M[i])

                                            continue
                                        else:

                                            continue

                                    U = len(L)
                                    #print U
                                    mean2=self.cali_mean(L)
                                    std_2= self.cali_std(L)

                                    K1=self.standard_norm_distribution(self.metric_value, mean2, std_2)
                                    z_value = 2.326348
                                    #Detecting threshold
                                    self.warning_dynamic_thresholds_values[k]=self.measure_threshold(mean2, std_2, z_value)
                                    #print"Threshold", self.thresholds_values[j]
                                    if(self.metric_value<=self.warning_dynamic_thresholds_values[k]):

                                        self.normal_value_count[s_i][j] +=1  # incrementing normal value counter

                                        str_data = self.local_time, 'I: ', self.line_data
                                        self.join_line = ''.join(str_data)
                                        self.write_data_to_file(self.fo,  self.join_line)
                                        self.write_data_to_file(self.log_files, self.join_line)

                                        break


                                    else:
                                        #print M
                                        self.anomaly_value_count [s_i][j]+=1  # incrementing anomaly value count
                                        str_data = self.local_time, 'W: ', self.line_data
                                        self.join_line = ''.join(str_data)
                                        self.write_data_to_file(self.fo,  self.join_line)
                                        self.write_data_to_file(self.log_files, self.join_line)

                                        break

                                    break

                                elif number_lines < self.warning_dynamic_thresholds_values[k]:
                                    if(self.metric_value <= self.warning_dynamic_thresholds_values[k]):
                                        self.normal_value_count[s_i][j] +=1  # incrementing normal value counter

                                        str_data = self.local_time, 'I: ', self.line_data
                                        self.join_line = ''.join(str_data)
                                        self.write_data_to_file(self.fo,  self.join_line)
                                        self.write_data_to_file(self.log_files, self.join_line)


                                        break

                                    else:
                                        if self.normal_value_count [s_i][j] > 0:
                                            self.anomaly_value_count[s_i][j] +=1  # incrementing anomaly value count

                                            false_positive = round((float)(self.anomaly_value_count[s_i][j])/(self.normal_value_count[s_i][j] + self.anomaly_value_count[s_i][j]) *100, 2)
                                            false_negative = round((float)(self.normal_value_count[s_i][j])/(self.normal_value_count[s_i][j] + self.anomaly_value_count[s_i][j]) *100, 2)

                                            self.create_sheet(self.normal_value_count[s_i][j], self.anomaly_value_count[s_i][j], str(false_positive),str(false_negative))
                                        str_data = self.local_time, 'W: ', self.line_data
                                        self.join_line = ''.join(str_data)
                                        self.write_data_to_file(self.fo,  self.join_line)
                                        self.write_data_to_file(self.log_files, self.join_line)
                                        break
                                    break
                                    #print "anomaly count", self.anomaly_value_count[s_i][j]

                            elif  k ==len(self.warning_dynamic_metric_name)-1:
                                #print "The area is supposed to be appended"
                                self.warning_dynamic_metric_name.append(self.prefix +" "+self.metric_name)

                                str_data = self.local_time, 'I: ', self.line_data
                                self.join_line = ''.join(str_data)

                                self.write_data_to_file(self.fo,  self.join_line)
                                self.write_data_to_file(self.log_files, self.join_line)
                                self.warning_dynamic_thresholds_lines.append(self.no_of_lines)
                                self.warning_dynamic_thresholds_values.append(0)

                                break

    def measure_threshold(self,mean,std_dev,z_value):
        thesh_value = ((z_value*std_dev)+mean)
        return thesh_value

    def readvalues(self, filename, My_sign):
        my_data = genfromtxt(filename,delimiter = My_sign)
        return my_data

    def cali_mean(self, Mean_data):
        z = np.mean(Mean_data)
        return z

    def cali_std(self, Std_data):
        k = np.std(Std_data)
        return k

    def cali_range(self, Std_data):
        r = np.ptp(Std_data)
        return r

    def cali_gauss(self,X,mean,std_dev):
        prob1 = (1/math.sqrt(2*math.pi*(math.pow(std_dev,2))))
        prob2 = -((math.pow((X-mean),2)))/(2*math.pow(std_dev,2))
        prob_final = prob1*math.exp(prob2)
        print prob_final

    def normpdf(self, X, mean, std_dev):
        var = float(std_dev)**2
        pi = 3.1415926
        denom = (2*pi*var)**.5
        num = math.exp(-(float(X)-float(mean))**2/(2*var))
        return num/denom

    def standard_norm_distribution(self,X,mean,std_dev):
        Z = ((X-mean)/std_dev)
        Pr = scipy.stats.norm.cdf(Z)
        return Pr

    def standard_norm_distribution_range(self,X,mean,range):
        Z = ((X-mean)/range)
        Pr = scipy.stats.norm.cdf(Z)
        return Pr
