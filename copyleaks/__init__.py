import sys
if sys.stderr.isatty():
    yellow = "\033[33m"
    red = "\033[31m"
    reset = "\033[0m"
else:
    yellow = ""
    red = ""
    reset = ""
notice = (
    f"{yellow}"
    "================================================================\n"
    f"{red} DEPRECATION NOTICE: copyleaks\n"
    f"{yellow}================================================================\n"
    "AI Code Detection will be discontinued on August 29, 2025.\n"
    "Please remove AI code detection integrations before the sunset date.\n"
    f"================================================================{reset}"
)
print(notice, file=sys.stderr)
