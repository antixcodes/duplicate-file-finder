import os
import hashlib

def calculate_checksum(file_path, algorithm='sha256'):
    hash_alg = getattr(hashlib, algorithm)()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            hash_alg.update(chunk)
    return hash_alg.hexdigest()

def find_duplicates(directory, algorithm='sha256'):
    checksums = {}
    duplicates = []

    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            checksum = calculate_checksum(file_path, algorithm)
            if checksum in checksums:
                duplicates.append((checksums[checksum], file_path))
            else:
                checksums[checksum] = file_path

    return duplicates

def remove_duplicates(duplicates):
    for original, duplicate in duplicates:
        print(f"Removing duplicate file: {duplicate}")
        os.remove(duplicate)

def main():
    directory = input("Enter the directory path to scan for duplicates: ")
    algorithm = 'sha256'
    duplicates = find_duplicates(directory, algorithm)
    
    if duplicates:
        print("Duplicate files found:")
        for original, duplicate in duplicates:
            print(f"Original: {original}, Duplicate: {duplicate}")

        confirm = input("Do you want to delete the duplicate files? (yes/no): ").strip().lower()
        if confirm == 'yes':
            remove_duplicates(duplicates)
            print("Duplicate files removed.")
        else:
            print("No files were removed.")
    else:
        print("No duplicate files found.")

if __name__ == "__main__":
    main()
