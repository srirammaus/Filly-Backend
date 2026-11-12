import subprocess
import sys
import os
import time

def start_services():
    print("==================================================================")
    print("              FILLY MULTI-TENANT APPLICATION LAUNCHER             ")
    print("==================================================================")
    
    # Compute directories relative to this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    auth_dir = os.path.join(base_dir, "filly_auth_server")
    inference_dir = os.path.join(base_dir, "filly_inference_server")
    automation_dir = os.path.join(base_dir, "filly_automation_server")
    cron_dir = os.path.join(base_dir, "filly_cron_service")
    frontend_dir = os.path.join(os.path.dirname(base_dir), "Filly-Frontend")

    env = dict(os.environ, PYTHONUNBUFFERED="1")
    # 1. Start Auth Server on Port 5001
    print("[+] Starting Auth Server (Flask on Port 5001)...")
    auth_proc = subprocess.Popen(
        [sys.executable, "app.py"],
        cwd=auth_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=env
    )
    
    # 2. Start Inference Server on Port 5002
    print("[+] Starting Inference Server (Flask on Port 5002)...")
    inf_proc = subprocess.Popen(
        [sys.executable, "app.py"],
        cwd=inference_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=env
    )

    # 3. Start Automation Server on Port 5003
    print("[+] Starting Automation Server (Flask on Port 5003)...")
    auto_proc = subprocess.Popen(
        [sys.executable, "app.py"],
        cwd=automation_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=env
    )

    # 4. Start Cron Service Daemon
    print("[+] Starting Cron Service Daemon...")
    cron_proc = subprocess.Popen(
        [sys.executable, "main.py"],
        cwd=cron_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=env
    )
    
    # Give backend services time to initialize PostgreSQL databases
    print("[*] Waiting for backend servers to spin up and initialize schemas...")
    time.sleep(5)
    
    # 5. Start Frontend React Server
    print("[+] Starting Frontend Dev Server (Vite React)...")
    front_proc = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=frontend_dir,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    # Print status message
    print("\n[!] All services started successfully!")
    print("    - Auth Server:       http://localhost:5001")
    print("    - Inference Server:  http://localhost:5002")
    print("    - Automation Server: http://localhost:5003")
    print("    - Cron Service:      [Background Daemon]")
    print("    - Frontend URL:      http://localhost:5173")
    print("Press Ctrl+C to terminate all services.\n")
    
    processes = [
        ("AUTH", auth_proc),
        ("INFERENCE", inf_proc),
        ("AUTOMATION", auto_proc),
        ("CRON", cron_proc),
        ("FRONTEND", front_proc)
    ]
    
    # Helper for non-blocking stream readers
    import threading
    def stream_reader(name, proc):
        for line in iter(proc.stdout.readline, ''):
            print(f"[{name}] {line.strip()}")
            
    threads = []
    for name, proc in processes:
        t = threading.Thread(target=stream_reader, args=(name, proc), daemon=True)
        t.start()
        threads.append(t)
        
    try:
        while True:
            for name, proc in processes:
                code = proc.poll()
                if code is not None:
                    print(f"\n[!] Service {name} has stopped unexpectedly with exit code {code}.")
                    return
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Shutting down all services...")
    finally:
        for name, proc in processes:
            try:
                proc.terminate()
                proc.wait(timeout=3)
            except Exception:
                try:
                    proc.kill()
                except Exception:
                    pass
        print("[*] All services stopped.")

if __name__ == "__main__":
    start_services()
