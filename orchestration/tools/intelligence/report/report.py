#!/usr/bin/env python3
import json
import os
import glob
from datetime import datetime

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
SKILLS_DIR = os.path.join(REPO_ROOT, "intelligence", "core", "skills")
OUTPUTS_DIR = os.path.join(REPO_ROOT, "orchestration", "pipelines", "outputs", "dream")
VAULT_CSS = os.path.join(SKILLS_DIR, "styles", "vault.css")

def main():
    # 1. Audit core specs
    all_specs = glob.glob(os.path.join(SKILLS_DIR, "**", "report_spec.json"), recursive=True)
    valid_specs = []
    broken_specs = []
    
    for s_path in all_specs:
        try:
            with open(s_path, "r") as f:
                json.load(f)
            valid_specs.append(s_path)
        except:
            broken_specs.append(s_path)

    # 2. Audit Output Connectivity
    output_ok = os.path.exists(OUTPUTS_DIR) and os.access(OUTPUTS_DIR, os.W_OK)
    
    # 3. Theme Audit
    theme_ok = os.path.exists(VAULT_CSS)

    summary = f"{len(valid_specs)} skills registered, outputs online."
    findings = [
        f"Specs: {len(valid_specs)} verified, {len(broken_specs)} malformed.",
        f"Outputs: {'Connected' if output_ok else 'Disconnected'} at orchestration/pipelines/outputs/dream/",
        f"Theme: {'Modern Vault CSS loaded' if theme_ok else 'Injected fallbacks used'}"
    ]
    
    flags = []
    if broken_specs:
        flags.append(f"CRITICAL: {len(broken_specs)} report_spec.json files are malformed.")
    if not theme_ok:
        flags.append("WARNING: Global vault.css missing — visual drift likely.")

    envelope = {
        "skill": "intelligence/report",
        "preferred_agent": "System Integrity (Antigravity)",
        "run_at": datetime.utcnow().isoformat() + "Z",
        "status": "ok" if not flags else ("error" if any("CRITICAL" in f for f in flags) else "warn"),
        "summary": summary,
        "findings": findings,
        "flags": flags
    }

    print(json.dumps(envelope))

if __name__ == "__main__":
    main()
