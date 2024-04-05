---

## whoami
## cert-manager https://www.thebookofjoel.com/k3s-cert-manager-letsencrypt

# - name: create TXT record
#   cloudflare_dns:
#   api_token: "{{ cftoken }}"
#   domain: "{{ domain }}"
#   record: "test"
#   type: "TXT"
#   value: "Hello World"

# DELETE DNS RECORD
# - name: create TXT record
#     cloudflare_dns:
#       api_token: "{{ cftoken }}"
#       domain: "{{ domain }}"
#       record: "test"
#       type: "TXT"
#       state: absent

- name: configure "{{ appname }}" application
  shell: |
    # NAMESPACE
    cat << 'EOF' | kubectl apply -f -
    kind: Namespace
    apiVersion: v1
    metadata:
      name: "{{ appname }}"
    EOF

    # DEPLOYMENT
    cat << 'EOF' | kubectl apply -f -
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: "{{ appname }}"
      namespace: "{{ appname }}"
    spec:
      selector:
        matchLabels:
          app: "{{ appname }}" # Pods will be launched if matches deployment Label.
      replicas: 1
      template:
        metadata:
          labels:
            app: "{{ appname }}" # Labels of the Pods.
            name: "{{ appname }}"
        spec:
          #nodeSelector:
            #node-type: worker
          containers:
            - name: "{{ appname }}"
              image: containous/whoami:v1.5.0
              resources:
                requests:
                  memory: "64Mi"
                  cpu: "100m"
                limits:
                  memory: "128Mi"
                  cpu: "500m"
              ports:
                - name: "{{ appname }}"
                  containerPort: 80
    EOF

    # SERVICE
    cat << 'EOF' | kubectl apply -f -
    apiVersion: v1
    kind: Service
    metadata:
      name: "{{ appname }}"
      namespace: "{{ appname }}"
      annotations:
        external-dns.alpha.kubernetes.io/hostname: "{{ appdomain }}"
        external-dns.alpha.kubernetes.io/ttl: "1"
        external-dns.alpha.kubernetes.io/cloudflare-proxied: "false"
    spec:
      ports:
        - name: http
          port: 80
          protocol: TCP
          targetPort: 80
      selector:
        app: "{{ appname }}"
      type: LoadBalancer
      # if type: LoadBalancer is enabled than comment out INGRESS section below
    EOF

    # INGRESS
    # cat << 'EOF' | kubectl apply -f -
    # kind: Ingress
    # apiVersion: networking.k8s.io/v1
    # metadata:
    #   name: "{{ appname }}"
    #   namespace: "{{ appname }}"
    #   annotations:
    #     kubernetes.io/ingress.class: traefik
    #     cert-manager.io/cluster-issuer: letsencrypt-staging
    #     traefik.ingress.kubernetes.io/router.middlewares: default-my-basic-auth@kubernetescrd
    # spec:
    #   tls:
    #     - secretName: "{{ appname }}"-home-local-tls
    #       hosts:
    #         - "{{ appdomain }}"
    #   rules:
    #   - host: "{{ appdomain }}" 
    #     http:
    #       paths:
    #         - path: /
    #           pathType: Prefix
    #           backend:
    #             service:
    #               name: "{{ appname }}"
    #               port:
    #                 number: 80
    #EOF

# need to run grep with a shell command and check the .stdout for content
# The lineinfile module ensures the line as defined in line is present in the file and the line is identified by your regexp. 
# So no matter what value your setting already has, it will be overridden by your new line.
# - name: Test line "192.168.0.161 "{{ appname }}" "{{ appdomain }}"" in /etc/hosts
#   shell: grep -c "^192.168.0.161 "{{ appname }}" "{{ appdomain }}"" /etc/hosts || true
#   register: test_traefik_existing_in_hosts

# And then apply the condition to your lineinfile task:
# - name: add "{{ appdomain }}" to hosts file 
#   lineinfile:
#     path: /etc/hosts
#     line: 192.168.0.161 "{{ appname }}" "{{ appdomain }}"
#     backup: true
#   when: test_traefik_existing_in_hosts.stdout == "0"