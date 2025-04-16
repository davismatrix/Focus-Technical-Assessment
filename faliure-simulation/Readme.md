**# Failure Simulation**

# TLS Failure (expired cert)

**Step 1: Simulating the Failure**
- I deleted the ingress TLD secret
`kubectl delete secret ca-key-pair`

Step 2: How I dectect the failure
- failure to access https endpoints
- monitoring alerts on /ready failing
- curl `https://demo.local` returns
curl: (60) SSL Certificate problem: unable to get local issuer certificate

Setp 3: How i troubleshoot / diagnose the failure
- I checked ingress events:
`kubectl describe ingress demo-ingress` will see error
> Error: secret "ca-key-pair" not found or invalid
- I also checked HAProxy ingress logs
`kubectl logs - n haproxy-controller deploy/haproxy-ingress-kubernetes-ingress`
- I also checked TLS certificate
`kubectl get secret ca-key-pair -o yaml`

Step 4:  Fixing the issue
Reissue the certificate using cert-manager and ClusterIssuer
`kubectl apply -f certificate.yml`

Step 5: Preventative measures
Enabled cert-manager auto-renewal via Certificate resources
