# MetalLB on Proxmox K3s

## Problem

MetalLB speaker pods crash repeatedly on Proxmox + k3s setup. Manual restart works temporarily but crashes return within minutes.

**Manual workaround (temporary):**
```bash
kubectl delete pod -n metallb-system -l app.kubernetes.io/component=speaker
```

## Root Causes

1. **Proxmox Bridge STP Delay**: Network bridge takes seconds to reach forwarding state at boot. Initial GARP announcements are dropped before router learns the MAC address.

2. **Proxmox Firewall/Bridge Filtering**: Default Proxmox firewall and MAC filtering block ARP/GARP packets from MetalLB speakers, causing ongoing connectivity issues.

3. **ARP Cache Expiration**: Even after manual restart, ARP entries expire after a few minutes and MetalLB cannot refresh them due to Proxmox filtering.

## Solution (3 Parts)

### 1. Proxmox VM Configuration
**Critical settings on Proxmox host** - See [PROXMOX-CONFIG-GUIDE.md](PROXMOX-CONFIG-GUIDE.md):
- Disable VM firewall on network interface
- Set bridge STP off
- Set bridge forwarding delay to 0

### 2. MetalLB Watchdog
Automatically restarts speaker pods 60 seconds after boot to ensure GARP is sent after bridge is ready.
- File: `metallb-watchdog-deployment.yaml`
- Runs once per boot, then sleeps indefinitely
- Prevents race condition between k3s startup and Proxmox bridge

### 3. Optimized MetalLB Configuration
Enhanced speaker settings for Proxmox compatibility:
- Memberlist enabled for better coordination
- Tolerations to run on all nodes
- Improved ARP announcement settings

## Files

- `argocd-metallb.yaml` - ArgoCD application with optimized helm values
- `metallb-config.yaml` - IPAddressPool and L2Advertisement
- `metallb-watchdog-deployment.yaml` - Boot-time speaker restarter
- `PROXMOX-CONFIG-GUIDE.md` - Complete Proxmox configuration guide

## Quick Start

1. **Configure Proxmox** (required first):
   ```bash
   # On Proxmox host
   qm set <VM_ID> --net0 virtio=<MAC>,bridge=vmbr0,firewall=0
   ```
   See [PROXMOX-CONFIG-GUIDE.md](PROXMOX-CONFIG-GUIDE.md) for complete steps.

2. **Deploy via ArgoCD**:
   ```bash
   git add app/k3s-system/metallb/
   git commit -m "fix: MetalLB Proxmox compatibility"
   git push
   # ArgoCD auto-syncs
   ```

3. **Verify**:
   ```bash
   kubectl get pods -n metallb-system
   kubectl logs -n metallb-system -l app=metallb-watchdog
   ```

4. **Test reboot**:
   ```bash
   # Reboot VM, wait 2 minutes, test LoadBalancer IP
   ping <LoadBalancer-IP>
   ```

## Status

✅ **Implemented** - All files created and ArgoCD configured
📋 **Next Step** - Apply Proxmox host configuration (see guide)
