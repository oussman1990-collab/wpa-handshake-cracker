# WPA Handshake Cracker

Version: 1.0.0

Automatic WPA/WPA2 handshake extraction and cracking tool using hashcat and hcxtools.

## Installation

Clone the tool:

git clone https://github.com/oussman1990-collab/wpa-handshake-cracker.git

Enter the directory:

cd wpa-handshake-cracker

Install required tools:

sudo apt update
sudo apt install hashcat hcxtools

Unzip the default wordlist:

sudo gunzip /usr/share/wordlists/rockyou.txt.gz

## Usage

Run the tool with a capture file:

python3 wpa_cracker.py capture.pcap

Use a custom wordlist:

python3 wpa_cracker.py capture.pcap -w my_wordlist.txt

Mask attack example (6 digits):

python3 wpa_cracker.py capture.pcap --mask '?d?d?d?d?d?d'

## Mask Symbols

?d = digit (0-9)  
?l = lowercase letters  
?u = uppercase letters  
?a = all characters
