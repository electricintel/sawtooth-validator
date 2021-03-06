# Copyright 2016 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------

import logging

from twisted.web.error import Error
from twisted.web import http

from txnserver.web_pages.base_page import BasePage

from txnintegration.utils import PlatformStats

LOGGER = logging.getLogger(__name__)


class StatisticsPage(BasePage):
    def __init__(self, validator):
        BasePage.__init__(self, validator)
        self.ps = PlatformStats()

    def render_get(self, request, components, args):
        if not components:
            raise Error(http.BAD_REQUEST, 'missing stat family')
        source = components.pop(0)

        result = {}
        if source == 'ledger':
            for domain in self.Ledger.StatDomains.iterkeys():
                result[domain] = self.Ledger.StatDomains[domain].get_stats()
            return result
        if source == 'node':
            for peer in self.Ledger.NodeMap.itervalues():
                result[peer.Name] = peer.Stats.get_stats()
                result[peer.Name]['IsPeer'] = peer.is_peer
            return result
        if source == 'platform':
            result['platform'] = self.ps.get_data_as_dict()
            return result
        if source == 'all':
            for domain in self.Ledger.StatDomains.iterkeys():
                result[domain] = self.Ledger.StatDomains[domain].get_stats()
            for peer in self.Ledger.NodeMap.itervalues():
                result[peer.Name] = peer.Stats.get_stats()
                result[peer.Name]['IsPeer'] = peer.is_peer
            result['platform'] = self.ps.get_data_as_dict()
            return result

        if 'ledger' in args:
            for domain in self.Ledger.StatDomains.iterkeys():
                result[domain] = self.Ledger.StatDomains[domain].get_stats()
        if 'node' in args:
            for peer in self.Ledger.NodeMap.itervalues():
                result[peer.Name] = peer.Stats.get_stats()
                result[peer.Name]['IsPeer'] = peer.is_peer
        if 'platform' in args:
            result['platform'] = self.ps.get_data_as_dict()

        elif ('ledger' not in args) & ('node' not in args) \
                & ('platform' not in args):
            raise Error(http.NOT_FOUND, 'not valid source or arg')

        return result
