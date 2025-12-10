from pathlib import Path

def delete_json_files(data_dir="data"):
    """Delete all JSON files in the data directory and subdirectories"""
    
    data_path = Path(data_dir)
    
    # Check if data directory exists
    if not data_path.exists():
        print(f"❌ Directory '{data_dir}' does not exist")
        return
    
    # Find all JSON files
    json_files = list(data_path.rglob("*.json"))
    
    if not json_files:
        print(f"✅ No JSON files found in '{data_dir}'")
        return
    
    print(f"Found {len(json_files)} JSON file(s) to delete:")
    for file in json_files:
        print(f"  - {file}")
    
    # Delete files
    deleted_count = 0
    error_count = 0
    
    for file in json_files:
        try:
            file.unlink()
            print(f"🗑️  Deleted: {file}")
            deleted_count += 1
        except Exception as e:
            print(f"❌ Error deleting {file}: {e}")
            error_count += 1
    
    print(f"\n✅ Deletion complete!")
    print(f"   Deleted: {deleted_count} file(s)")
    if error_count > 0:
        print(f"   Errors: {error_count} file(s)")


def delete_empty_directories(data_dir="data"):
    """Delete empty subdirectories in the data directory"""
    
    data_path = Path(data_dir)
    
    if not data_path.exists():
        return
    
    # Get all subdirectories
    subdirs = [d for d in data_path.iterdir() if d.is_dir()]
    
    deleted_dirs = []
    for subdir in subdirs:
        # Check if directory is empty
        if not any(subdir.iterdir()):
            try:
                subdir.rmdir()
                deleted_dirs.append(subdir.name)
                print(f"🗑️  Deleted empty directory: {subdir}")
            except Exception as e:
                print(f"❌ Error deleting directory {subdir}: {e}")
    
    if deleted_dirs:
        print(f"\n✅ Deleted {len(deleted_dirs)} empty director(ies)")


if __name__ == "__main__":
    print("=" * 60)
    print("JSON File Cleaner - Data Directory")
    print("=" * 60)
    print()
    
    # Delete JSON files
    delete_json_files("data")
    
    delete_empty_directories("data")
    
    print("\n" + "=" * 60)
    print("✅ Cleanup complete!")
    print("=" * 60)