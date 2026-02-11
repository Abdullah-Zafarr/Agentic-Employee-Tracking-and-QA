import os
import sys
import subprocess
from datetime import datetime, timedelta
from pytz import timezone

def run_script(script_name, args=None):
    cmd = [sys.executable, script_name]
    if args:
        cmd.extend(args)
    
    print(f"\n>>> Running {script_name}...")
    try:
        subprocess.run(cmd, check=True)
        print(f">>> Completed {script_name}")
    except subprocess.CalledProcessError as e:
        print(f">>> Error in {script_name}: {e}")
        sys.exit(1)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Monday.com & OpenPhone AI Integration Pipeline")
    parser.add_argument("--days", type=int, default=16, help="Days offset for processing (default: 16)")
    parser.add_argument("--quick", action="store_true", help="Run a quick pipeline (skips some steps)")
    args = parser.parse_args()

    offset_str = str(args.days)
    
    # Define the full pipeline
    pipeline = [
        ("01_reference_collecter.py", []),
        ("02.py", []),
        ("03_notes_cleaner.py", [offset_str]),
        ("04_call_logs_retriever.py", []),
        ("05_call_ids_retriever.py", []),
        ("06_call_logs_ids_combiner.py", [offset_str]),
        ("07_call_transcript_retriever.py", []),
        ("08_call_transcript_cleaner.py", []),
        ("09_calls_notes_combiner.py", []),
        ("10_ai_1_transcript_analyzer.py", []),
        ("10_ai_2_start.py", []),
        ("10_ai_3_end.py", []),
        ("10_ai_4_service.py", []),
        ("10_ai_5_bills.py", []),
        ("10_ai_6_columns.py", []),
        ("11_CST_to_UTC.py", []),
        ("12_1_groups_columns_fetcher.py", []),
        ("12_2_units.py", []),
        ("13.py", []),
        ("14_hired_units.py", []),
        ("14_units_monday.py", [offset_str]),
        ("remover.py", []),
    ]

    if args.quick:
        # Define quick pipeline if needed, for now just run everything
        pass

    for script, script_args in pipeline:
        if os.path.exists(script):
            run_script(script, script_args)
        else:
            print(f"Warning: Script {script} not found, skipping.")

if __name__ == "__main__":
    main()
