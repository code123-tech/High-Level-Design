import subprocess
import time
import sys
from colorama import init, Fore

init(autoreset=True)

def run_script(script_name: str, wait: bool = True):
    """Run a Python script as a subprocess"""
    print(f"{Fore.CYAN}Starting {script_name}...")
    
    try:
        process = subprocess.Popen([sys.executable, script_name])
        if wait:
            process.wait()
        return process
    except Exception as e:
        print(f"{Fore.RED}Error running {script_name}: {str(e)}")
        return None

def main():
    print(f"{Fore.YELLOW}Starting Kafka Partitioning Demo...")
    
    # First create the topic
    print(f"\n{Fore.GREEN}Step 1: Creating Kafka Topic")
    run_script("topic_manager.py")
    
    # Start the consumer group (in background)
    print(f"\n{Fore.GREEN}Step 2: Starting Consumer Group")
    consumer_process = run_script("consumer.py", wait=False)
    
    # Wait a bit for consumers to start up
    time.sleep(3)
    
    # Run the producer
    print(f"\n{Fore.GREEN}Step 3: Running Producer Demo")
    run_script("producer.py")
    
    print(f"\n{Fore.YELLOW}Demo complete! Press Ctrl+C to stop the consumers...")
    
    try:
        # Keep the script running until Ctrl+C
        consumer_process.wait()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Stopping consumers...")
        if consumer_process:
            consumer_process.terminate()
            consumer_process.wait()
    
    print(f"{Fore.GREEN}Demo finished!")

if __name__ == "__main__":
    main()
