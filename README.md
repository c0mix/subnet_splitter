# subnet_splitter
This utility will help you splitting your big subnets in smaller ones. 
## Instructions
The script takes as inputs:
- a file with a list of subnets (-i --input)
- a number that represents the subnet dimension you want to obtain (-s --size)
- an output file (-o --output)
Input file example:
```
$ cat /tmp/input_big.txt
217.141.57.208/29
195.103.115.74/32 
193.108.60.0/22 
82.112.223.136/32
```
Program execution example:
```
$ python3 subnet_splitter.py -i /tmp/input_big.txt -o /tmp/output.txt -s 26
```
Output example:
```
cat /tmp/output.txt 
217.141.57.208/29 
195.103.115.74/32 
193.108.60.0/26 
193.108.60.64/26 
193.108.60.128/26 
...
```
