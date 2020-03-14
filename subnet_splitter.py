'''
Author: Lorenzo Comi

This utility will help you splitting your big subnets in smaller ones.
The script takes as inputs:
- a file with a list of subnets (-i --input)
- a number that represents the subnet dimension you want to obtain (-s --size)
- an output file (-o --output)

Example:
$ cat /tmp/input_big.txt
217.141.57.208/29
195.103.115.74/32
193.108.60.0/22
82.112.223.136/32

$ python3 subnet_splitter.py -i /tmp/input_big.txt -o /tmp/output.txt -s 26 -v
217.141.57.208/29
195.103.115.74/32
193.108.60.0/26
193.108.60.64/26
193.108.60.128/26
...

$ cat /tmp/output.txt
217.141.57.208/29
195.103.115.74/32
193.108.60.0/26
193.108.60.64/26
193.108.60.128/26
...
'''

import ipaddress
import argparse
import os


def check_args(args):
	if not os.path.isfile(args.input):
		exit('[-] Input file does not exists! Please specify a correct filename/path')
	if int(args.size) > 32:
		exit('[-] Incorrect CIDR size! Specify a value lower that 32')

parser = argparse.ArgumentParser(description='This script will help you splitting your big subnets in smaller ones. $ python3 subnet_splitter.py -i /tmp/input_big.txt -o /tmp/output.txt -s 26')
parser.add_argument('-i', '--input', help='Input file', required=True)
parser.add_argument('-o', '--output', help='Output file', required=True)
parser.add_argument('-s', '--size', help='The size of the subnet you want to obtain', required=True)
parser.add_argument('-v', '--verbose', help='Print verbose outputs', action="store_true", required=False, default=False)
args = parser.parse_args()
check_args(args)

input = open(args.input, 'r')
output = open(args.output, 'w')

for line in input.readlines():
	try:
		sub_size = int(ipaddress.ip_network(line.strip()).prefixlen)
		# the input subnet is smaller than the one we want as output. NO SPLIT REQUIRED HERE
		if sub_size >= int(args.size):
			output.write(str(ipaddress.ip_network(line.strip())))
			if args.verbose:
				print(str(ipaddress.ip_network(line.strip())))

		# the input subnet is bigger than the one we want as output. SPLIT REQUIRED
		elif sub_size < int(args.size):
			for subnet in list(ipaddress.ip_network(line.strip(), strict=False).subnets(new_prefix=int(args.size))):
				output.write(str(subnet)+'\n')
				if args.verbose:
					print(str(subnet))
	except:
		print('[-] Probably the CIDR notation for this subnet is wrong: {} \nAnyway it will not be splitted but it will be added to the output as is.'.format(line.strip()))
		output.write(line)

input.close()
output.close()
