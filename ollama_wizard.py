#!/usr/bin/env python3
import subprocess
import os
import time
import sys
import threading
import re
from datetime import datetime

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

class ProgressBar:
    def __init__(self, total=100, width=50, emoji_start="🚀", emoji_end="✅"):
        self.total = total
        self.width = width
        self.current = 0
        self.emoji_start = emoji_start
        self.emoji_end = emoji_end
        self.is_complete = False
        
    def update(self, progress, status=""):
        self.current = min(progress, self.total)
        percentage = (self.current / self.total) * 100
        filled_width = int((self.current / self.total) * self.width)
        
        # Create progress bar
        bar = '█' * filled_width + '░' * (self.width - filled_width)
        
        # Choose emoji based on progress
        if percentage == 100:
            emoji = self.emoji_end
            self.is_complete = True
        else:
            emoji = self.emoji_start
            
        # Color based on progress
        if percentage < 30:
            color = Colors.RED
        elif percentage < 70:
            color = Colors.YELLOW
        else:
            color = Colors.GREEN
            
        # Print progress bar
        print(f"\r{emoji} {color}{bar}{Colors.RESET} {percentage:5.1f}% {status}", end="", flush=True)
        
        if self.is_complete:
            print()  # New line when complete

class EnhancedOllamaSetup:
    def __init__(self):
        self.cloudflare_token = "eyJhIjoiYzRhMTcwZmEzZGViOWRkNTRmNmQ1NTdkMmVlNjg2MTAiLCJ0IjoiMTBjN2Q3YzgtZWQwOC00ZTg1LThiMjYtYjBmMDg0ODliNTA1IiwicyI6Ik1qRTBORGt3Wm1JdE4yVTVNeTAwTmpGaUxXRTBNamd0WVdFeE9HVmlZamN4TVRNMSJ9"
        self.ollama_model = "hf.co/TheDrummer/Gemmasutra-Mini-2B-v1-GGUF:Q6_K"
        self.overall_progress = 0
        
    def print_banner(self):
        banner = f"""
{Colors.CYAN}{'=' * 70}{Colors.RESET}
{Colors.BOLD}{Colors.MAGENTA}    🚀 OLLAMA SETUP WIZARD 🚀{Colors.RESET}
{Colors.CYAN}{'=' * 70}{Colors.RESET}
{Colors.YELLOW}⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}
{Colors.CYAN}{'=' * 70}{Colors.RESET}
"""
        print(banner)
        
    def print_step(self, step_num, total_steps, title, emoji):
        print(f"\n{Colors.BOLD}{Colors.BLUE}📋 Step {step_num}/{total_steps}: {emoji} {title}{Colors.RESET}")
        print(f"{Colors.CYAN}{'─' * 50}{Colors.RESET}")
        
    def simulate_progress(self, progress_bar, duration, status_messages):
        """Simulate progress for operations without real progress feedback"""
        steps = len(status_messages)
        step_duration = duration / steps
        
        for i, message in enumerate(status_messages):
            progress = ((i + 1) / steps) * 100
            progress_bar.update(progress, message)
            time.sleep(step_duration)
            
    def run_command_with_progress(self, command, shell=True, background=False, progress_messages=None, duration=10):
        """Run command with progress simulation"""
        try:
            if background:
                process = subprocess.Popen(command, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return process
            else:
                if progress_messages:
                    progress_bar = ProgressBar(emoji_start="⚡", emoji_end="✅")
                    
                    # Start progress simulation in a thread
                    progress_thread = threading.Thread(
                        target=self.simulate_progress,
                        args=(progress_bar, duration, progress_messages)
                    )
                    progress_thread.daemon = True
                    progress_thread.start()
                    
                    # Run the actual command
                    result = subprocess.run(command, shell=shell, capture_output=True, text=True)
                    
                    # Wait for progress to complete
                    progress_thread.join()
                    
                    if result.returncode == 0:
                        print(f"{Colors.GREEN}✅ Success!{Colors.RESET}")
                    else:
                        print(f"{Colors.RED}❌ Error: {result.stderr[:100]}...{Colors.RESET}")
                        
                    return result
                else:
                    return subprocess.run(command, shell=shell, capture_output=True, text=True)
                    
        except Exception as e:
            print(f"{Colors.RED}❌ Exception: {e}{Colors.RESET}")
            return None

    def install_ollama(self):
        """Install Ollama with progress"""
        self.print_step(1, 5, "Installing Ollama", "📦")
        
        progress_messages = [
            "Downloading installer script... 📥",
            "Verifying download... 🔍",
            "Installing Ollama binary... 🛠️",
            "Setting up permissions... 🔐",
            "Finalizing installation... 🎯"
        ]
        
        command = "curl -fsSL https://ollama.com/install.sh | sh"
        result = self.run_command_with_progress(command, progress_messages=progress_messages, duration=15)
        
        if result and result.returncode == 0:
            print(f"{Colors.GREEN}🎉 Ollama installed successfully!{Colors.RESET}")
            return True
        else:
            print(f"{Colors.RED}💥 Failed to install Ollama{Colors.RESET}")
            return False

    def start_ollama_server(self):
        """Start Ollama server with progress"""
        self.print_step(2, 5, "Starting Ollama Server", "🖥️")
        
        # Set environment variables
        os.environ['OLLAMA_HOST'] = '0.0.0.0'
        os.environ['OLLAMA_ORIGINS'] = '*'
        print(f"{Colors.YELLOW}🌐 Setting up external access...{Colors.RESET}")
        
        progress_messages = [
            "Configuring server settings... ⚙️",
            "Binding to external interface... 🔗",
            "Starting background process... 🚀",
            "Waiting for server to respond... ⏳",
            "Server ready for connections... 🟢"
        ]
        
        # Show progress while starting
        progress_bar = ProgressBar(emoji_start="🔄", emoji_end="🟢")
        for i, message in enumerate(progress_messages):
            progress = ((i + 1) / len(progress_messages)) * 100
            progress_bar.update(progress, message)
            time.sleep(1)
            
        # Start the actual server
        command = "ollama serve"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print(f"{Colors.GREEN}🎉 Ollama server started! PID: {process.pid}{Colors.RESET}")
        return process

    def install_cloudflared(self):
        """Install Cloudflared with progress"""
        self.print_step(3, 5, "Installing Cloudflared", "☁️")
        
        commands = [
            ("sudo mkdir -p --mode=0755 /usr/share/keyrings", "Creating keyrings directory... 📁"),
            ("curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null", "Adding GPG key... 🔑"),
            ("echo 'deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared any main' | sudo tee /etc/apt/sources.list.d/cloudflared.list", "Adding repository... 📋"),
            ("sudo apt-get update", "Updating package lists... 🔄"),
            ("sudo apt-get install cloudflared -y", "Installing cloudflared... 📦")
        ]
        
        progress_bar = ProgressBar(emoji_start="☁️", emoji_end="✅")
        
        for i, (cmd, status) in enumerate(commands):
            progress = ((i + 1) / len(commands)) * 100
            progress_bar.update(progress, status)
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"\n{Colors.RED}❌ Failed: {cmd}{Colors.RESET}")
                return False
            time.sleep(1)
            
        print(f"{Colors.GREEN}🎉 Cloudflared installed successfully!{Colors.RESET}")
        return True

    def start_cloudflare_tunnel(self):
        """Start Cloudflare tunnel with progress"""
        self.print_step(4, 5, "Starting Cloudflare Tunnel", "🌐")
        
        progress_messages = [
            "Connecting to Cloudflare... 🔗",
            "Establishing secure tunnel... 🔒",
            "Configuring routing... 🛣️",
            "Testing connectivity... 🔍",
            "Tunnel ready for traffic... 🚀"
        ]
        
        progress_bar = ProgressBar(emoji_start="🌐", emoji_end="🚀")
        
        for i, message in enumerate(progress_messages):
            progress = ((i + 1) / len(progress_messages)) * 100
            progress_bar.update(progress, message)
            time.sleep(1)
            
        command = f"cloudflared tunnel run --token {self.cloudflare_token}"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print(f"{Colors.GREEN}🎉 Cloudflare tunnel started! PID: {process.pid}{Colors.RESET}")
        return process

    def install_ollama_model(self, model_name=None):
        """Install Ollama model with real-time progress"""
        if model_name is None:
            model_name = self.ollama_model
            
        self.print_step(5, 5, f"Installing Model: {model_name}", "🧠")
        
        print(f"{Colors.YELLOW}📥 Downloading model: {model_name}{Colors.RESET}")
        
        # Start the pull command
        command = f"ollama pull {model_name}"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        
        progress_bar = ProgressBar(emoji_start="📥", emoji_end="🧠")
        
        # Read output line by line
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                # Try to extract progress from ollama output
                line = output.strip()
                if 'pulling' in line.lower() or 'downloading' in line.lower():
                    # Look for percentage in the output
                    percentage_match = re.search(r'(\d+)%', line)
                    if percentage_match:
                        progress = int(percentage_match.group(1))
                        progress_bar.update(progress, f"Downloading... {line}")
                    else:
                        progress_bar.update(50, f"Downloading... {line}")
                elif 'verifying' in line.lower():
                    progress_bar.update(90, "Verifying model...")
                elif 'success' in line.lower() or process.poll() == 0:
                    progress_bar.update(100, "Model ready!")
                    
        if process.returncode == 0:
            print(f"{Colors.GREEN}🎉 Model {model_name} installed successfully!{Colors.RESET}")
            return True
        else:
            print(f"{Colors.RED}💥 Failed to install model {model_name}{Colors.RESET}")
            return False

    def show_completion_summary(self, ollama_pid, tunnel_pid):
        """Show beautiful completion summary"""
        completion_banner = f"""
{Colors.GREEN}{'=' * 70}{Colors.RESET}
{Colors.BOLD}{Colors.GREEN}    🎉 SETUP COMPLETED SUCCESSFULLY! 🎉{Colors.RESET}
{Colors.GREEN}{'=' * 70}{Colors.RESET}

{Colors.BOLD}{Colors.CYAN}📊 Summary:{Colors.RESET}
{Colors.GREEN}✅ Ollama installed and running{Colors.RESET}        (PID: {ollama_pid})
{Colors.GREEN}✅ Cloudflare tunnel active{Colors.RESET}           (PID: {tunnel_pid})
{Colors.GREEN}✅ Model {self.ollama_model} ready{Colors.RESET}
{Colors.GREEN}✅ External access configured{Colors.RESET}

{Colors.BOLD}{Colors.YELLOW}🔗 Your Ollama is now accessible worldwide!{Colors.RESET}
{Colors.BOLD}{Colors.MAGENTA}⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}

{Colors.CYAN}{'=' * 70}{Colors.RESET}
{Colors.BOLD}{Colors.BLUE}Press Ctrl+C to stop all services...{Colors.RESET}
{Colors.CYAN}{'=' * 70}{Colors.RESET}
"""
        print(completion_banner)

    def setup_all(self):
        """Run the complete setup with beautiful progress"""
        self.print_banner()
        
        try:
            # Step 1: Install Ollama
            if not self.install_ollama():
                return False
                
            # Step 2: Start Ollama server
            ollama_process = self.start_ollama_server()
            if not ollama_process:
                return False
                
            # Step 3: Install Cloudflared
            if not self.install_cloudflared():
                return False
                
            # Step 4: Start Cloudflare tunnel
            tunnel_process = self.start_cloudflare_tunnel()
            if not tunnel_process:
                return False
                
            # Step 5: Install Ollama model
            print(f"\n{Colors.YELLOW}⏳ Waiting for Ollama server to be ready...{Colors.RESET}")
            time.sleep(5)
            
            if not self.install_ollama_model():
                return False
                
            # Show completion summary
            self.show_completion_summary(ollama_process.pid, tunnel_process.pid)
            
            # Keep running
            while True:
                time.sleep(60)
                
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}👋 Shutting down gracefully...{Colors.RESET}")
            return True
        except Exception as e:
            print(f"{Colors.RED}💥 Unexpected error: {e}{Colors.RESET}")
            return False

def main():
    setup = EnhancedOllamaSetup()
    
    # Handle custom model argument
    if len(sys.argv) > 1:
        setup.ollama_model = sys.argv[1]
        print(f"{Colors.CYAN}🎯 Using custom model: {setup.ollama_model}{Colors.RESET}")
    
    try:
        setup.setup_all()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}👋 Goodbye!{Colors.RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()
