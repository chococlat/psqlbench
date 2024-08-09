import os
if __name__ == "__main__":
    os.system("pg_restore -U postgres -d postgres -1 data_only.dump")