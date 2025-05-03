#!/usr/bin/env python3

import argparse
import os
import yaml
import json
from pathlib import Path

REQUIRED_FIELDS = ["apiVersion", "kind", "metadata"]

def validate_manifest(file_path):
    issues = []
    with open(file_path, 'r') as f:
        try:
            documents = list(yaml.safe_load_all(f))
        except yaml.YAMLError as e:
            issues.append({
                "file": str(file_path),
                "error": f"YAML parse error: {str(e)}"
            })
            return issues

        for i, doc in enumerate(documents):
            if not isinstance(doc, dict):
                issues.append({
                    "file": str(file_path),
                    "document": i + 1,
                    "error": "Document is not a valid YAML object"
                })
                continue

            for field in REQUIRED_FIELDS:
                if field not in doc:
                    issues.append({
                        "file": str(file_path),
                        "document": i + 1,
                        "error": f"Missing required field: {field}"
                    })

            if "metadata" in doc and not doc["metadata"].get("name"):
                issues.append({
                    "file": str(file_path),
                    "document": i + 1,
                    "error": "Missing metadata.name"
                })

    return issues

def validate_directory(directory):
    all_issues = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".yaml", ".yml")):
                file_path = os.path.join(root, file)
                all_issues.extend(validate_manifest(file_path))
    return all_issues

def main():
    parser = argparse.ArgumentParser(description="Validate Kubernetes YAML manifests")
    parser.add_argument("directory", help="Directory containing YAML files")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(json.dumps({"error": f"Directory not found: {args.directory}"}))
        return

    issues = validate_directory(args.directory)
    if issues:
        print(json.dumps({"validation_issues": issues}, indent=2))
    else:
        print(json.dumps({"message": "All YAML files are valid!"}, indent=2))

if __name__ == "__main__":
    main()

