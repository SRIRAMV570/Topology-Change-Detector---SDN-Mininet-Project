# Topology Change Detector

A POX OpenFlow controller module that monitors and manages SDN network topology changes in real-time.

## Overview

The Topology Change Detector is a specialized POX controller that actively monitors network events and maintains an up-to-date view of the network topology. It tracks switch connections, link status, and packet flows while logging all changes for network visibility and debugging.

## Features

### ✅ Monitor Switch/Link Events
- **Switch Connection Tracking**: Detects and logs when switches connect/disconnect from the controller
- **Real-time Event Handling**: Responds immediately to OpenFlow events (ConnectionUp, PacketIn)
- **Network State Awareness**: Maintains awareness of active switches and their connection status
- **Packet-Level Monitoring**: Tracks incoming packets and their source switches/ports

### ✅ Update Topology Map
- **Dynamic Topology Maintenance**: Automatically updates the network topology as switches join/leave
- **Port Management**: Tracks packets arriving on specific switch ports
- **Flow Routing**: Directs traffic based on switch configuration and port rules
- **ARP Handling**: Automatically floods ARP requests to discover topology

### ✅ Display Changes
- **Rich Console Logging**: Uses emoji-enhanced logging for visual clarity
  - 🟢 Green indicator for switch connections
  - 📦 Package indicator for packet events
  - 🔥 Fire icon for controller startup
- **Detailed Event Information**: Logs switch DPIDs (datapath IDs) and port information
- **Visual Distinction**: Easy identification of network events in logs

### ✅ Log Updates
- **Comprehensive Event Logging**: All topology changes are recorded with timestamps
- **Switch Connection Logs**: Records each switch connection event
- **Packet Flow Logs**: Tracks all incoming packets with source and port information
- **Debug-Friendly Output**: Structured logs aid in troubleshooting and analysis

## Architecture

```
TopologyDetector
├── Switch Connection Management
│   └── _handle_ConnectionUp()
├── Packet Processing
│   └── _handle_PacketIn()
└── Controller Integration
    └── launch()
```

## Usage

### Installation

1. Place `topology_detector.py` in the POX extensions directory:
   ```
   pox/ext/topology_detector.py
   ```

2. Ensure you have POX installed with OpenFlow support

### Running the Controller

```bash
python pox.py topology_detector
```

### With Additional POX Modules

```bash
python pox.py openflow.discovery topology_detector
```

## How It Works

### 1. **Initialization**
   - Registers the controller with POX core
   - Adds listeners for OpenFlow events
   - Logs startup confirmation

### 2. **Switch Connection Handling**
   - Listens for `ConnectionUp` events
   - Records new switch connections with their DPIDs
   - Updates active topology

### 3. **Packet Processing**
   - Captures incoming packets from switches
   - Validates packet structure (prevents parsing errors)
   - Handles different packet types:
     - **ARP Packets (0x0806)**: Floods to all ports for discovery
     - **IPv4 Packets (0x0800)**: Routes based on switch-specific rules
     - **Other Types**: Discarded for safety

### 4. **Packet Routing**
   - Switch 1 & 2: Forward from port 1 → ports 2, 3; other ports → port 1
   - Switch 3: Forward from port 1 → port 2; other ports → port 1

## Configuration

### Supported Switches
- Switch 1 (DPID: 1)
- Switch 2 (DPID: 2)
- Switch 3 (DPID: 3)

### Port Mapping
- **Primary/Backup Configuration**: Implements redundancy patterns
- **Flexible Routing**: Can be customized per switch/port requirements

## Log Output Example

```
🔥 Final Clean Controller Started
🟢 Switch Connected: 1
📦 Packet received at switch 1 on port 1
📦 Packet received at switch 1 on port 2
🟢 Switch Connected: 2
📦 Packet received at switch 2 on port 1
```

## Event Types Tracked

| Event | Description | Log Level |
|-------|-------------|-----------|
| Controller Start | POX controller initialization | INFO |
| Switch Connect | Switch connects to controller | INFO |
| Packet In | Packet received at switch | INFO |
| ARP Detection | ARP packet processing | INFO |
| IPv4 Routing | IPv4 packet forwarding | INFO |

## Benefits

- **Real-Time Visibility**: See topology changes as they happen
- **Debugging Support**: Detailed logs help identify network issues
- **Automatic Discovery**: ARP flooding enables automatic topology learning
- **Scalability**: Event-driven architecture scales with network size
- **Non-Invasive**: Monitors without disrupting network operation

## Dependencies

- **POX Controller**: OpenFlow controller framework
- **OpenFlow 1.0**: Protocol support (libopenflow_01)
- **Python 2/3**: Compatible with both versions

## Troubleshooting

### No Switch Connections Detected
- Verify switches are configured to connect to controller IP/port
- Check firewall rules on controller machine
- Confirm OpenFlow protocol version compatibility

### Packets Not Being Logged
- Ensure switches are connected (check for 🟢 green indicators)
- Verify packet types match supported protocols (ARP, IPv4)
- Check controller logs for parsing errors

### Missing Topology Updates
- Confirm all switches are sending connection events
- Verify event handlers are registered correctly
- Check for exceptions in POX logs

## Future Enhancements

- [ ] Dynamic topology learning (no hardcoded switch rules)
- [ ] Link discovery using LLDP packets
- [ ] Topology graph visualization
- [ ] Web-based topology dashboard
- [ ] Switch/port status queries
- [ ] Network resilience testing

## License

This module is part of the POX OpenFlow controller framework.

## Contact & Support

For issues or questions, refer to POX documentation:
- POX GitHub: https://github.com/noxrepo/pox
- POX Documentation: https://github.com/noxrepo/pox/wiki
