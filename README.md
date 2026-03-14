# wpa-handshake-cracker
Automatic WPA/WPA2 handshake extraction and cracking tool using hashcat and hcxtools.
## Installation

Install required tools:

sudo apt update
sudo apt install hashcat hcxtools

Unzip the default wordlist:

sudo gunzip /usr/share/wordlists/rockyou.txt.gz
## Usage

Run the tool with a capture file:

python3 wpa_cracker.py capture.pcap
python3 wpa_cracker.py capture.pcap -w my_wordlist.txt
python3 wpa_cracker.py capture.pcap --mask '?d?d?d?d?d?d'
?d = digit (0-9)
?l = lowercase letters
?u = uppercase letters
?a = all characters
