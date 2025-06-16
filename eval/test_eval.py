import subprocess
import os
from dotenv import load_dotenv

# --- Configuration ---
# Correct path to the agent module DIRECTORY
AGENT_MODULE_PATH = "data_science" 
EVAL_CONFIGS = {
    "Orchestrator Routing": "eval/test_configs/config_routing.json",
    "BQML Agent Skills": "eval/test_configs/config_bqml.json",
    "End-to-End Plotting": "eval/test_configs/config_e2e_plot.json",
}

def run_evaluation(suite_name: str, config_path: str):
    """Runs a single ADK evaluation suite using the correct CLI syntax."""
    print("="*80)
    print(f"🔬 Running Evaluation Suite: {suite_name}")
    print("="*80)

    # This is the corrected command structure based on the ADK documentation.
    # 'AGENT_MODULE_PATH' is now a positional argument.
    # '--config_file_path' is the correct flag for the config file.
    command = [
        "adk", "eval",
        AGENT_MODULE_PATH,
        f"--config_file_path={config_path}"
    ]

    try:
        # The environment variables loaded by load_dotenv() are automatically
        # inherited by the subprocess.
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("✅ Suite completed successfully!")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Suite failed for {suite_name}!")
        print(f"Return Code: {e.returncode}")
        print("\n--- STDOUT ---")
        print(e.stdout)
        print("\n--- STDERR ---")
        print(e.stderr)
    except FileNotFoundError:
        print("❌ Error: 'adk' command not found. Make sure you are in the correct poetry environment.")
    print("\n\n")


if __name__ == "__main__":
    # Load variables from the .env file at the project root
    load_dotenv() 
    
    if not os.environ.get("WANDB_API_KEY") or not os.environ.get("WANDB_PROJECT_ID"):
        print("🛑 Error: WANDB_API_KEY and WANDB_PROJECT_ID environment variables must be set in your .env file.")
    else:
        print("🚀 Starting Data Science Agent Evaluation Pipeline...")
        for name, config in EVAL_CONFIGS.items():
            run_evaluation(name, config)
        print("🎉 Evaluation Pipeline Finished.")