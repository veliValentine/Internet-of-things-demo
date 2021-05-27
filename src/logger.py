from datetime import datetime

LOG_FILE = "log.txt"

class Logger:
    def log(description, message = "", file_path = LOG_FILE):
        file = None
        try:
            file = open(file_path, "a")
            time = datetime.now()
            log_entry = f"{time}, {description}, {message}\n"
            file.write(log_entry)
        except:
            print("Error when writing to", file_path)
        finally:
            try:
                file.close()
            finally:
                pass
