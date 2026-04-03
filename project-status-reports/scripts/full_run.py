import subprocess
import os

REPO_ROOT = "/Users/benbelanger/GitHub/ben-cp/project-status-reports"
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")

def run_script(script_name, *args):
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    cmd = ["python3", script_path] + list(args)
    print(f"🚀 Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def main():
    print("=== Platform Weekly Status: Full Run Pipeline ===")
    
    # Reset manifest and archive
    run_script("update_manifest.py", "reset")
    
    # Run pipeline steps
    run_script("step_1_asana_platform_filter.py")
    run_script("update_manifest.py", "1_asana_ingest", "complete")
    
    run_script("step_2_rovo_context.py")
    run_script("update_manifest.py", "2_rovo_context", "complete")
    
    run_script("step_3_jira_harvest.py")
    run_script("update_manifest.py", "3_jira_harvest", "complete")
    
    run_script("step_4_report_generator.py")
    run_script("update_manifest.py", "4_report_generation", "complete")
    
    print("✅ Full Run Pipeline Finished Successfully!")

if __name__ == "__main__":
    main()
