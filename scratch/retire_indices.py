import os

RENAMES = [
    "intelligence/casebook/index.md",
    "intelligence/casebook/reporting/index.md",
    "intelligence/product/index.md",
    "intelligence/product/shareout/q2/index.md",
    "intelligence/product/projects/q2/index.md",
    "intelligence/product/projects/q2/notes-locked-notes/index.md",
    "intelligence/product/projects/q2/enrollment-dialog-bulk-services-section/index.md",
    "intelligence/product/projects/q2/integrations-zapier-improvements/index.md",
    "intelligence/product/projects/q2/notes-bulk-service-notes/index.md",
    "intelligence/product/projects/q2/notes-bulk-general-notes/index.md",
    "intelligence/product/projects/q2/portal-client-dashboard/index.md",
    "intelligence/product/projects/q2/notes-notes-datagrid/index.md",
    "intelligence/product/projects/q2/services-multiple-rosters-for-enrollments-and-notes/index.md",
    "intelligence/product/projects/q2/notes-signing-service-note-locking/index.md",
    "intelligence/product/projects/q2/services-service-plan-datagrid-with-bulk-actions/index.md",
    "intelligence/product/projects/q2/data-import-bulk-import-for-notes/index.md",
    "intelligence/product/projects/q2/services-wlv-bulk-actions/index.md",
    "skills/handoff/index.md",
    "skills/status/index.md",
    "skills/dream/index.md",
    "skills/tasks/index.md",
    "skills/asana/index.md",
    "skills/rovo/index.md",
    "skills/styles/index.md",
]

# Root index.md to keep
KEEP = ["./index.md"]

def main():
    # Execute renames
    for rel_path in RENAMES:
        abs_path = os.path.abspath(rel_path)
        if os.path.exists(abs_path):
            new_path = abs_path.replace("index.md", "overview.md")
            print(f"Renaming {rel_path} -> {os.path.basename(new_path)}")
            os.rename(abs_path, new_path)
        else:
            print(f"Skip (not found): {rel_path}")

    # Bulk delete remaining index.md files (except root)
    for root, dirs, files in os.walk("."):
        if "node_modules" in root or ".git" in root or "dist" in root:
            continue
        for file in files:
            if file == "index.md":
                rel_file = os.path.join(root, file)
                if rel_file in KEEP:
                    print(f"Keeping {rel_file}")
                    continue
                abs_file = os.path.abspath(rel_file)
                print(f"Deleting {rel_file}")
                os.remove(abs_file)

if __name__ == "__main__":
    main()
