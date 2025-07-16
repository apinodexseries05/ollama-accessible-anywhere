#!/usr/bin/env python3
import subprocess
import os
import time
import sys
import threading
import re
from datetime import datetime
import asyncio
import concurrent.futures
from queue import Queue

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

class FastProgressBar:
    def __init__(self, total=100, width=30, emoji_start="🚀", emoji_end="✅"):
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

        bar = '█' * filled_width + '░' * (self.width - filled_width)
        emoji = self.emoji_end if percentage == 100 else self.emoji_start
        
        color = Colors.RED if percentage < 50 else Colors.YELLOW if percentage < 90 else Colors.GREEN
        print(f"\r{emoji} {color}{bar}{Colors.RESET} {percentage:5.1f}% {status}", end="", flush=True)

        if percentage == 100:
            print()
            self.is_complete = True

class SuperFastOllamaSetup:
    def __init__(self):
        self.cloudflare_token = "eyJhIjoiYzRhMTcwZmEzZGViOWRkNTRmNmQ1NTdkMmVlNjg2MTAiLCJ0IjoiMTBjN2Q3YzgtZWQwOC00ZTg1LThiMjYtYjBmMDg0ODliNTA1IiwicyI6Ik1qRTBORGt3Wm1JdE4yVTVNeTAwTmpGaUxXRTBNamd0WVdFeE9HVmlZamN4TVRNMSJ9"
        self.ollama_model = "hf.co/DavidAU/L3.1-RP-Hero-Dirty_Harry-8B-GGUF:Q6_K"
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
        self.processes = []

    def print_banner(self):
        banner = f"""
{Colors.CYAN}{'=' * 50}{Colors.RESET}
{Colors.BOLD}{Colors.MAGENTA}🚀 SUPERFAST OLLAMA SETUP 🚀{Colors.RESET}
{Colors.CYAN}{'=' * 50}{Colors.RESET}
{Colors.YELLOW}Started: {datetime.now().strftime('%H:%M:%S')}{Colors.RESET}
{Colors.CYAN}{'=' * 50}{Colors.RESET}
"""
        print(banner)

    def run_fast_command(self, command, shell=True, timeout=300):
        """Run command without artificial delays"""
        try:
            result = subprocess.run(
                command, 
                shell=shell, 
                capture_output=True, 
                text=True,
                timeout=timeout
            )
            return result
        except subprocess.TimeoutExpired:
            print(f"{Colors.RED}⏰ Command timed out: {command[:50]}...{Colors.RESET}")
            return None
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
            return None

    def install_ollama_fast(self):
        """Install Ollama without delays"""
        print(f"{Colors.BLUE}📦 Installing Ollama...{Colors.RESET}")
        
        command = "curl -fsSL https://ollama.com/install.sh | sh"
        result = self.run_fast_command(command, timeout=120)
        
        if result and result.returncode == 0:
            print(f"{Colors.GREEN}✅ Ollama installed!{Colors.RESET}")
            return True
        else:
            print(f"{Colors.RED}❌ Ollama install failed{Colors.RESET}")
            return False

    def start_ollama_server_fast(self):
        """Start Ollama server immediately"""
        print(f"{Colors.BLUE}🖥️ Starting Ollama server...{Colors.RESET}")
        
        # Set environment variables
        os.environ['OLLAMA_HOST'] = '0.0.0.0'
        os.environ['OLLAMA_ORIGINS'] = '*'
        
        # Start server in background
        command = "ollama serve"
        process = subprocess.Popen(
            command, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        
        # Quick health check
        for i in range(10):  # Max 5 seconds
            try:
                check = subprocess.run(
                    "curl -s http://localhost:11434/api/version", 
                    shell=True, 
                    capture_output=True, 
                    timeout=1
                )
                if check.returncode == 0:
                    print(f"{Colors.GREEN}✅ Ollama server ready! PID: {process.pid}{Colors.RESET}")
                    self.processes.append(process)
                    return process
            except:
                pass
            time.sleep(0.5)
        
        print(f"{Colors.GREEN}✅ Ollama server started! PID: {process.pid}{Colors.RESET}")
        self.processes.append(process)
        return process

    def install_cloudflared_fast(self):
        """Install Cloudflared with parallel commands where possible"""
        print(f"{Colors.BLUE}☁️ Installing Cloudflared...{Colors.RESET}")
        
        # Batch preparation commands
        prep_commands = [
            "rm -f /usr/local/bin/cloudflared",
            "apt-get clean",
            "mkdir -p --mode=0755 /usr/share/keyrings"
        ]
        
        # Run prep commands in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(self.run_fast_command, cmd) for cmd in prep_commands]
            concurrent.futures.wait(futures)
        
        # Sequential commands that depend on each other
        sequential_commands = [
            "curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null",
            "echo 'deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared any main' | tee /etc/apt/sources.list.d/cloudflared.list",
            "apt-get update",
            "apt-get install cloudflared -y"
        ]
        
        for cmd in sequential_commands:
            result = self.run_fast_command(cmd)
            if "install cloudflared" in cmd and (not result or result.returncode != 0):
                print(f"{Colors.RED}❌ Cloudflared install failed{Colors.RESET}")
                return False
        
        print(f"{Colors.GREEN}✅ Cloudflared installed!{Colors.RESET}")
        return True

    def start_cloudflare_tunnel_fast(self):
        """Start Cloudflare tunnel immediately"""
        print(f"{Colors.BLUE}🌐 Starting Cloudflare tunnel...{Colors.RESET}")
        
        command = f"cloudflared tunnel run --token {self.cloudflare_token}"
        process = subprocess.Popen(
            command, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        
        print(f"{Colors.GREEN}✅ Cloudflare tunnel started! PID: {process.pid}{Colors.RESET}")
        self.processes.append(process)
        return process

    def install_ollama_model_fast(self, model_name=None):
        """Install Ollama model with real-time progress"""
        if model_name is None:
            model_name = self.ollama_model
        
        print(f"{Colors.BLUE}🧠 Installing model: {model_name}...{Colors.RESET}")
        
        # Start the pull command
        command = f"ollama pull {model_name}"
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Show real-time output
        progress_bar = FastProgressBar(emoji_start="📥", emoji_end="✅")
        last_progress = 0
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                # Try to extract progress from output
                if "%" in output:
                    try:
                        progress_match = re.search(r'(\d+)%', output)
                        if progress_match:
                            progress = int(progress_match.group(1))
                            if progress > last_progress:
                                progress_bar.update(progress, "downloading...")
                                last_progress = progress
                    except:
                        pass
                
                # Show status updates
                if "pulling" in output.lower():
                    progress_bar.update(last_progress, "pulling layers...")
                elif "verifying" in output.lower():
                    progress_bar.update(90, "verifying...")
                elif "success" in output.lower():
                    progress_bar.update(100, "complete!")
        
        # Ensure we show completion
        if not progress_bar.is_complete:
            progress_bar.update(100, "complete!")
        
        rc = process.poll()
        if rc == 0:
            print(f"{Colors.GREEN}✅ Model installed successfully!{Colors.RESET}")
            return True
        else:
            print(f"{Colors.RED}❌ Model installation failed{Colors.RESET}")
            return False

    def setup_all_fast(self):
        """Run complete setup with maximum speed"""
        start_time = time.time()
        self.print_banner()
        
        try:
            # Step 1: Install Ollama
            if not self.install_ollama_fast():
                return
            
            # Step 2: Start Ollama server (non-blocking)
            ollama_process = self.start_ollama_server_fast()
            
            # Step 3: Install Cloudflared in parallel with server startup
            future_cloudflared = self.executor.submit(self.install_cloudflared_fast)
            
            # Wait for both to complete
            if not future_cloudflared.result():
                return
            
            # Step 4: Start tunnel
            tunnel_process = self.start_cloudflare_tunnel_fast()
            
            # Step 5: Install model (this is the longest step)
            if not self.install_ollama_model_fast():
                return
            
            # Show completion
            elapsed_time = time.time() - start_time
            self.show_completion_summary(ollama_process.pid, tunnel_process.pid, elapsed_time)
            
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}👋 Interrupted by user{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}💥 Error: {e}{Colors.RESET}")
        finally:
            self.executor.shutdown(wait=False)

    def show_completion_summary(self, ollama_pid, tunnel_pid, elapsed_time):
        """Show completion summary with timing"""
        summary = f"""
{Colors.GREEN}{'=' * 50}{Colors.RESET}
{Colors.BOLD}{Colors.GREEN}🎉 SETUP COMPLETE! 🎉{Colors.RESET}
{Colors.GREEN}{'=' * 50}{Colors.RESET}

{Colors.CYAN}📊 Status:{Colors.RESET}
{Colors.GREEN}✅ Ollama running{Colors.RESET} (PID: {ollama_pid})
{Colors.GREEN}✅ Tunnel active{Colors.RESET} (PID: {tunnel_pid})
{Colors.GREEN}✅ Model ready{Colors.RESET}

{Colors.BOLD}{Colors.YELLOW}⚡ Total time: {elapsed_time:.1f} seconds{Colors.RESET}
{Colors.BOLD}{Colors.MAGENTA}🔗 Check tunnel URL above for access{Colors.RESET}

{Colors.GREEN}{'=' * 50}{Colors.RESET}
"""
        print(summary)

def main():
    setup = SuperFastOllamaSetup()
    print(f"{Colors.CYAN}🎯 Model: {setup.ollama_model}{Colors.RESET}")
    setup.setup_all_fast()

if __name__ == "__main__":
    main()
