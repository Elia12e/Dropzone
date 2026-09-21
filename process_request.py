from pathlib import Path
import zipfile
import tempfile
import csv
import pandas as pd


downloads = Path.home() / "Downloads"



def extract_zip(zip_path, extracted_folder):
    with zipfile.ZipFile(zip_path, "r") as zip_file:
        zip_file.extractall(extracted_folder)

    return extracted_folder

categories = {
    "images": [".png", ".jpg", ".jpeg"],
    "documents": [".pdf", ".docx", ".txt"],
    "videos": [".mp4", ".mov"],
    "archives": [".zip", ".rar"],
    "code": [".py", ".js", ".sv"]
}


def classify_file(filename):
      file_extension = Path(filename).suffix.lower()
      for category, extensions in categories.items():
           if file_extension in extensions:
            return category
      return "other"
def process_request(request):
    if not isinstance(request, dict):
        return {"status": "error", "message": "request must be a dictionary"}
    if "files" not in request:
         return {"status": "error", "message": "files must be in request"}
    files = request["files"] 
    if not isinstance(files, list):
         return {"status": "error", "message": "files must be a list"}
    if not all(isinstance(item, str) and item != ""for item in files):
         return {"status": "error", "message": "files must contain non-empty strings"}
    include_unknown = request.get("include_unknown", True)
    if not isinstance(include_unknown, bool):
         return {"status": "error", "message": "include_unknown must be a boolean"}         
    
    groups = {category: [] for category in categories}
    groups["other"] = []
    for filename in files:
        category = classify_file(filename)
        
        if category == "other" and not include_unknown:
            continue
    
        groups[category].append(filename)
    total = sum(len(file_list) for file_list in groups.values())
    return {
    "status": "success",
    "total": total,
    "groups": groups}


def get_safe_destination(folder, file):
    destination = folder / file.name
    counter = 1
    while destination.exists():
        new_name = f"{file.stem}_{counter}{file.suffix}"
        destination = folder / new_name
        counter += 1
    else:
        return destination
    

def organize_folder(folder_path):
        files = list(folder_path.iterdir())
        for file in files:
            category = classify_file(file)
            folder = folder_path / category
            folder.mkdir(exist_ok=True)
            destination = get_safe_destination(folder, file)
            file.rename(destination)
        
def log_files(folder_path, log_path):
    with open(log_path, 'w', newline="") as csvfile:
        logwriter = csv.writer(csvfile)

        logwriter.writerow(["filename", "extension", "category"])
        for file in folder_path.rglob("*"):
            if file.is_file():
                category = classify_file(file)
                logwriter.writerow([file.name, file.suffix.lower(), category])

def analyze_log(log_path):           
    df = pd.read_csv(log_path)
    
    total_files = len(df)
    category_counts = df["category"].value_counts().to_dict()
    extension_counts = df["extension"].value_counts().to_dict()
    longest_category = df["category"].value_counts().index[0]
    
    return {"total_files": total_files,
            "category_counts": category_counts,
            "extension_counts": extension_counts,
            "most_common_category": longest_category}
       
def create_zip(folder_path, output_path):
    with zipfile.ZipFile(output_path, "w") as zip_file:
        for file in folder_path.rglob("*"):
            if file.is_file():
                zip_file.write(file, file.relative_to(folder_path))
        return output_path
def organize_zip(zip_path, output_path):
    with tempfile.TemporaryDirectory() as temp_dir:
        extracted = Path(temp_dir) / "extracted"
        extracted_folder = extract_zip(zip_path, extracted)
        organize_folder(extracted_folder,)
        log_path = extracted_folder / "dropzone_log.csv"
        log_files(extracted_folder, log_path)
        analyze_log(log_path)
        organized_files =create_zip(extracted_folder, output_path)
        return organized_files
    
    

result = organize_zip(
    Path("test.zip"),
    Path("organized.zip")
)

print(result)
