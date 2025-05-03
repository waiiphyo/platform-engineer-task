#!/bin/bash

echo " Checking for pods in CrashLoopBackOff state across all namespaces..."
echo

pods=$(kubectl get pods --all-namespaces --field-selector status.phase=Running -o json \
  | jq -r '
    .items[] 
    | select(
        .status.containerStatuses[]? 
        | .state.waiting?.reason == "CrashLoopBackOff"
      )
    | [.metadata.name, .metadata.namespace] 
    | @tsv'
)

if [ -z "$pods" ]; then
  echo "No pods found in CrashLoopBackOff state."
  exit 0
fi

# Process each pod
while IFS=$'\t' read -r pod namespace; do
  echo "Pod: $pod"
  echo "Namespace: $namespace"

  # Get the image (first container assumed)
  image=$(kubectl get pod "$pod" -n "$namespace" -o jsonpath="{.spec.containers[0].image}")
  echo "Image: $image"

  echo "Last 10 log lines:"
  kubectl logs "$pod" -n "$namespace" --tail=10 2>/dev/null || echo "⚠️ Failed to fetch logs"

  echo "------------------------------"
done <<< "$pods"

