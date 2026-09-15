def run_task2():
    print("\n--- Завдання 2 ---")

    users = {
        "forensic_lead": {"role": "forensic_analyst", "clearance": 4, "department": "Forensics", "active": True},
        "compliance_off": {"role": "compliance_officer", "clearance": 3, "department": "Compliance", "active": True},
        "trainee_sec": {"role": "trainee", "clearance": 1, "department": "Training", "active": True},
        "vendor_tech": {"role": "vendor_support", "clearance": 2, "department": "Vendor", "active": True},
        "archived_usr": {"role": "archived", "clearance": 1, "department": "Archive", "active": False}
    }

    resources = [("forensic_images", 4), ("compliance_reports", 3), ("training_videos", 1), ("vendor_tools", 2),
                 ("evidence_locker", 4), ("certification_docs", 1), ("audit_findings", 3), ("chain_of_custody", 4),
                 ("support_tickets", 2), ("learning_modules", 1)]
    security_levels = ("Basic", "Standard", "Protected", "Maximum")
    blocked_users = {"archived_usr", "terminated_vendor", "security_breach"}

    print("Ресурси системи:")
    for res, lvl in resources:
        print(f"- {res}: {security_levels[lvl - 1]}")

    print("\nПеревірка доступу:")
    for username, user_info in users.items():
        for res, lvl in resources:
            if username in blocked_users:
                print(f"user={username} resource={res} -> DENY (User is blocked)")
            elif not user_info["active"]:
                print(f"user={username} resource={res} -> DENY (Account inactive)")
            elif user_info["clearance"] >= lvl:
                print(f"user={username} resource={res} -> ALLOW")
            else:
                print(f"user={username} resource={res} -> DENY (Insufficient clearance)")


if __name__ == "__main__":
    run_task2()
