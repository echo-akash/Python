import sys
import os
import nmap
import socket
import getopt, sys
import platform
import urllib, urllib2, json
import ftplib
import time
import utils
import re
import argparse

try:
    from bs4 import BeautifulSoup
except Exception as e:
    print("pip install beautifulsoup4")
    exit(1)
    
try:
    import requests
except:
    print "Request library not found, please install it before proceeding\n"
    sys.exit()

#datetime
from datetime import datetime

from pywebfuzz import fuzzdb

#for request password
import getpass

from Log import Log
from NexposeFrameWork import NexposeFrameWork
from MetaSploitFrameWork import MetaSploitFrameWork
from UtilDNS import UtilDNS
from ShodanSearch import ShodanSearch
from SSHConnection import SSHConnection
from FTPConnection import FTPConnection
from Checker import Checker
from Scraping import Scraping
from InfoLocation import InfoLocation
from ScanningNMAP import ScanningNMAP
from HTTPScan import HTTPScan
from CheckOpenSslVulnerable import CheckOpenSslVulnerable
from CheckFTPVulnerable import CheckFTPVulnerable
from NmapScanner import NmapScanner
from ExtractMails import ExtractMails
from Search import Search
from CheckVuln_SQL_XSS_LFI import CheckVuln_SQL_XSS_LFI
from IdentifyServer import IdentifyServer
from CheckHeadersXSS import CheckHeadersXSS
from CheckCookies import CheckCookies

#from ScannerScapy import ScannerScapy

#nexpose
import pynexposeHttps
import builtwith



def showMenu():
    print "[0]-->EXIT"
    print "[1]-->Check Open Ports[80,8080 by default]"
    print "[2]-->Port Scanning[It will scan over ports parameter,by default it will scan 80 and 8080]"
    print "[3]-->Nmap Scanning Advanced"
    print "[4]-->Check Option methods"
    print "[5]-->Check DNS Servers info"
    print "[6]-->Check Host info from Shodan Service"
    print "[7]-->NMAP Port Scanning"
    print "[8]-->Host Info by Socket Call"
    print "[9]-->GeoLocation Host Info"
    print "[10]-->Scraping for images and pdf & obtain metadata"
    print "[11]-->Get Headers info"
    print "[12]-->Get SSH user/password Brute Force[Requires port 22 opened]"
    print "[13]-->Get FTP Anonymous access[Requires port 21 opened]"
    print "[14]-->MetaSploitFrameWork"
    print "[15]-->NexposeFramework"
    print "[16]-->HTTP SCAN[Requires port 80 opened]"
    print "[17]-->Check HeartBleed OpenSSL vulnerability[Requires port 443 opened]"
    print "[18]-->Check FTP Server Buffer Overflow Vulnerability[Requires port 21 opened]"
    print "[19]-->Check Vulnerabilities SQL,XSS,LFI in domain"
    print "[20]-->Check Domains and obtain metadata[mails, hosts, servers,urls]"
    print "[21]-->Check open ports with scapy"
    print "[22]-->Check website libraries"
    print "[23]-->Identify web server"
    print "[24]-->Check headers & Clickjacking"
    print "[25]-->Check Cookies from website"
    
    option = raw_input ("Choose an option:")
    return option
    
if __name__ == "__main__":

    print(author())
    
    parser = argparse.ArgumentParser(description='Pentesting-tool')
    
    # Main arguments
    parser.add_argument("-target", dest="target", help="target IP / domain", required=None)
    parser.add_argument("-ports", dest="ports", help="Please, specify the target port(s) separated by comma[80,8080 by default]", default = "80,8080")
    parser.add_argument("-proxy", dest="proxy", help="Proxy[IP:PORT]", required=None)

    parsed_args = parser.parse_args()    
    
    shodanSearch = ShodanSearch()
    dnsResolver = UtilDNS()
    sshConnection = SSHConnection()
    checker = Checker()
    scraping = Scraping()
    scanningNMAP = ScanningNMAP()
    infoLocation = InfoLocation()
    httpScan = HTTPScan()
    checkOpenSslVulnerable = CheckOpenSslVulnerable()
    checkFtpVulnerable = CheckFTPVulnerable()
    extractMails = ExtractMails()
    checkVuln_SQL_XSS_LFI = CheckVuln_SQL_XSS_LFI()
    #scannerScapy = ScannerScapy()
    
    #default port list

    ip = ""
    hostname = ""
    option = ""

    ip_server_metasploit = ""
    port_server_metasploit = ""
    user_metasploit = ""
    password_metasploit = ""
    shodan_results = []
    shodan_visited = []
    
    pyconnect = 0
    
    if parsed_args.target == None:
	while (hostname ==""):
	    hostname = raw_input ("[*] Introduce IP or name domain:")
    else:
	hostname = parsed_args.target
    
    print("\n [*] Obtain Ip address from host name")
    print "-----------------------------------"
    ip = socket.gethostbyname(hostname)
    print '[*] The IP address of ', hostname, 'is', ip
    
    
    while option != 0:
        
        print "\n [*] IP/Hostname: "+ ip + " / " + hostname
        
        option = showMenu()
        if option == "0":
            sys.exit(1);
        if option == "1":
            f = open('logOpenPorts.txt', 'a')
            sys.stdout = Log(sys.stdout, f)
	    portlist = parsed_args.ports.split(',')
            checker.checkOpenPorts(ip,hostname,portlist)
        if option == "2":
            f = open('logPortScanning.txt', 'a')
            sys.stdout = Log(sys.stdout, f)
	    print "[*] Scanning ports "+ parsed_args.ports + "..."
	    portlist = parsed_args.ports.split(',')
            for port in portlist: 
                NmapScanner().nmapScan(ip, port)
		
	    NmapScanner().nmapScanJSONGenerate(ip, parsed_args.ports)
	    
        if option == "3":
            f = open('logNmapScanningAdvanced.txt', 'a')
            sys.stdout = Log(sys.stdout, f)
            checker.checkNmapOptions(ip)          
        if option == "4":
            f = open('logOptionMethods.txt', 'a')
            sys.stdout = Log(sys.stdout, f)
            checker.checkOptionMethods(hostname)
        if option == "5":
            f = open('logDnsInfo.txt', 'a')
            sys.stdout = Log(sys.stdout, f)
            dnsResolver.checkDNSInfo(ip,hostname)
        if option == "6":
            f = open('logHostInfo.txt', 'a')
            sys.stdout = Log(sys.stdout, f)
            shodanSearch.obtain_host_info2(ip)
	    shodanSearch.obtain_host_info2(hostname)
        if option == "7":
            f = open('logNScanningNmap.txt', 'a')
            sys.stdout = Log(sys.stdout, f)
	    portlist = parsed_args.ports
            scanningNMAP.scanNMAP(ip,portlist)
            if platform.system() == "Linux":
                scanningNMAP.scanningNmapUnix(ip,hostname,portlist)
            if platform.system() == "Windows":
                scanningNMAP.scanningNmapWindows(ip,hostname,portlist)
        if option == "8":
            f = open('logHostByName.txt', 'a')
            sys.stdout = Log(sys.stdout, f)
            print socket.gethostbyname(hostname)
        if option == "9":
            f = open('logGeoLocationInfo.txt', 'a')
            sys.stdout = Log(sys.stdout, f)
	    infoLocation.printRecord(ip)
	    infoLocation.printRecord(hostname)	    
            infoLocation.geoInfo(hostname,ip)
        if option == "10":
            f = open('logScraping.txt', 'a')
            sys.stdout = Log(sys.stdout, f)
            print '\njpg images'
            print '--------------'
            scraping.getImgFromUrl(hostname, 'jpg')
            print '\npng images'
            print '--------------'
            scraping.getImgFromUrl(hostname, 'png')
            print '\ngif images'
            print '--------------'
            scraping.getImgFromUrl(hostname, 'gif')
            
            scraping.scrapingImagesPdf(hostname)
            scraping.scrapingImagesPdf(ip)
            scraping.scrapingBeautifulSoup(hostname)
            scraping.scrapingBeautifulSoup(ip)
            
        if option == "11":
            f = open('logCheckHeaders.txt', 'a')
            sys.stdout = Log(sys.stdout, f)
            checker.checkHeadersInfoByIp(ip)
            checker.checkHeadersInfoByHostName(hostname)
        if option == "12":
            f = open('logSSHBruteForce.txt', 'a')
            sys.stdout = Log(sys.stdout, f)
            sshConnection.SSHBruteForce(hostname)
        if option == "13":
            f = open('logFTP.txt', 'a')
            sys.stdout = Log(sys.stdout, f)
            ftpConnection = FTPConnection(hostname)
            ftpConnection.ftpConnectionAnonymous()
        if option == "14":

            while (ip_server_metasploit == ""):
                ip_server_metasploit = raw_input ("[*] Introduce IP server where MetaSploit is running:")
            while (port_server_metasploit == ""):
                port_server_metasploit = raw_input ("[*] Introduce Port server where MetaSploit is running:")
            while (user_metasploit == ""):
                user_metasploit = raw_input ("[*] Introduce user for MetaSploit:")
            while (password_metasploit == ""):
                password_metasploit = getpass.getpass ("[*] Introduce password for MetaSploit:")
                
            try:
                f = open('metaSploit_log.txt', 'w')
                sys.stdout = Log(sys.stdout, f)
            
                metaSploitFrameWork = MetaSploitFrameWork(port_server_metasploit,ip_server_metasploit,ip,user_metasploit,password_metasploit)
                metaSploitFrameWork.scanMetaSploitFrameWork()
                
            except Exception,e:
                print "Error to connecting with MetaSploit Server"
                print e
                pass

        if option == "15":
            if pyconnect == 0:
                serveraddr_nexpose = ""
                port_server_nexpose = ""
                user_nexpose = ""
                password_nexpose = ""
                while (serveraddr_nexpose == ""):
                    serveraddr_nexpose = raw_input ("[*] Introduce IP server where Nexpose is running:")
                while (port_server_nexpose == ""):
                    port_server_nexpose = raw_input ("[*] Introduce Port server where Nexpose is running:")
                while (user_nexpose == ""):
                    user_nexpose = raw_input ("[*] Introduce user for Nexpose:")
                while (password_nexpose == ""):
                    password_nexpose = getpass.getpass ("[*] Introduce password for Nexpose:")
                

            try:
                if pyconnect == 0: 
                    pynexposeHttps = pynexposeHttps.NeXposeServer(serveraddr_nexpose, port_server_nexpose, user_nexpose, password_nexpose)
                    pyconnect = 1                
            except Exception,e:
                pyconnect = 0
		print e.message
                print "Error to connecting with NeXposeServer"
                
                pass
            
            try:
                f = open('nexpose_log.txt', 'w')
                sys.stdout = Log(sys.stdout, f)
                nexposeFrameWork = NexposeFrameWork(pynexposeHttps)
                nexposeFrameWork.siteListing()
                nexposeFrameWork.vulnerabilityListing()
                
                pynexposeHttps.logout()
                
            except Exception,e:
                print "Error to connecting with NeXposeServer for listing vulnerabilities"
                print e
                pass
        if option == "16":
            f = open('logHTTPScan.txt', 'a')
            sys.stdout = Log(sys.stdout, f)
            httpScan.startHTTPScanBruteForce(hostname,ip,parsed_args.proxy)
        if option == "17":
            f = open('logCheckHeartbleed.txt', 'a')
            sys.stdout = Log(sys.stdout, f)
            checkOpenSslVulnerable.startCheckVulnerability(ip,hostname)
        if option == "18":
            f = open('logCheckFTPvulnerable.txt', 'a')
            sys.stdout = Log(sys.stdout, f)
            checkFtpVulnerable.startCheckVulnerability(ip,hostname)
	if option == "19":
	    f = open('logCheckvuln_SQL_XSS_LFI.txt', 'a')
	    sys.stdout = Log(sys.stdout, f)
	    checkVuln_SQL_XSS_LFI.startCheckVulnerability(ip,hostname)
	if option == "21":
	    f = open('logCheckOpenPortsScapy.txt', 'a')
	    sys.stdout = Log(sys.stdout, f)
	    #scannerScapy.scan_ports_multithread(hostname,parsed_args.ports)
	if option == "22":
	    f = open('logCheckLibrariesWebsite.txt', 'a')
	    sys.stdout = Log(sys.stdout, f)
	    url = utils.verify_url(hostname)
	    print 'Obtaining libraries from website ' + url
	    print builtwith.parse(str(url))
	if option == "23":
	    f = open('logIdentifyWebServer.txt', 'a')
	    sys.stdout = Log(sys.stdout, f)
	    url = utils.verify_url(hostname)
	    print 'Identify Server from ' + url
	    identifyServer = IdentifyServer()
	    identifyServer.test(url)
	    identifyServer.test(hostname)
	    identifyServer.test(ip)   	    
	if option == "24":
	    f = open('logCheckHeadersXSS.txt', 'a')
	    sys.stdout = Log(sys.stdout, f)
	    url = utils.verify_url(hostname)
	    print 'Checking headers from ' + url
	    headersXSS = CheckHeadersXSS()
	    headersXSS.test(url)
	if option == "25":
	    f = open('logCheckCookies.txt', 'a')
	    sys.stdout = Log(sys.stdout, f)
	    url = utils.verify_url(hostname)
	    print 'Checking cookies from ' + url
	    checkCookies = CheckCookies()
	    checkCookies.test(url)
        if option == "20":
            try:
                f = open('logCheckDomains.txt', 'a')
                sys.stdout = Log(sys.stdout, f)
                html = utils.HtmlExtractor(hostname)
                #url always starts with http:// or https://
            
		print "[+] Searching urls, emails and domains......"
		
                url = html.get_url()
                print url
                data_extractor = utils.DataExtractor(html.get_body(), url, only_href = True)

		logins = fuzzdb.Discovery.PredictableRes.Logins
		httpMethods= fuzzdb.attack_payloads.http_protocol.http_protocol_methods
		
		
		data_extractor.get_predictable_urls(url,logins)
		data_extractor.get_http_methods(url,httpMethods)

                urls = data_extractor.get_urls()
                if len(urls)>0:
		    print "[+] URLS:"
                    for url in urls:
                        print url
                        extractMails.obtain_mails(url)
                    else:
			print "[-] No URL found"
                
                domains = data_extractor.get_domains(urls)
                if len(domains)>0:
		    print "[+] Domains:"
                    for domain in domains:
                        print domain
                        extractMails.obtain_mails(domain)
                    else:
			print "[-] No Domains found"
                
                ips = data_extractor.get_ips_for_domains(domains)
                for key in ips.iterkeys():
                    print key, ": ", " ".join(ips[key])
            
		extractMails.obtain_mails(hostname)
                    
            except Exception,e:
                pass
	    
	    host=''
	    
	    if hostname.startswith("www") == True:
		parts = hostname.split(".")
		for part in parts:
		    if part !='www':
			host+=part+'.'
		host = host[:-1]
	    else:
		host = hostname
		
	    search = Search(host)
	    search.process()
	    emails = search.get_emails()
	    hosts = search.get_hostnames()
	    full = []
	    
	    print "\n\n[+] Emails:"
	    print "------------------"
	    if emails == []:
		print "No emails found"
	    else:
		for email in emails:
		    print email
	    
	    print "\n[+] Hosts:"
	    print "------------------------------------"
	    if hosts == []:
		print "No hosts found"
	    else:
		print "[+] Resolving hostnames and IPs... "
		host = utils.Checker(hosts)
		full = host.check()
		for host in full:
		    print host
		    
	    print "\n[+] Shodan Database search:"
	    print "------------------------------------"
	    for host in full:
		try:
		    ip = host.split(":")[0]
		    if not shodan_visited.count(ip):
			print "\tSearching Shodan info for: " + host
			shodan_visited.append(ip)
			results = shodanSearch.execute(ip)
			for res in results:
			    #print str(res['_shodan'])
			    shodan_results.append(host + "SHODAN" + str(res['_shodan']) + "SHODAN" + str(res['port']))
		except Exception,e:
		    continue
	    
	    #print shodan_results		
	    print "\n[+] Shodan results:"
	    print "------------------------------------"
	    for result in shodan_results:
		print result.split("SHODAN")[0] + ":" + result.split("SHODAN")[1]+ ":" + result.split("SHODAN")[2] 

	    response = requests.get('http://sameip.org/'+ip)
	    bs = BeautifulSoup(response.text, 'lxml')
	    for site in bs.find_all(attrs={'class': 's-title'}):
		print site.text.encode('utf-8')
