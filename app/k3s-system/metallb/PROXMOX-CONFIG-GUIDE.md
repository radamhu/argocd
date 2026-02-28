# MetalLB on Proxmox - Required Configuration

This guide documents the **mandatory** Proxmox VM and network settings required for MetalLB L2 mode to work reliably.

## The Problem

MetalLB speaker pods crash or become unreachable because:
1. **Proxmox bridge STP delay** drops initial GARP announcements at boot
2. **Proxmox firewall/bridge filtering** blocks ARP packets from the speaker
3. **MAC address filtering** prevents MetalLB from announcing virtual IPs

## Solution: 3-Part Fix

### Part 1: Proxmox VM Network Settings ⚙️

**On the Proxmox host**, configure the VM's network interface:

```bash
# SSH into your Proxmox host
ssh root@proxmox-host

# Edit the VM config (replace 100 with your VM ID)
# Add or modify the net0 line:
qm set <VM_ID> --net0 virtio=XX:XX:XX:XX:XX:XX,bridge=vmbr0,firewall=0

# Disable MAC address filtering
# This is CRITICAL - allows MetalLB to announce virtual MACs
```

#### Option A: Via Proxmox Web UI

1. Select your K3s VM → **Hardware** → **Network Device**
2. Click **Edit**
3. **Uncheck** "Firewall"
4. Click **OK**
5. Restart the VM

#### Option B: Via Proxmox CLI

```bash
# Show current network config
qm config <VM_ID> | grep net0

# Disable firewall on network interface
qm set <VM_ID> --net0 virtio=<MAC>,bridge=vmbr0,firewall=0

# Verify
qm config <VM_ID> | grep net0
```

### Part 2: Proxmox Bridge Configuration 🌉

**Check and configure the bridge** (usually `vmbr0`):

```bash
# SSH into Proxmox host

# Check current bridge config
cat /etc/network/interfaces | grep -A 10 vmbr0

# Ensure these settings in /etc/network/interfaces:
```

```
auto vmbr0
iface vmbr0 inet static
    address 192.168.0.X/24  # Your Proxmox host IP
    gateway 192.168.0.1
    bridge-ports eno1       # Your physical NIC
    bridge-stp off          # CRITICAL: Disable STP
    bridge-fd 0             # CRITICAL: No forwarding delay
    bridge-vlan-aware yes
```

**Apply changes:**

```bash
# Backup first
cp /etc/network/interfaces /etc/network/interfaces.backup

# Edit
nano /etc/network/interfaces

# Apply (non-destructive, preserves connections)
ifreload -a

# Or reboot Proxmox host if needed
reboot
```

### Part 3: Deploy the Kubernetes Fix 🛠️

The ArgoCD application now includes:

1. **Watchdog deployment** - Restarts speakers 60s after boot to re-send GARP
2. **Optimized speaker config** - Better memberlist and ARP settings
3. **Tolerations** - Ensures speakers run on all nodes

#### Apply the Configuration

```bash
# From your workstation with kubectl access

# Commit and push the changes
cd /home/ferko/Documents/argocd
git add app/k3s-system/metallb/
git commit -m "fix: MetalLB Proxmox compatibility fixes"
git push

# ArgoCD will auto-sync, or manually sync:
kubectl -n argocd get application metallb
# Wait for sync or force it via ArgoCD UI
```

#### Verify Deployment

```bash
# Check MetalLB pods
kubectl get pods -n metallb-system
# You should see:
# - controller pod (1)
# - speaker pods (1 per node)
# - metallb-watchdog pod (1)

# Check watchdog logs
kubectl logs -n metallb-system -l app=metallb-watchdog

# Check speaker logs
kubectl logs -n metallb-system -l app.kubernetes.io/component=speaker

# Verify LoadBalancer IPs are assigned
kubectl get svc --all-namespaces | grep LoadBalancer
```

## Validation Tests

### Test 1: Immediate Connectivity

```bash
# Get a LoadBalancer IP
LB_IP=$(kubectl get svc traefik -n traefik -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

# Ping from outside the cluster (different machine on LAN)
ping -c 5 $LB_IP

# Check ARP table on your router or a LAN machine
arp -a | grep $LB_IP
# Should show a MAC address
```

### Test 2: Boot Test

```bash
# Reboot the K3s VM
ssh k3s-vm
sudo reboot

# Wait 2-3 minutes for full boot + watchdog delay

# From another machine, test connectivity
ping -c 10 192.168.0.103  # Your LoadBalancer IP

# Should be reachable without manual intervention
```

### Test 3: Long-term Stability

```bash
# Monitor for crashes over 30 minutes
watch -n 30 'kubectl get pods -n metallb-system'

# Check for restarts (RESTARTS column should be 0 or low)
# Speaker pods should NOT be CrashLoopBackOff
```

## Troubleshooting

### Speakers still crashing?

```bash
# Check speaker logs for errors
kubectl logs -n metallb-system -l app.kubernetes.io/component=speaker --tail=100

# Common errors:
# - "Failed to announce" → Proxmox bridge/firewall blocking
# - "Memberlist" errors → Network connectivity issues between nodes
```

### Watchdog not running?

```bash
# Check ArgoCD sync status
kubectl get application -n argocd metallb -o yaml | grep syncResult -A 20

# Force sync
kubectl patch application metallb -n argocd --type merge -p '{"operation":{"initiatedBy":{"username":"admin"},"sync":{"revision":"HEAD"}}}'
```

### IPs still unreachable after reboot?

1. **Check Proxmox firewall:**
   ```bash
   # On Proxmox host
   qm config <VM_ID> | grep firewall
   # Should show firewall=0
   ```

2. **Check bridge STP/FD:**
   ```bash
   # On Proxmox host
   bridge link show | grep vmbr0
   brctl show vmbr0
   ```

3. **Manually test GARP:**
   ```bash
   # Inside a speaker pod
   kubectl exec -it -n metallb-system <speaker-pod> -- sh
   # Check if arping is available or use ip:
   ip neigh show
   ```

## Why This Works

1. **Bridge STP/FD=0**: No delay at boot, GARP packets sent immediately
2. **Firewall=0 on VM NIC**: Proxmox doesn't filter ARP/GARP packets
3. **Watchdog**: Restarts speakers after 60s to guarantee GARP is sent post-boot
4. **Memberlist**: Better coordination between speaker pods across nodes
5. **Tolerations**: Speakers run even on control-plane nodes

## References

- [MetalLB L2 Mode Documentation](https://metallb.universe.tf/configuration/_advanced_l2_configuration/)
- [Proxmox Network Configuration](https://pve.proxmox.com/wiki/Network_Configuration)
- [GitHub Issue: MetalLB on Proxmox](https://github.com/metallb/metallb/issues/284)

## Summary Checklist

- [ ] Proxmox VM firewall disabled on network interface
- [ ] Bridge STP disabled (`bridge-stp off`)
- [ ] Bridge forwarding delay set to 0 (`bridge-fd 0`)
- [ ] MetalLB watchdog deployment applied
- [ ] ArgoCD synced successfully
- [ ] Tested reboot - LoadBalancer IPs reachable within 2 minutes
- [ ] No speaker crashes after 30+ minutes
