"""
Phase - 1 packet train

Created on Fri Oct 30 15:41:42 2020

@author: POP PC (60070019) for TSIT Project 63
"""

"""Assign File Name here"""

import time

begin = time.time()

import csv

csv_file_text = "%s.csv" % ("train_text_R3")
csv_file_bin = "%s.csv" % ("train_binary_R3")

"""Assign Variable here"""

# the value number must %2 (or mod 2) = 0
import ipaddress

# ------------------------------------ POOL --------------------------
"""Assign IP soruce Address here"""
ip_src_all = []
net4 = ipaddress.ip_network('192.168.0.0/16')

for x in net4.hosts():
    ip_src_all.append(str(x))

"""Assign IP Destination Address here"""
ip_dst_all = ['161.246.34.11/24']
    
"""Assign Port here"""
port_all = ['22','80']

"""Assign Protocol here"""
protocol_all = ['6','17']

# ------------------------------------ RULES --------------------------
"""Assign Firewall Rule here"""
rule_1 = ['allow', '192.168.0.0/16','161.246.34.11/24', '80', '6'] # Set 1
rule_2 = ['deny', '192.168.128.0/18', '161.246.34.11/24', '22', '17'] 
rule_3 = ['allow', '192.168.64.0/24', '161.246.34.11/24', '22', '6'] # Set 2
rule_4 = ['deny', '192.168.64.0/24', '161.246.34.11/24', '80', '17']
rule_5 = ['allow', '192.168.192.0/18', '161.246.34.11/24', '22', '17'] # Set 3
rule_6 = ['allow', '192.168.128.0/18', '161.246.34.11/24', '22', '6'] 

# ------------------------------------ RATIO --------------------------
"""Assign Packet Number Wanted"""
ruleN_1 = 5000  
ruleN_2 = 5000
ruleN_3 = 5000
ruleN_4 = 5000
ruleN_5 = 5000
ruleN_6 = 5000
default = 5000
    
import random

def random_packet(): # will fix it later
    
    src_address = random.choice(ip_src_all)
    src_mask = "255.255.0.0"
    dst_address = str(ipaddress.IPv4Interface(ip_dst_all[0]).ip)
    dst_mask = str(ipaddress.IPv4Interface(ip_dst_all[0]).netmask)
    port = random.choice(port_all)
    protocol = random.choice(protocol_all)
        
    raw_data_packet = [src_address, src_mask, dst_address, dst_mask, port, protocol]
    
    return raw_data_packet
    
def rule_packet_possible(firewall_rule):
    
    raw_data_packet = []
    
    net4 = ipaddress.ip_network(firewall_rule[1])
    
    for x in net4.hosts():
        raw_data_packet.append([str(x), '255.255.0.0', str(ipaddress.IPv4Interface(ip_dst_all[0]).ip), 
                                str(ipaddress.IPv4Interface(ip_dst_all[0]).netmask), firewall_rule[3], firewall_rule[4]])
        
    return raw_data_packet

#------------------------ raw train data set from rule -------------------------------------------

rule_1_possible = rule_packet_possible(rule_1)
rule_1_quota = [] # use this as output
for i in range(ruleN_1):
    temp = [rule_1[0]] + random.choice(rule_1_possible)
    rule_1_quota.append(temp)
    
rule_2_possible = rule_packet_possible(rule_2)
rule_2_quota = [] # use this as output
for i in range(ruleN_2):
    temp = [rule_2[0]] + random.choice(rule_2_possible)
    rule_2_quota.append(temp)
    
rule_3_possible = rule_packet_possible(rule_3)
rule_3_quota = [] # use this as output
for i in range(ruleN_3):
    temp = [rule_3[0]] + random.choice(rule_3_possible)
    rule_3_quota.append(temp)
    
rule_4_possible = rule_packet_possible(rule_4)
rule_4_quota = [] # use this as output
for i in range(ruleN_4):
    temp = [rule_4[0]] + random.choice(rule_4_possible)
    rule_4_quota.append(temp)
    
rule_5_possible = rule_packet_possible(rule_5)
rule_5_quota = [] # use this as output
for i in range(ruleN_5):
    temp = [rule_5[0]] + random.choice(rule_5_possible)
    rule_5_quota.append(temp)
    
rule_6_possible = rule_packet_possible(rule_6)
rule_6_quota = [] # use this as output
for i in range(ruleN_6):
    temp = [rule_6[0]] + random.choice(rule_6_possible)
    rule_6_quota.append(temp)
    
#------------------------ merge all packet in rule to check default-----------------------------------------------------
    
all_rule_possible = rule_1_possible + rule_2_possible + rule_3_possible + rule_4_possible + rule_5_possible + rule_6_possible
    
#------------------------ raw train data set from universe ---------------------------------------
default_quota = []
while True:
    rand =  random_packet()
    if len(default_quota) == default:
        break
    elif rand not in all_rule_possible:
        temp = ["deny"] + rand
        default_quota.append(temp)

#------------------------- merge list of all train set --------------------------------------------

data_set_text = rule_1_quota + rule_2_quota + rule_3_quota + rule_4_quota + rule_5_quota + rule_6_quota + default_quota
train_set_text = rule_1_quota + rule_2_quota + rule_3_quota + rule_4_quota + rule_5_quota + rule_6_quota + default_quota
random.shuffle(train_set_text)

#------------------------- binary convert --------------------------------------------------------

train_set_binary = []

for train_packet in train_set_text:
    binary_a_packet = []
    if train_packet[0] == 'allow':
        binary_a_packet.append('1')
    else:
        binary_a_packet.append('0')
    for j in range(1, 5):
        ip = train_packet[j]
        list_octet = [bin(int(x)+256)[3:] for x in ip.split('.')]
        binary_a_packet.append(list_octet[0])
        binary_a_packet.append(list_octet[1])
        binary_a_packet.append(list_octet[2])
        binary_a_packet.append(list_octet[3])
    binary_a_packet.append(bin(int(train_packet[5])+65536)[3:])
    binary_a_packet.append(bin(int(train_packet[6])+256)[3:])
    # train_packet[6]
    train_set_binary.append(binary_a_packet)

#-------------------------- csv write -------------------------------------------------------------

with open(csv_file_text, 'w', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(["Action", "Source address", "Source Mask", "Destination address", "Destination Mask", "Port", "Protocol"])
    
    for i in train_set_text:
        wr.writerow(i)
    
    
with open(csv_file_bin, 'w', newline='') as myfile:
    column = ["Act","src_a1","src_a2","src_a3","src_a4","src_m1","src_m2","src_m3","src_m4","dst_a1","dst_a2","dst_a3","dst_a4","dst_m1","dst_m2","dst_m3","dst_m4","port","protocol",]
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(column)
    
    for i in train_set_binary:
        wr.writerow(i)

end = time.time()

print("SUMMARY:",str(csv_file_text),"\nPacket Created:", len(train_set_text), "packets\nTime used:", end-begin, "seconds") 

i,j = [], []