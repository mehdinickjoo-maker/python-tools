import os
import hashlib
import json
import datetime
import zipfile
import tarfile
from sklearn.externals import joblib  # برای ذخیره مدل‌های یادگیری ماشین
import numpy as np

class MalwareScanner:
    def __init__(self, database_path, model_path):
        self.database_path = database_path
        self.malware_signatures = self.load_signatures()
        self.report = []
        self.model = self.load_model(model_path)

    def load_signatures(self):
        if not os.path.exists(self.database_path):
            print("Signature database not found!")
            return {}
        with open(self.database_path, 'r') as db_file:
            return json.load(db_file)

    def load_model(self, model_path):
        # بارگذاری مدل یادگیری ماشین
        if os.path.exists(model_path):
            return joblib.load(model_path)
        else:
            print("Model not found!")
            return None

    def hash_file(self, filepath):
        hasher = hashlib.sha256()
        with open(filepath, 'rb') as file:
            while chunk := file.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def static_analysis(self, filepath):
        # تحلیل استاتیک فایل
        file_hash = self.hash_file(filepath)
        if file_hash in self.malware_signatures:
            return self.malware_signatures[file_hash]
        return None

    def behavioral_analysis(self, filepath):
        # شبیه‌سازی اجرا برای تحلیل رفتار
        # (این بخش نیاز به پیاده‌سازی دقیق‌تری دارد)
        # می‌توان از subprocess برای اجرای فایل استفاده کرد و رفتار آنرا زیر نظر گرفت.
        print(f"Behavioral analysis for {filepath} not implemented yet.")
        return None

    def scan_file(self, filepath):
        static_result = self.static_analysis(filepath)
        if static_result:
            return static_result
        
        # شما می‌توانید برای تحلیل رفتار هم از اینجا اقدام کنید
        # behavioral_result = self.behavioral_analysis(filepath)
        # if behavioral_result:
        #     return behavioral_result

        return None

    def extract_files(self, archive_path):
        if zipfile.is_zipfile(archive_path):
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(os.path.dirname(archive_path))
                return zip_ref.namelist()
        elif tarfile.is_tarfile(archive_path):
            with tarfile.open(archive_path, 'r:*') as tar_ref:
                tar_ref.extractall(os.path.dirname(archive_path))
                return tar_ref.getnames()
        return []

    def scan_directory(self, directory):
        print(f"Scanning directory: {directory}")
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)

                if file_path.endswith(('.zip', '.tar', '.tar.gz', '.tgz')):
                    print(f"Extracting: {file_path}")
                    extracted_files = self.extract_files(file_path)
                    for extracted_file in extracted_files:
                        result = self.scan_file(os.path.join(root, extracted_file))
                        if result:
                            self.report.append(f"Malware detected in extracted file: {extracted_file} - {result}")

                result = self.scan_file(file_path)
                if result:
                    self.report.append(f"Malware detected: {file_path} - {result}")

    def save_report(self):
        report_file = "scan_report.txt"
        with open(report_file, 'w') as f:
            f.write("Malware Scan Report\n")
            f.write(f"Date: {datetime.datetime.now()}\n\n")
            for entry in self.report:
                f.write(entry + "\n")
        print(f"Report saved to {report_file}")

    def start_scan(self):
        directory_to_scan = input("Enter the directory path to scan: ")
        if os.path.isdir(directory_to_scan):
            self.scan_directory(directory_to_scan)
            if self.report:
                print("Malware detected with the following entries:")
                for entry in self.report:
                    print(entry)
            else:
                print("No malware found.")
            self.save_report()
        else:
            print("Invalid directory path.")

if __name__ == "__main__":
    database_path = 'malware_signatures.json'  # Ensure you have a database of malware signatures
    model_path = 'malware_model.pkl'  # Ensure you have a pre-trained model for machine learning
    scanner = MalwareScanner(database_path, model_path)
    scanner.start_scan()