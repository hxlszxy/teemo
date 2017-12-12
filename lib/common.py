# encoding: utf-8

import re
import socket
from config import *

import json
import subprocess

import requests as requests
import requests as __requests__
import colorama

# from tldextract import extract, TLDExtract

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

if allow_http_session:
    requests = requests.Session()

def is_domain(domain):
    domain_regex = re.compile(
        r'(?:[A-Z0-9_](?:[A-Z0-9-_]{0,247}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,}(?<!-))\Z', 
        re.IGNORECASE)
    return True if domain_regex.match(domain) else False

def proxy_verify(proxy):
    OK_proxy= {}
    if isinstance(proxy, dict) and len(proxy)!=0:
        for item in proxy.keys():
            ip = proxy.get(item).split("//")[-1].split(":")[0]
            port = proxy.get(item).split("//")[-1].split(":")[1]
            try:
                sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sk.settimeout(2)
                sk.connect((ip, int(port)))
                sk.close
                OK_proxy[item] = proxy.get(item)
            except:
                pass
    return OK_proxy

def http_request_get(url, body_content_workflow=False, allow_redirects=allow_redirects, custom_cookie="", proxies = None):
    try:
        if custom_cookie:
            headers['Cookie']=custom_cookie
        result = requests.get(url, 
            stream=body_content_workflow, 
            headers=headers, 
            timeout=timeout, 
            proxies=proxies,
            allow_redirects=allow_redirects,
            verify=allow_ssl_verify)
        return result
    except Exception, e:
        # return empty requests object
        return __requests__.models.Response()

def http_request_post(url, payload, body_content_workflow=False, allow_redirects=allow_redirects, custom_cookie="", proxies = None):
    """ payload = {'key1': 'value1', 'key2': 'value2'} """
    try:
        if custom_cookie:
            headers['Cookie']=custom_cookie
        result = requests.post(url, 
            data=payload, 
            headers=headers, 
            stream=body_content_workflow, 
            timeout=timeout, 
            proxies=proxies,
            allow_redirects=allow_redirects,
            verify=allow_ssl_verify)
        return result
    except Exception, e:
        # return empty requests object
        return __requests__.models.Response()

def curl_get_content(url):
    try:
        cmdline = 'curl "{url}"'.format(url=url)
        logging.info("subprocess call curl: {}".format(url))
        run_proc = subprocess.Popen(
            cmdline,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        (stdoutput,erroutput) = run_proc.communicate()
        response = {
            'resp': stdoutput.rstrip(),
            'err': erroutput.rstrip(),
        }
        return response
    except Exception as e:
        pass

def save_result(filename, args):
    try:
        fd = open(filename, 'w')
        json.dump(args, fd, indent=4)
    finally:
        fd.close()

def read_json(filename):
    if FileUtils.exists(filename):
        try:
            fd = open(filename, 'r')
            args = json.load(fd)
            return args
        finally:
            fd.close()
    else:
        return []

def banner():
    colorama.init()
    G = colorama.Fore.GREEN  # green
    Y = colorama.Fore.YELLOW  # yellow
    B = colorama.Fore.BLUE  # blue
    R = colorama.Fore.RED  # red
    W = colorama.Fore.WHITE  # white
    version = 'V 0.5'
    waring = "[!] legal disclaimer: Usage of Teemo for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program\n"

    print """%s

          #####  ######  ######  #    #   ####
            #    #       #       ##  ##  #    #
            #    #####   #####   # ## #  #    #
            #    #       #       #    #  #    #
            #    #       #       #    #  #    #
            #    ######  ######  #    #   ####

            %s%s

         # Coded By bit4 - https://github.com/bit4woo
         # %s
         
%s
  """ % (G, W, Y, version, waring) #must inport colorama to ensure G、W、Y works fine

def strip_list(inputlist):
    if isinstance(inputlist,list):
        resultlist =[]
        for x in inputlist:
            x = x.strip()
            resultlist.append(x)
        return resultlist
    else:
        print "The input should be a list"