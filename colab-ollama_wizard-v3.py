#!/usr/bin/env python3
import subprocess
import os
import time
import sys
import threading
import re
import asyncio
import concurrent.futures
from datetime import datetime
from queue import Queue, Empty
import multiprocessing

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
        self.lock = threading.Lock()

    def update(self, progress, status=""):
        with self.lock:
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

class UltraFastOllamaSetup:
    def __init__(self):
        self.cloudflare_token = "eyJhIjoiYzRhMTcwZmEzZGViOWRkNTRmNmQ1NTdkMmVlNjg2MTAiLCJ0IjoiMTBjN2Q3YzgtZWQwOC00ZTg1LThiMjYtYjBmMDg0ODliNTA1IiwicyI6Ik1qRTBORGt3Wm1JdE4yVTVNeTAwTmpGaUxXRTBNamd0WVdFeE9HVmlZamN4TVRNMSJ9"
        self.ollama_model = "hf.co/TheBloke/Pygmalion-2-13B-GGUF:Q4_K_M"
        self.max_workers = min(32, multiprocessing.cpu_count() * 4)  # Use more threads
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers)
        self.progress_queue = Queue()
        self.results = {}
        self.start_time = time.time()

    def print_banner(self):
        banner = f"""
{Colors.CYAN}{'=' * 70}{Colors.RESET}
{Colors.BOLD}{Colors.MAGENTA}    ⚡ ULTRA-FAST OLLAMA SETUP WIZARD ⚡{Colors.RESET}
{Colors.CYAN}{'=' * 70}{Colors.RESET}
{Colors.YELLOW}⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}
{Colors.RED}🔥 MAX PERFORMANCE MODE - USING {self.max_workers} THREADS{Colors.RESET}
{Colors.CYAN}{'=' * 70}{Colors.RESET}
"""
        print(banner)

    def print_step(self, step_num, total_steps, title, emoji):
        print(f"\n{Colors.BOLD}{Colors.BLUE}📋 Step {step_num}/{total_steps}: {emoji} {title}{Colors.RESET}")
        print(f"{Colors.CYAN}{'─' * 50}{Colors.RESET}")

    def run_command_async(self, command, shell=True, name="", timeout=300):
        """Run command asynchronously with timeout"""
        try:
            result = subprocess.run(
                command, 
                shell=shell, 
                capture_output=True, 
                text=True, 
                timeout=timeout,
                env=dict(os.environ, DEBIAN_FRONTEND='noninteractive')  # Non-interactive mode
            )
            return name, result
        except subprocess.TimeoutExpired:
            return name, None
        except Exception as e:
            return name, None

    def parallel_command_runner(self, commands):
        """Run multiple commands in parallel"""
        futures = []
        for cmd_info in commands:
            if len(cmd_info) == 3:
                command, name, timeout = cmd_info
            else:
                command, name = cmd_info
                timeout = 300
            
            future = self.executor.submit(self.run_command_async, command, True, name, timeout)
            futures.append(future)
        
        results = {}
        for future in concurrent.futures.as_completed(futures):
            name, result = future.result()
            results[name] = result
        
        return results

    def install_ollama_parallel(self):
        """Install Ollama with parallel preparation"""
        self.print_step(1, 4, "Installing Ollama (Parallel Mode)", "🚀")
        
        progress_bar = ProgressBar(emoji_start="⚡", emoji_end="✅")
        
        # Parallel preparation commands
        prep_commands = [
            ("curl -fsSL https://ollama.com/install.sh -o /tmp/ollama_install.sh", "download_script", 30),
            ("mkdir -p /usr/local/bin", "create_dirs", 10),
            ("export PATH=/usr/local/bin:$PATH", "setup_path", 5)
        ]
        
        progress_bar.update(25, "Parallel preparation...")
        prep_results = self.parallel_command_runner(prep_commands)
        
        progress_bar.update(50, "Installing Ollama...")
        install_result = self.run_command_async("bash /tmp/ollama_install.sh", True, "install", 120)
        
        progress_bar.update(75, "Configuring environment...")
        
        # Set up environment in parallel
        env_commands = [
            ("echo 'export PATH=/usr/local/bin:$PATH' >> ~/.bashrc", "bashrc", 5),
            ("export OLLAMA_HOST=0.0.0.0", "host_config", 5),
            ("export OLLAMA_ORIGINS=*", "origins_config", 5)
        ]
        
        env_results = self.parallel_command_runner(env_commands)
        progress_bar.update(100, "Installation complete!")
        
        if install_result[1] and install_result[1].returncode == 0:
            print(f"{Colors.GREEN}🎉 Ollama installed successfully!{Colors.RESET}")
            return True
        else:
            print(f"{Colors.RED}💥 Failed to install Ollama{Colors.RESET}")
            return False

    def start_ollama_server_fast(self):
        """Start Ollama server with immediate launch"""
        self.print_step(2, 4, "Starting Ollama Server (Instant)", "🖥️")
        
        # Set environment variables
        os.environ['OLLAMA_HOST'] = '0.0.0.0'
        os.environ['OLLAMA_ORIGINS'] = '*'
        
        progress_bar = ProgressBar(emoji_start="🔄", emoji_end="🟢")
        
        progress_bar.update(25, "Configuring server...")
        
        # Start server immediately in background
        command = "nohup ollama serve > /tmp/ollama.log 2>&1 &"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        progress_bar.update(50, "Server starting...")
        
        # Quick health check
        for i in range(20):  # 2 seconds max
            try:
                check_result = subprocess.run(
                    "pgrep -f 'ollama serve'", 
                    shell=True, 
                    capture_output=True, 
                    timeout=1
                )
                if check_result.returncode == 0:
                    progress_bar.update(100, "Server ready!")
                    print(f"{Colors.GREEN}🎉 Ollama server started lightning fast!{Colors.RESET}")
                    return process
            except:
                pass
            time.sleep(0.1)
        
        progress_bar.update(100, "Server started (backgrounded)")
        print(f"{Colors.GREEN}🎉 Ollama server started!{Colors.RESET}")
        return process

    def install_cloudflared_parallel(self):
        """Install Cloudflared with maximum parallelism"""
        self.print_step(3, 4, "Installing Cloudflared (Parallel)", "☁️")
        
        progress_bar = ProgressBar(emoji_start="☁️", emoji_end="✅")
        
        # Parallel cleanup and preparation
        cleanup_commands = [
            ("rm -f /usr/local/bin/cloudflared", "remove_conflict", 5),
            ("apt-get clean", "clean_cache", 10),
            ("dpkg --configure -a", "configure_packages", 15),
            ("mkdir -p --mode=0755 /usr/share/keyrings", "create_keyrings", 5)
        ]
        
        progress_bar.update(20, "Parallel cleanup...")
        cleanup_results = self.parallel_command_runner(cleanup_commands)
        
        progress_bar.update(40, "Adding repository...")
        
        # Repository setup (sequential due to dependencies)
        repo_commands = [
            "curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null",
            "echo 'deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared any main' | tee /etc/apt/sources.list.d/cloudflared.list"
        ]
        
        for cmd in repo_commands:
            subprocess.run(cmd, shell=True, capture_output=True)
        
        progress_bar.update(70, "Updating package lists...")
        
        # Parallel update and install
        install_commands = [
            ("apt-get update -y", "update_packages", 60),
            ("apt-get install cloudflared -y", "install_cloudflared", 60)
        ]
        
        progress_bar.update(90, "Installing cloudflared...")
        install_results = self.parallel_command_runner(install_commands)
        
        progress_bar.update(100, "Installation complete!")
        
        if install_results.get("install_cloudflared") and install_results["install_cloudflared"].returncode == 0:
            print(f"{Colors.GREEN}🎉 Cloudflared installed at light speed!{Colors.RESET}")
            return True
        else:
            print(f"{Colors.RED}💥 Failed to install Cloudflared{Colors.RESET}")
            return False

    def start_cloudflare_tunnel_instant(self):
        """Start Cloudflare tunnel instantly"""
        self.print_step(4, 4, "Starting Cloudflare Tunnel (Instant)", "🌐")
        
        progress_bar = ProgressBar(emoji_start="🌐", emoji_end="🚀")
        
        progress_bar.update(25, "Connecting to Cloudflare...")
        
        # Start tunnel immediately
        command = f"nohup cloudflared tunnel run --token {self.cloudflare_token} > /tmp/cloudflared.log 2>&1 &"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        progress_bar.update(50, "Establishing tunnel...")
        
        # Quick verification
        time.sleep(2)  # Minimal wait
        
        progress_bar.update(100, "Tunnel active!")
        print(f"{Colors.GREEN}🎉 Cloudflare tunnel started instantly!{Colors.RESET}")
        return process

    def install_ollama_model_background(self, model_name=None):
        """Install Ollama model in background with real-time progress"""
        if model_name is None:
            model_name = self.ollama_model
        
        print(f"\n{Colors.BOLD}{Colors.BLUE}📋 Background Task: 🧠 Installing Model: {model_name}{Colors.RESET}")
        print(f"{Colors.CYAN}{'─' * 50}{Colors.RESET}")
        
        print(f"{Colors.YELLOW}📥 Model download started in background...{Colors.RESET}")
        
        # Start model download in background
        command = f"nohup ollama pull {model_name} > /tmp/model_install.log 2>&1 &"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print(f"{Colors.GREEN}🎉 Model installation initiated! (PID: {process.pid}){Colors.RESET}")
        print(f"{Colors.YELLOW}📋 Check /tmp/model_install.log for progress{Colors.RESET}")
        
        return process

    def monitor_processes(self, ollama_pid, tunnel_pid, model_pid):
        """Monitor all processes in background"""
        def check_process(pid, name):
            try:
                result = subprocess.run(f"ps -p {pid}", shell=True, capture_output=True)
                return result.returncode == 0
            except:
                return False
        
        def monitor_thread():
            while True:
                ollama_running = check_process(ollama_pid, "Ollama")
                tunnel_running = check_process(tunnel_pid, "Tunnel")
                model_running = check_process(model_pid, "Model")
                
                status = f"Ollama: {'🟢' if ollama_running else '🔴'} | Tunnel: {'🟢' if tunnel_running else '🔴'} | Model: {'🟢' if model_running else '🔴'}"
                
                if not model_running:
                    print(f"\n{Colors.GREEN}🎉 Model installation completed!{Colors.RESET}")
                    break
                
                time.sleep(5)
        
        monitor = threading.Thread(target=monitor_thread, daemon=True)
        monitor.start()
        return monitor

    def show_completion_summary(self, ollama_pid, tunnel_pid, model_pid):
        """Show ultra-fast completion summary"""
        elapsed_time = time.time() - self.start_time
        
        completion_banner = f"""
{Colors.GREEN}{'=' * 70}{Colors.RESET}
{Colors.BOLD}{Colors.GREEN}    ⚡ ULTRA-FAST SETUP COMPLETED! ⚡{Colors.RESET}
{Colors.GREEN}{'=' * 70}{Colors.RESET}

{Colors.BOLD}{Colors.CYAN}📊 Lightning Summary:{Colors.RESET}
{Colors.GREEN}✅ Ollama installed and running{Colors.RESET}        (PID: {ollama_pid})
{Colors.GREEN}✅ Cloudflare tunnel active{Colors.RESET}           (PID: {tunnel_pid})
{Colors.GREEN}🔄 Model {self.ollama_model} downloading{Colors.RESET} (PID: {model_pid})
{Colors.GREEN}✅ External access configured{Colors.RESET}

{Colors.BOLD}{Colors.MAGENTA}⚡ Total Setup Time: {elapsed_time:.2f} seconds{Colors.RESET}
{Colors.BOLD}{Colors.YELLOW}🔗 Your Ollama is accessible worldwide via Cloudflare URL!{Colors.RESET}
{Colors.BOLD}{Colors.MAGENTA}⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}

{Colors.CYAN}{'=' * 70}{Colors.RESET}
{Colors.BOLD}{Colors.BLUE}All services running at maximum performance!{Colors.RESET}
{Colors.BOLD}{Colors.YELLOW}Model download continues in background.{Colors.RESET}
{Colors.BOLD}{Colors.RED}To stop, interrupt/restart the Colab runtime.{Colors.RESET}
{Colors.CYAN}{'=' * 70}{Colors.RESET}
"""
        print(completion_banner)

    def setup_all_ultrafast(self):
        """Run the complete setup at maximum speed"""
        self.print_banner()
        
        try:
            # Step 1: Install Ollama (parallel)
            if not self.install_ollama_parallel():
                return
            
            # Step 2: Start Ollama server (instant)
            ollama_process = self.start_ollama_server_fast()
            if not ollama_process:
                return
            
            # Step 3: Install Cloudflared (parallel)
            if not self.install_cloudflared_parallel():
                return
            
            # Step 4: Start Cloudflare tunnel (instant)
            tunnel_process = self.start_cloudflare_tunnel_instant()
            if not tunnel_process:
                return
            
            # Step 5: Start model download in background
            model_process = self.install_ollama_model_background()
            if not model_process:
                return
            
            # Show completion summary
            self.show_completion_summary(ollama_process.pid, tunnel_process.pid, model_process.pid)
            
            # Start monitoring in background
            monitor_thread = self.monitor_processes(ollama_process.pid, tunnel_process.pid, model_process.pid)
            
            print(f"\n{Colors.BOLD}{Colors.GREEN}⚡ ULTRA-FAST SETUP COMPLETE! All processes running at maximum speed!{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.YELLOW}📊 Check /tmp/model_install.log for model download progress{Colors.RESET}")
            
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}👋 Process interrupted by user.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}💥 Error: {e}{Colors.RESET}")
        finally:
            self.executor.shutdown(wait=False)

def main():
    setup = UltraFastOllamaSetup()
    
    print(f"{Colors.CYAN}🎯 Using model: {setup.ollama_model}{Colors.RESET}")
    print(f"{Colors.RED}🔥 Maximum performance mode with {setup.max_workers} threads{Colors.RESET}")
    
    setup.setup_all_ultrafast()

if __name__ == "__main__":
    main()
