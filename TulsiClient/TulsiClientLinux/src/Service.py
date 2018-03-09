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

class Service(object):

    def     __init__(self):
        self.ALL_NODE = ["openstack-swift-proxy:True", "openstack-swift-object:True",
                         "openstack-swift-object-replicator:True",
                         "openstack-swift-object-updater:True",
                         "openstack-swift-object-auditor:True",
                         "openstack-swift-container:True",
                         "openstack-swift-container-replicator:True",
                         "openstack-swift-container-updater:True",
                         "openstack-swift-container-auditor:True",
                         "openstack-swift-account:True",
                         "openstack-swift-account-replicator:True",
                         "openstack-swift-account-reaper:True",
                         "openstack-swift-account-auditor:True"]

        self.STORAGE_NODE = ["openstack-swift-proxy:False", "openstack-swift-object:True",
                             "openstack-swift-object-replicator:True",
                             "openstack-swift-object-updater:True",
                             "openstack-swift-object-auditor:True",
                             "openstack-swift-container:True",
                             "openstack-swift-container-replicator:True",
                             "openstack-swift-container-updater:True",
                             "openstack-swift-container-auditor:True",
                             "openstack-swift-account:True",
                             "openstack-swift-account-replicator:True",
                             "openstack-swift-account-reaper:True",
                             "openstack-swift-account-auditor:True"]

        self.PROXY_NODE = ["openstack-swift-proxy:True", "openstack-swift-object:False",
                           "openstack-swift-object-replicator:False",
                           "openstack-swift-object-updater:False",
                           "openstack-swift-object-auditor:False",
                           "openstack-swift-container:False",
                           "openstack-swift-container-replicator:False",
                           "openstack-swift-container-updater:False",
                           "openstack-swift-container-auditor:False",
                           "openstack-swift-account:False",
                           "openstack-swift-account-replicator:False",
                           "openstack-swift-account-reaper:False",
                           "openstack-swift-account-auditor:False"]
