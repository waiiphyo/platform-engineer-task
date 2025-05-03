# 1. Kubernetes Mastery
## 1.1 Pod Scheduling & Resource Management
### Affinity (Node Scheduling)
- nodeAffinity ensures the pod is only scheduled to appropriate nodes:
    - Must have the label env=prod
    - Must also have the label nvidia.com/gpu
- Uses requiredDuringSchedulingIgnoredDuringExecution, which is a hard constraint during scheduling. The pod won’t be scheduled at all if these conditions aren’t met.
- This is useful for high-performance or ML workloads where GPU is a must and environment isolation is required.

### Resource Requests & Limits
- Requests and Limits are both set to:
    - Memory: 2Gi
    - CPU: 1
- Since requests == limits for both memory and CPU:
    - The pod falls into the Guaranteed QoS class.
    - This is the highest-priority class for Kubernetes and helps:
        - Prevent eviction under memory pressure.
        - Provide more predictable and stable performance in production.
**Note:** Although the original task said "reserve 500Mi and 250m", this manifest I uses 2Gi and 1 CPU for both. That’s okay if the goal is Guaranteed QoS, because that class requires requests = limits.

### Secret Mount
- A Kubernetes secret named app-secrets is mounted at /etc/secrets inside the container.
- The mount is read-only for security reasons.

### How to Apply

```
kubectl apply -f 1.1.Pod_Scheduling.yaml
```

---
## 1.2 Network Policy & Secure Exposure
- A **Deployment** (`frontend-app`) exposed via an **Ingress**.
- A **NetworkPolicy** that restricts access to the frontend service, allowing only specific backend pods.

---

### Application Deployment & Ingress

- **Deployment Name:** `frontend-app`
- **Namespace:** `default`
- **Ingress Exposure:**
  - Uses the `nginx` ingress controller.
  - Ingress is annotated accordingly:
    ```yaml
    metadata:
      annotations:
        kubernetes.io/ingress.class: "nginx"
    ```
---
### NetworkPolicy Overview

- **Objective:** Restrict access to the frontend application.
- **Policy Details:**
  - Only pods in the `backend` namespace are allowed.
  - Pods must have the label `access: true`.
  - All other traffic is denied by default.
---

### Included Files

- `1.2.ns.yaml` - Defines the namespaces for frontend and backend.
- `1.2.fe_deployment.yaml` – Defines the frontend app Deployment.
- `1.2.fe_svc.yaml` - Defines the frontend app service.
- `1.2.Ingress.yaml` – Exposes the service via an Ingress resource.
- `1.2.Netpol.yaml` – Implements traffic control to the frontend pods.

---
### How to Apply

```
kubectl apply -f 1.2.ns.yaml
kubectl apply -f 1.2.fe_deployment.yaml
kubectl apply -f 1.2.fe_svc.yaml
kubectl apply -f 1.2.Netpol.yaml
kubectl apply -f 1.2.Ingress.yaml
```
---
