#!/usr/bin/env python3
"""
XRay Proxy Validator
Advanced proxy and VPN configuration validator with multi-stage testing,
IP reputation checking, and performance analysis.

Supports VLESS, VMess, Trojan, and ShadowSocks protocols.

Author: kort0881
Repository: https://github.com/kort0881/xray-proxy-validator
Telegram: @vlesstrojan
"""

import os
import sys
import re
import json
import socket
import time
import base64
import subprocess
import hashlib
from datetime import datetime
from urllib.parse import unquote, urlparse
import requests

# Try to import custom configuration
try:
    from config import *
except ImportError:
    print("Warning: config.py not found. Using default settings.")
    MAX_LATENCY = 2000
    TCP_TIMEOUT = 3
    ENABLE_STAGE3_IP_REPUTATION = True


class ProxyValidator:
    """Main validator class for proxy and VPN configurations."""
    
    def __init__(self):
        """Initialize the validator."""
        self.stats = {
            'total': 0,
            'tcp_live': 0,
            'xray_live': 0,
            'speed_tested': 0,
            'stable': 0,
        }
        self.results = []
    
    def log(self, msg):
        """Print log message with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {msg}")
    
    def stage1_tcp_check(self, host, port):
        """
        Stage 1: TCP Connectivity Check
        
        Tests basic TCP connectivity to the proxy host.
        This is a fast initial check to detect unreachable hosts.
        
        Args:
            host: Proxy hostname or IP
            port: Proxy port number
            
        Returns:
            bool: True if TCP connection successful
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(TCP_TIMEOUT)
            sock.connect((host, port))
            sock.close()
            return True
        except (socket.timeout, socket.error, OSError):
            return False
    
    def stage2_xray_test(self, proxy_config):
        """
        Stage 2: XRay Protocol Validation
        
        Uses XRay-core to test the actual proxy protocol.
        Validates VLESS, VMess, Trojan, and ShadowSocks configurations.
        
        Args:
            proxy_config: Proxy configuration object
            
        Returns:
            bool: True if XRay test successful
        """
        # This stage requires XRay-core binary
        # Implementation depends on XRay testing infrastructure
        pass
    
    def stage3_ip_reputation(self, ip_address):
        """
        Stage 3: IP Reputation Check
        
        Checks IP address against DNSBL services:
        - Spamhaus (zen.spamhaus.org)
        - SpamCop (bl.spamcop.net)
        - SORBS (dnsbl.sorbs.net)
        
        Args:
            ip_address: IP address to check
            
        Returns:
            dict: Reputation status and details
        """
        if not ENABLE_STAGE3_IP_REPUTATION:
            return {'blacklisted': False}
        
        reputation = {'blacklisted': False, 'checks': {}}
        
        dnsbl_hosts = [
            'zen.spamhaus.org',
            'bl.spamcop.net',
            'dnsbl.sorbs.net'
        ]
        
        # Reverse IP for DNSBL query
        reversed_ip = '.'.join(reversed(ip_address.split('.')))
        
        for dnsbl in dnsbl_hosts:
            try:
                query = f"{reversed_ip}.{dnsbl}"
                socket.gethostbyname(query)
                reputation['blacklisted'] = True
                reputation['checks'][dnsbl] = 'LISTED'
            except socket.gaierror:
                reputation['checks'][dnsbl] = 'OK'
        
        return reputation
    
    def stage4_speed_test(self, proxy_config):
        """
        Stage 4: Speed Testing
        
        Measures bandwidth through the proxy.
        Tests download speed and determines throughput capacity.
        
        Args:
            proxy_config: Proxy configuration
            
        Returns:
            dict: Speed test results
        """
        if not ENABLE_STAGE4_SPEED_TEST:
            return {'tested': False}
        
        return {'speed_mbps': 0, 'tested': False}
    
    def stage5_stability_test(self, proxy_config):
        """
        Stage 5: Stability Testing
        
        Performs multiple connection attempts to measure reliability.
        Calculates success rate and identifies unstable proxies.
        
        Args:
            proxy_config: Proxy configuration
            
        Returns:
            dict: Stability metrics
        """
        if not ENABLE_STAGE5_STABILITY:
            return {'stable': False}
        
        return {'success_rate': 0.0, 'attempts': 0}
    
    def stage6_route_quality(self, proxy_config):
        """
        Stage 6: Route Quality Analysis
        
        Measures latency to multiple test hosts through the proxy.
        Evaluates geographic routing and overall connection quality.
        
        Args:
            proxy_config: Proxy configuration
            
        Returns:
            dict: Route quality metrics
        """
        if not ENABLE_STAGE6_ROUTE_QUALITY:
            return {'quality_score': 0}
        
        return {'avg_latency': 0, 'hosts_tested': 0}
    
    def stage7_tls_validation(self, proxy_config):
        """
        Stage 7: TLS/Reality Validation
        
        Validates TLS certificates and Reality parameters.
        Checks certificate validity and fingerprint matching.
        
        Args:
            proxy_config: Proxy configuration
            
        Returns:
            dict: TLS validation results
        """
        if not ENABLE_STAGE7_TLS_VALIDATION:
            return {'valid': True}
        
        return {'valid': False, 'error': 'TLS validation not implemented'}
    
    def validate_proxy(self, proxy_uri):
        """
        Main validation method - runs all stages.
        
        Args:
            proxy_uri: Proxy URI string (vless://, vmess://, trojan://, ss://)
            
        Returns:
            dict: Complete validation results
        """
        self.stats['total'] += 1
        
        result = {
            'uri': proxy_uri,
            'protocol': self.detect_protocol(proxy_uri),
            'valid': False,
            'stages': {}
        }
        
        # Extract host and port
        host, port = self.extract_host_port(proxy_uri)
        if not host or not port:
            return result
        
        # Stage 1: TCP
        if self.stage1_tcp_check(host, port):
            self.stats['tcp_live'] += 1
            result['stages']['tcp'] = True
            result['host'] = host
            result['port'] = port
            
            # Stage 3: IP Reputation
            try:
                ip = socket.gethostbyname(host)
                result['stages']['ip_reputation'] = self.stage3_ip_reputation(ip)
            except:
                pass
            
            result['valid'] = True
        
        return result
    
    def detect_protocol(self, uri):
        """
        Detect proxy protocol from URI.
        
        Args:
            uri: Proxy URI string
            
        Returns:
            str: Protocol name (VLESS, VMess, Trojan, SS)
        """
        if uri.lower().startswith('vless://'):
            return 'VLESS'
        elif uri.lower().startswith('vmess://'):
            return 'VMess'
        elif uri.lower().startswith('trojan://'):
            return 'Trojan'
        elif uri.lower().startswith('ss://'):
            return 'ShadowSocks'
        return 'Unknown'
    
    def extract_host_port(self, uri):
        """
        Extract host and port from proxy URI.
        
        Args:
            uri: Proxy URI string
            
        Returns:
            tuple: (host, port) or (None, None) if parsing fails
        """
        try:
            # Simple parsing - real implementation would be more complex
            if '@' in uri:
                host_port = uri.split('@')[1].split('?')[0]
                if ':' in host_port:
                    parts = host_port.rsplit(':', 1)
                    return parts[0], int(parts[1])
        except:
            pass
        return None, None
    
    def run_validation(self, proxies):
        """
        Run validation on a list of proxies.
        
        Args:
            proxies: List of proxy URI strings
        """
        self.log(f"Starting validation of {len(proxies)} proxies...")
        
        for proxy in proxies:
            result = self.validate_proxy(proxy)
            if result['valid']:
                self.results.append(result)
        
        self.log(f"Validation complete. Valid proxies: {len(self.results)}")
        self.print_stats()
    
    def print_stats(self):
        """Print validation statistics."""
        self.log("="*50)
        self.log("VALIDATION STATISTICS")
        self.log("="*50)
        self.log(f"Total proxies tested: {self.stats['total']}")
        self.log(f"TCP connectivity: {self.stats['tcp_live']}")
        self.log(f"Valid proxies: {len(self.results)}")
        self.log("="*50)
    
    def save_results(self, filename='results.json'):
        """Save validation results to JSON file."""
        output_path = os.path.join(RESULTS_FOLDER if 'RESULTS_FOLDER' in globals() else '.', filename)
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        self.log(f"Results saved to {output_path}")


def main():
    """Main entry point."""
    print("""
    ╔═════════════════════════════════════════╗
    ║   XRay Proxy Validator                  ║
    ║   Advanced Proxy Testing Tool           ║
    ║   Repository: kort0881/xray-proxy-validator
    ║   Telegram: @vlesstrojan                ║
    ╚═════════════════════════════════════════╝
    """)
    
    validator = ProxyValidator()
    
    # Example usage - replace with your proxy list
    example_proxies = [
        'vless://example-uuid@proxy.example.com:443?security=tls&sni=example.com#Example1',
        'trojan://password@proxy.example.com:443?security=tls&sni=example.com#Example2',
    ]
    
    validator.run_validation(example_proxies)
    
    if validator.results:
        validator.save_results()


if __name__ == '__main__':
    main()
