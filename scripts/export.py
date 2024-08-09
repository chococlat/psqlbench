import os, subprocess

def run(cmd):
    so,se = None,None
    try:
        sp = subprocess.Popen(cmd, stdout=so, stderr=se, text=True)
        stdout, stderr = sp.communicate()
        return stdout
    except Exception:
        print(se)
        return None

if __name__ == "__main__":
    os.system("pg_dump -U postgres -d postgres --data-only -F c -f data_only.dump")