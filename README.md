# wireguard-reinstate-peers
Python script for reinstating WireGuard® peers that have been "offline" for more than 180 seconds.

### Problem: The public IP address of a peer is stored in memory indefinitely
If you run the WireGuard® command line tool wg(8) on your server, you can see a peer's endpoint. The output should be like:

```
peer: /X3nyLMlOSmahCVNIsSqqT8vh9pkeEdOsoAwaoo9uUZ=
  endpoint: 195.230.111.45:52402
  allowed ips: 10.200.200.2/32
  latest handshake: 5 hours, 13 minutes, 10 seconds ago
  transfer: 158.31 KiB received, 365.59 KiB sent
```

As you can see, WireGuard® is associating the peer's public key with it's endpoint ip.

This cannot be remedied when a connection is active as WireGuard® of course needs to know, where to send the encrypted packets to. But when a connection becomes "inactive", this is a privacy issue.

### Solution
WireGuard® uses sessions and this gives us a point of action!

Internally WireGuard® stores the time of the latest handshake so that it knows what to do when exchanging data with a peer:
- When fewer than 120 seconds have elapsed, just send data as the session is still active.
- 120 to 179 seconds have elapsed, send data and interleave a handshake to renew the session. 
- More than 180 seconds have elapsed, handshake to renew the session before data is sent.

So, we can solve this issue. When it is reasonably clear that the peer and server have stopped talking, the peer’s configuration can be deleted and then reinstated. A "reasonable" criteria is e.g. latest handshake is more than 180 seconds ago.

This removes the peer information and configures the server to wait for an incoming handshake. The example above becomes:

```
peer: /X3nyLMlOSmahCVNIsSqqT8vh9pkeEdOsoAwaoo9uUZ=
  allowed ips: 10.200.200.2/32
```

This Python script scans the list of peers for those that have the latest handshake time greater than 180 seconds ago and deletes/reinstates their configuration.

### @Community
There is room for improvements - feel free to open a PR :-)
Thanks!
