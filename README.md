# pfSense Network Metrics Collector

## Overview
Python script for collecting and analyzing network metrics from pfSense firewall/router installations.

## Features
- Retrieve network performance statistics
- Monitor firewall traffic data
- Export metrics to various formats

## Requirements
- Python 3.8+
- `requests` library
- pfSense API access

## Installation
```bash
git clone https://github.com/yourusername/pfsense-metrics.git
pip install -r requirements.txt
```

## Usage
```python
python pfsense_metrics.py --host 192.168.1.1 --api-key YOUR_API_KEY
```

## Configuration
Configure connection details in `config.yaml`

## License
MIT License
