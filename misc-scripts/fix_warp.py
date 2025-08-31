import subprocess
import time

def run_command(command, sudo=False):
    """Run a command in the terminal and return its output."""
    if sudo and not command.startswith("sudo"):
        command = "sudo " + command
    try:
        result = subprocess.run(
            command, shell=True, check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Command failed: {command}")
        print(e.stderr.strip())
        return ""

def main():
    print("🛠️ Fixing Cloudflare WARP and DNS...\n")

    # 1. Disconnect WARP
    print("🔌 Disconnecting WARP...")
    run_command("warp-cli disconnect", sudo=True)

    # 2. Remove immutable flag on /etc/resolv.conf
    print("🔓 Removing immutable flag from /etc/resolv.conf...")
    run_command("chattr -i /etc/resolv.conf", sudo=True)

    # 3. Restart the WARP service
    print("🔁 Restarting warp-svc...")
    run_command("systemctl restart warp-svc", sudo=True)

    # 4. Check and register if needed
    print("📝 Checking WARP registration...")
    status = run_command("warp-cli status")
    if "Registration Missing" in status:
        print("📥 Registering WARP...")
        run_command("warp-cli registration new", sudo=True)

    # 5. Set mode to warp+doh
    print("⚙️ Setting WARP mode to warp+doh...")
    run_command("warp-cli mode warp+doh", sudo=True)

    # 6. Connect WARP
    print("🔗 Connecting to WARP...")
    run_command("warp-cli connect", sudo=True)

    # 7. Wait a bit for the connection to establish
    time.sleep(3)
    print("📡 Checking WARP status...")
    print(run_command("warp-cli status"))

    # 8. Test DNS resolution
    print("🌐 Testing DNS resolution (Cloudflare trace)...")
    trace = run_command("curl https://www.cloudflare.com/cdn-cgi/trace")
    print(trace if trace else "❌ Could not reach Cloudflare.")

    print("\n✅ Done!")

if __name__ == "__main__":
    main()
