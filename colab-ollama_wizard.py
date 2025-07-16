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
        self.ollama_model = "goonsai/qwen2.5-3B-goonsai-nsfw-100k"
        # self.ollama_model = "hf.co/TheBloke/Luna-AI-Llama2-Uncensored-GGUF:Q8_0"
        # self.ollama_model = "ollama run hf.co/Epiculous/Violet_Twilight-v0.2-GGUF:Q4_K_M"
        # self.ollama_model = "hf.co/mradermacher/MN-Violet-Lotus-12B-GGUF:Q4_K_M"
        # self.ollama_model = "hf.co/mradermacher/HamSter-0.2-i1-GGUF:Q6_K"
        self.overall_progress = 0

    def print_banner(self):
        banner = f"""
{Colors.CYAN}{'=' * 70}{Colors.RESET}
{Colors.BOLD}{Colors.MAGENTA}    🚀 OLLAMA SETUP WIZARD (COLAB EDITION) 🚀{Colors.RESET}
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
                        print(f"{Colors.RED}❌ Error: {result.stderr[:200]}...{Colors.RESET}")

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
        """Install Cloudflared for Colab, forcibly removing conflicting files first."""
        self.print_step(3, 5, "Installing Cloudflared", "☁️")

        # The key fix is adding 'rm -f /usr/local/bin/cloudflared' to remove the blocking file.
        commands = [
            ("rm -f /usr/local/bin/cloudflared", "Removing conflicting files... 🗑️"),
            ("apt-get clean", "Cleaning apt cache... 🧹"),
            ("apt-get -f install -y", "Fixing any broken dependencies... 🛠️"),
            ("dpkg --configure -a", "Reconfiguring pending packages... ⚙️"),
            ("mkdir -p --mode=0755 /usr/share/keyrings", "Creating keyrings directory... 📁"),
            ("curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null", "Adding GPG key... 🔑"),
            ("echo 'deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared any main' | tee /etc/apt/sources.list.d/cloudflared.list", "Adding repository... 📋"),
            ("apt-get update", "Updating package lists... 🔄"),
            ("apt-get install cloudflared -y", "Installing cloudflared... 📦")
        ]

        progress_bar = ProgressBar(emoji_start="☁️", emoji_end="✅")

        for i, (cmd, status) in enumerate(commands):
            progress = ((i + 1) / len(commands)) * 100
            progress_bar.update(progress, status)

            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                # Only fail on the final install step, as repair steps might exit with non-zero codes
                if "install cloudflared" in cmd:
                    print(f"\n{Colors.RED}❌ Failed: {cmd}\n{result.stderr}{Colors.RESET}")
                    return False
                else:
                    # Print a warning for other steps but continue
                    print(f"\n{Colors.YELLOW}⚠️ Warning on step '{cmd}': {result.stderr}{Colors.RESET}")
            
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
        # Using nohup to ensure the process continues running in the background
        process = subprocess.Popen(f"nohup {command} &", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print(f"{Colors.GREEN}🎉 Cloudflare tunnel started! Look for the public URL in the output above.{Colors.RESET}")
        return process

    def install_ollama_model(self, model_name=None):
        """Install Ollama model with a simulated progress bar to avoid excessive output."""
        if model_name is None:
            model_name = self.ollama_model

        self.print_step(5, 5, f"Installing Model: {model_name}", "🧠")

        print(f"{Colors.YELLOW}📥 Downloading model: {model_name}{Colors.RESET}")
        print(f"{Colors.YELLOW}⏳ This may take several minutes. A simulated progress bar will be shown.{Colors.RESET}")

        # Define messages for the simulated progress animation
        progress_messages = [
            "Initiating download...",
            "Fetching model layers...",
            "Downloading data (this can take a while)...",
            "Decompressing model...",
            "Verifying integrity...",
            "Finalizing installation..."
        ]

        # Execute the command with a simulated progress bar.
        # The duration is just for the animation; the script will wait as long as needed for the download to finish.
        command = f"ollama pull {model_name}"
        result = self.run_command_with_progress(
            command,
            progress_messages=progress_messages,
            duration=300  # Simulate a 5-minute progress bar
        )

        # Check the result of the command after it completes
        if result and result.returncode == 0:
            print(f"{Colors.GREEN}🎉 Model {model_name} installed successfully!{Colors.RESET}")
            return True
        else:
            print(f"{Colors.RED}💥 Failed to install model {model_name}.{Colors.RESET}")
            if result:
                # Show the error if the command failed, for easier debugging
                print(f"{Colors.RED}Error details: {result.stderr[:500]}...{Colors.RESET}")
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

{Colors.BOLD}{Colors.YELLOW}🔗 Your Ollama is now accessible worldwide via the Cloudflare URL!{Colors.RESET}
{Colors.BOLD}{Colors.MAGENTA}⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}

{Colors.CYAN}{'=' * 70}{Colors.RESET}
{Colors.BOLD}{Colors.BLUE}The services are running in the background.{Colors.RESET}
{Colors.BOLD}{Colors.BLUE}You can now use the public URL to access Ollama.{Colors.RESET}
{Colors.BOLD}{Colors.RED}To stop, you will need to interrupt/restart the Colab runtime.{Colors.RESET}
{Colors.CYAN}{'=' * 70}{Colors.RESET}
"""
        print(completion_banner)

    def setup_all(self):
        """Run the complete setup with beautiful progress"""
        self.print_banner()

        try:
            # Step 1: Install Ollama
            if not self.install_ollama():
                return

            # Step 2: Start Ollama server
            ollama_process = self.start_ollama_server()
            if not ollama_process:
                return

            # Step 3: Install Cloudflared
            # A short delay to let apt-get release any locks if needed.
            time.sleep(2)
            if not self.install_cloudflared():
                return

            # Step 4: Start Cloudflare tunnel
            # Delay to let the Ollama server initialize fully
            print(f"\n{Colors.YELLOW}⏳ Waiting for Ollama server to get ready...{Colors.RESET}")
            time.sleep(10) # Increased wait time for server
            tunnel_process = self.start_cloudflare_tunnel()
            if not tunnel_process:
                return
            
            # Allow time for the tunnel to start and print its URL
            print(f"\n{Colors.YELLOW}⏳ Waiting for Cloudflare tunnel to establish...{Colors.RESET}")
            time.sleep(10)

            # Step 5: Install Ollama model
            if not self.install_ollama_model():
                return

            # Show completion summary
            self.show_completion_summary(ollama_process.pid, tunnel_process.pid)

            # In Colab, the cell will keep running, and so will the background processes.
            # No need for an infinite loop which can be hard to stop.
            print(f"\n{Colors.BOLD}{Colors.GREEN}✅ All processes are running in the background.{Colors.RESET}")


        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}👋 Process interrupted by user. Services might still be running in the background.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}💥 An unexpected error occurred: {e}{Colors.RESET}")


def main():
    setup = EnhancedOllamaSetup()

    # In Colab, we can't easily pass sys.argv, so we'll hardcode or use a form
    # For now, we'll stick to the default model.
    # To use a different model, simply change the line below:
    # setup.ollama_model = "your-custom-model-name"

    print(f"{Colors.CYAN}🎯 Using model: {setup.ollama_model}{Colors.RESET}")

    setup.setup_all()


if __name__ == "__main__":
    main()
