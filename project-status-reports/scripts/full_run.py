import subprocess
import os

REPO_ROOT = "/Users/benbelanger/GitHub/ben-cp/project-status-reports"
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")

def run_script(script_name, capture_output, *args):
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    cmd = ["python3", script_path] + list(args)
    
    try:
        if capture_output:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout
        else:
            subprocess.run(cmd, check=True)
            return None
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_name}")
        if e.stdout: print(e.stdout)
        if e.stderr: print(e.stderr)
        raise

def main():
    print("=== Platform Weekly Status: Full Run Pipeline ===")
    
    # Reset manifest and archive
    run_script("update_manifest.py", True, "reset")
    print("✅ Initialization: Manifest Reset & Archive Complete")
    
    # Run pipeline steps
    run_script("step_1_asana_platform_filter.py", True)
    run_script("update_manifest.py", True, "1_asana_ingest", "complete")
    print("✅ Step 1: Asana Ingest Complete")
    
    run_script("step_2_rovo_context.py", True)
    run_script("update_manifest.py", True, "2_rovo_context", "complete")
    print("✅ Step 2: Rovo Context Complete")
    
    run_script("step_3_jira_harvest.py", True)
    run_script("update_manifest.py", True, "3_jira_harvest", "complete")
    print("✅ Step 3: Jira Harvest Complete")
    
    # Step 4: Full output required for Report Extraction
    print("🚀 Step 4: Generating Final Report...")
    report_output = run_script("step_4_report_generator.py", True)
    print(report_output)
    
    run_script("update_manifest.py", True, "4_report_generation", "complete")
    
    print("\nRelay Success: Pipeline Complete. Use the tags above to extract the report.")

if __name__ == "__main__":
    main()
