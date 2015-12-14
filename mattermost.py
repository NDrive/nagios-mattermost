#!/usr/bin/python

# Copyright (c) 2015 NDrive SA
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import argparse
import urllib2
import json

CONFIG = {
    "icon_url": "https://slack.global.ssl.fastly.net/7bf4/img/services/nagios_128.png", #noqa
    "username": "Nagios"
}

TEMPLATE_SERVICE = "__{notificationtype}__ {hostalias}/{servicedesc} is {servicestate}\n{serviceoutput}" #noqa
TEMPLATE_HOST = "__{notificationtype}__ {hostalias} is {hoststate}\n{hostoutput}"  #noqa


def parse():
    parser = argparse.ArgumentParser(description='Send mattermost webhooks')
    parser.add_argument('--url', help='Integration URL', required=True)
    parser.add_argument('--hostalias', help='Host Alias', required=True)
    parser.add_argument('--notificationtype', help='Notification type',
                        required=True)
    parser.add_argument('--hoststate', help='Host State')
    parser.add_argument('--hostoutput', help='Host Output')
    parser.add_argument('--servicedesc', help='Service Description')
    parser.add_argument('--servicestate', help='Service State')
    parser.add_argument('--serviceoutput', help='Service Output')
    args = parser.parse_args()
    return args


def encode_special_characters(text):
    text = text.replace("%", "%25")
    return text


def make_data(args, config):
    template = TEMPLATE_SERVICE if args.servicestate else TEMPLATE_HOST
    text = template.format(**vars(args))

    payload = {
        "username": config["username"],
        "icon_url": config["icon_url"],
        "text": encode_special_characters(text)
    }

    data = "payload=" + json.dumps(payload)
    return data


def request(url, data):
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    return response.read()

if __name__ == "__main__":
    args = parse()
    data = make_data(args, CONFIG)
    response = request(args.url, data)
    print response
