# XRay Proxy Validator

🚀 Advanced proxy and VPN configuration validator with multi-stage testing, IP reputation checking, and performance analysis.

Supports **VLESS**, **VMess**, **Trojan**, and **ShadowSocks** protocols with comprehensive validation pipeline.

---

## 📋 Features

### Core Validation Stages

1. **Stage 1: TCP Connectivity Check**
   - Direct TCP connection testing
   - Fast initial proxy validation
   - Detects unreachable hosts

2. **Stage 2: XRay Protocol Validation**
   - Full protocol parsing and testing
   - Supports VLESS, VMess, Trojan, ShadowSocks
   - Configuration syntax validation

3. **Stage 3: IP Reputation Check**
   - DNSBL queries (Spamhaus, SpamCop, SORBS)
   - Blacklist status verification
   - Caching mechanism for performance

4. **Stage 4: Speed Testing**
   - Bandwidth measurement
   - Download speed analysis
   - Configurable thresholds

5. **Stage 5: Stability Testing**
   - Multiple connection attempts
   - Success rate calculation
   - Reliability metrics

6. **Stage 6: Route Quality Analysis**
   - Latency measurement to multiple hosts
   - Geographic routing analysis
   - Quality scoring

7. **Stage 7: TLS/Reality Validation**
   - Certificate validation
   - Fingerprint checking
   - Security protocol verification

### Additional Features

- **Multi-threaded Processing**: Concurrent proxy validation (configurable worker count)
- **Result Caching**: IP reputation cache to reduce DNSBL queries
- **Detailed Logging**: Comprehensive stage-by-stage reporting
- **JSON Output**: Structured results for integration
- **Configuration Presets**: Customizable test parameters
- **GitHub Actions Support**: CI/CD integration ready

---

## 🛠️ Installation

### Requirements

- Python 3.8+
- XRay-core (auto-downloaded on first run)
- Linux/Ubuntu (or Windows with WSL)

### Setup

```bash
# Clone the repository
git clone https://github.com/kort0881/xray-proxy-validator.git
cd xray-proxy-validator

# Install dependencies
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Maximum latency threshold (ms)
MAX_LATENCY = 2000

# TCP connection timeout (seconds)
TCP_TIMEOUT = 3

# Enable/disable validation stages
ENABLE_STAGE3_IP_REPUTATION = True
ENABLE_STAGE4_SPEED_TEST = True
ENABLE_STAGE5_STABILITY = True
ENABLE_STAGE6_ROUTE_QUALITY = True
ENABLE_STAGE7_TLS_VALIDATION = True

# Minimum speed requirement (Mbps)
MIN_SPEED_MBPS = 1.0

# Proxy sources (replace with your own)
KEY_SOURCES = {
    'source1': ['https://example.com/proxies.txt'],
    'source2': ['https://example.com/premium.txt'],
}
```

---

## 🚀 Usage

### Basic Validation

```bash
python proxy_validator.py
```

### With Custom Config

```bash
python proxy_validator.py --config custom_config.py
```

### Process Proxy List from File

```bash
python proxy_validator.py --input proxies.txt
```

### Output Results

Results are saved to `results/` directory:

- `verified_*.txt` - Validated working proxies
- `raw_*.txt` - Raw unfiltered results  
- `detailed_*.json` - Detailed metrics per proxy

---

## 📊 Output Format

### Text Format (verified_*.txt)

```
vless://uuid@host:port?security=tls&sni=domain&fp=chrome#[latency|quality|protocol|comments]
trojan://password@host:port?security=tls#[comments]
```

### JSON Format (detailed_*.json)

```json
{
  "key": "vless://...",
  "protocol": "VLESS",
  "host": "example.com",
  "port": 443,
  "latency_ms": 120,
  "speed_mbps": 45.5,
  "stability": {
    "checks": 3,
    "success_rate": 0.95
  },
  "reputation": {
    "blacklisted": false
  },
  "tls_validation": {
    "valid": true,
    "fingerprint": "chrome"
  }
}
```

---

## 🔧 Advanced Usage

### Using with GitHub Actions

Add to `.github/workflows/validate.yml`:

```yaml
name: Proxy Validation
on: [push, schedule]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: python proxy_validator.py
      - uses: actions/upload-artifact@v2
        with:
          name: results
          path: results/
```

### Integrate with Telegram Bot

```python
from proxy_validator import validate_proxies

# Use validated proxies in your bot
results = validate_proxies(proxy_list)
for proxy in results:
    if proxy['valid']:
        use_proxy_in_bot(proxy['key'])
```

---

## 📝 Configuration File Example

Create `sources.config` with your proxy sources:

```
# Replace with your actual proxy sources
# Format: https://example.com/proxies.txt
# Add multiple sources separated by newlines

# Premium sources (customize these)
https://example.com/premium.txt
https://example.com/elite.txt

# Free sources
https://example.com/free.txt
```

**⚠️ Important**: Replace example sources with your actual proxy sources.

---

## 📚 Supported Protocols

### VLESS (XTLS/Vision)
```
vless://uuid@host:port?security=tls&encryption=none&sni=domain#comment
```

### VMess
```
vmess://base64encodedconfig#comment
```

### Trojan
```
trojan://password@host:port?security=tls&sni=domain#comment
```

### ShadowSocks (SIP002)
```
ss://base64method:password@host:port#comment
```

---

## 🔐 Security Notes

- **Never commit real proxy sources or credentials** to git
- Always use `.gitignore` for sensitive data
- Cache directory (`/cache`) is ignored automatically
- Results directory (`/results`) contains unencrypted data - handle carefully
- GitHub tokens should use environment variables

---

## 🐛 Troubleshooting

### XRay not downloading
```bash
# Check internet connection
# Manually place xray binary in xray/ folder
# Check GitHub release page for your OS
```

### "No proxies found"
```bash
# Verify proxy sources are accessible
# Check format of proxy strings
# Ensure proxies haven't expired
```

### Slow validation
```bash
# Reduce MAX_LATENCY threshold
# Disable unnecessary stages
# Increase thread worker count
```

---

## 📖 Documentation

Detailed documentation and protocol references:

- [VLESS Specification](https://github.com/XTLS/VLESS)
- [XRay-core Project](https://github.com/XTLS/Xray-core)
- [Trojan Protocol](https://trojan-gfw.github.io/)

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## 📢 Updates & Community

Follow updates and join community:

- **Telegram Channel**: [@vlesstrojan](https://t.me/vlesstrojan)
- **Telegram Bot**: [@vlessbots_bot](https://t.me/vlessbots_bot)

---

## ⚖️ Legal

This tool is for educational and testing purposes. Users are responsible for:

- Complying with local laws and regulations
- Obtaining proper authorization before testing proxies
- Respecting server resources and rate limits
- Handling proxy data securely

---

## 📄 License

MIT License - See LICENSE file for details

---

**Last Updated**: 2026  
**Maintainer**: [kort0881](https://github.com/kort0881)
