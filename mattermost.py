#!/usr/bin/env python

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
import json
import urllib2

VERSION = "0.3.1"


def parse():
    parser = argparse.ArgumentParser(description='Sends alerts to Mattermost')
    parser.add_argument('--url', help='Incoming Webhook URL', required=True)
    parser.add_argument('--channel', help='Channel to notify')
    parser.add_argument('--username', help='Username to notify as',
                        default='Nagios')
    parser.add_argument('--iconurl', help='URL of icon to use for username',
                        default='https://slack.global.ssl.fastly.net/7bf4/img/services/nagios_128.png') # noqa
    parser.add_argument('--notificationtype', help='Notification Type',
                        required=True)
    parser.add_argument('--hostalias', help='Host Alias', required=True)
    parser.add_argument('--hostaddress', help='Host Address', required=True)
    parser.add_argument('--hoststate', help='Host State')
    parser.add_argument('--hostoutput', help='Host Output')
    parser.add_argument('--servicedesc', help='Service Description')
    parser.add_argument('--servicestate', help='Service State')
    parser.add_argument('--serviceoutput', help='Service Output')
    parser.add_argument('--cgiurl', help='Link to extinfo.cgi on your Nagios instance')
    parser.add_argument('--version', action='version',
                        version='% (prog)s {version}'.format(version=VERSION))
    args = parser.parse_args()
    return args


def encode_special_characters(text):
    text = text.replace("%", "%25")
    text = text.replace("&", "%26")
    return text


def emoji(notificationtype):
    return {
        "RECOVERY": ":white_check_mark:",
        "PROBLEM": ":fire:",
        "DOWNTIMESTART": ":clock10:",
        "DOWNTIMEEND": ":sunny:"
    }.get(notificationtype, "")


def text(args):
    template_host = "__{notificationtype}__ {hostalias} is {hoststate}\n{hostoutput}" # noqa
    template_service = "__{notificationtype}__ {hostalias} at {hostaddress}/{servicedesc} is {servicestate}\n{serviceoutput}" # noqa
    if args.servicestate is not None:
        template_cgiurl = " [View :link:]({cgiurl}?type=2&host={hostalias}&service={servicedesc})"
    template = template_service if args.servicestate else template_host

    text = emoji(args.notificationtype) + template.format(**vars(args))
    if args.servicestate and args.cgiurl is not None:
        # If we know the CGI url, and this is a service notification,
        # provide a clickable link to the nagios CGI
        text = text + template_cgiurl.format(**vars(args))

    return encode_special_characters(text)


def payload(args):
    payload = {
        "username": args.username,
        "icon_url": args.iconurl,
        "text": text(args)
    }

    if args.channel:
        payload["channel"] = args.channel

    data = "payload=" + json.dumps(payload)
    return data


def request(url, data):
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    return response.read()


if __name__ == "__main__":
    args = parse()
    response = request(args.url, payload(args))
    print response
