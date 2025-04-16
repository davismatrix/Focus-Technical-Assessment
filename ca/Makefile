.PHONY: all ca cert-manager metallb ingress-dns haproxy clean

all: ca cert-manager metallb haproxy ingress-dns

ca:
	@echo "🔐 Generating Local CA..."
	./scripts/setup-ca.sh

cert-manager:
	@echo "📜 Installing cert-manager and ClusterIssuer..."
	kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml
	sleep 5
	kubectl create namespace cert-manager --dry-run=client -o yaml | kubectl apply -f -
	kubectl apply -f ./certs/cluster-issuer.yml
	kubectl create secret tls ca-key-pair --cert=./certs/ca.pem --key=./certs/ca-key.pem -n cert-manager --dry-run=client -o yaml | kubectl apply -f -

metallb:
	@echo "📦 Installing and configuring MetalLB..."
	kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.10/config/manifests/metallb-native.yaml
	sleep 5
	kubectl create secret generic -n metallb-system memberlist --from-literal=secretkey="$$(openssl rand -base64 128)" --dry-run=client -o yaml | kubectl apply -f -
	kubectl apply -f ../deploy/metallb-config.yml

ingress-dns:
	@echo "🌐 Adding demo.local to /etc/hosts..."
	IP=172.20.0.10 ; \
	if ! grep -q "$IP demo.local" /etc/hosts; then \
		echo "$IP demo.local" | sudo tee -a /etc/hosts; \
	fi

haproxy:
	@echo "📥 Installing HAProxy Ingress Controller..."
	helm repo add haproxytech https://haproxytech.github.io/helm-charts
	helm repo update
	helm upgrade --install haproxy-ingress haproxytech/kubernetes-ingress \
	  --namespace haproxy-controller \
	  --create-namespace \
	  --set controller.service.type=LoadBalancer \
	  --set controller.service.LoadBalancerIP=172.20.0.100

clean:
	rm -f certs/ca.pem certs/ca-key.pem certs/ca.csr
