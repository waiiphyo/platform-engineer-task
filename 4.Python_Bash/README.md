# 4. Python &amp; Bash Scripting
## 4.1 Kubernetes Config Validation Tool

This Python CLI tool validates Kubernetes YAML manifests in a specified directory. It ensures each file has the required `apiVersion`, `kind`, and `metadata.name` fields. Add new for test

---

### Features
- Validates all `.yaml` and `.yml` files in a given directory.
- Supports multi-document YAML files.
- Outputs validation results in structured JSON format.

### How to Run
``` bash
python3 -m venv venv
source venv/bin/activate
pip install pyyaml
python yaml-validate.py  /path/to/yaml/files
```
### Testing Example Output (valid files)
```
(venv) ➜  4.Python_Bash python yaml-validate.py ../1.Kubernetes_Mastery 
```
```json
{
  "message": "All YAML files are valid!"
}
```
### Update the file for Example Output (With issues)
```bash
(venv) ➜  4.Python_Bash python yaml-validate.py ../1.Kubernetes_Mastery    
```
```json
{
  "validation_issues": [
    {
      "file": "../1.Kubernetes_Mastery/1.1.Pod_Scheduling.yaml",
      "error": "YAML parse error: mapping values are not allowed here\n  in \"../1.Kubernetes_Mastery/1.1.Pod_Scheduling.yaml\", line 2, column 6"
    }
  ]
}
```
## 4.2 CrashLoopBackOff Triage Script
This Bash script lists all pods across **all namespaces** that are in the `CrashLoopBackOff` state. For each affected pod, it prints:

- Pod Name
- Namespace
- Container Image
- Last 10 log lines

This is useful for platform engineers or SREs troubleshooting pod startup issues.

---
### Files

- `check.sh`: Bash script to detect CrashLoopBackOff pods and extract logs.
- `clp.yaml`: Sample pod definition to simulate a CrashLoopBackOff condition using `busybox`.

---

### Testing
#### Deploy a CrashLoopBackOff Pod
```bash
kubectl apply -f clp.yaml
```
The container will print "Simulating error..." 20 times and exit with an error, triggering a CrashLoopBackOff loop.

#### Run the Script
```bash
chmod +x check.sh
./check.sh
```
#### When the pod is not in CrashLoopBackOff:
```bash
Checking for pods in CrashLoopBackOff state across all namespaces...

No pods found in CrashLoopBackOff state.
```
#### When the pod is in CrashLoopBackOff:
```bash
 Checking for pods in CrashLoopBackOff state across all namespaces...

Pod: crashloop-logger
Namespace: default
Image: busybox
Last 10 log lines:
Simulating error...
Simulating error...
Simulating error...
Simulating error...
Simulating error...
Simulating error...
Simulating error...
Simulating error...
Simulating error...
Simulating error...
------------------------------
```
- The script filters only pods in Running phase with containers specifically in CrashLoopBackOff state.
- Only the first container in the pod is assumed when retrieving logs and image.
