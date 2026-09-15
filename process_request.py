from pathlib import Path

downloads = Path.home() / "Downloads"
files = list(downloads.iterdir())

categories = {
    "images": [".png", ".jpg", ".jpeg"],
    "documents": [".pdf", ".docx", ".txt"],
    "videos": [".mp4", ".mov"],
    "archives": [".zip", ".rar"],
    "code": [".py", ".js", ".sv"]
}


def classify_file(filename):
      extension = Path(filename).suffix.lower()
      if extension in categories["images"]:
        return "images"
      if extension in categories["documents"]:
        return "documents"
      if extension in categories["code"]:
        return "code"
      else:
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
    
    groups = {
        "images": [],
        "documents": [],
        "code": [],
        "other": []}
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


def organize_folder():
    

    for file in files:
        for category, extension in categories.items():
            if file.suffix.lower()  in extension:
                    folder = downloads / category
                    folder.mkdir(exist_ok=True)
                    destination = folder / file.name
                    if destination.exists():
                          new_name = file.stem + "_1" + file.suffix
                          destination = folder / new_name
                    file.rename(destination)
                    break
        else:
                folder = downloads / "other"
                folder.mkdir(exist_ok=True)
                destination = folder / file.name
                file.rename(destination)
      
