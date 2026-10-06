# BlobDump - Azure Blob Storage Downloader

BlobDump is a lightweight Python CLI tool that enumerates publicly listable Azure Blob Storage containers and downloads their contents concurrently. It requires no Azure credentials when anonymous container listing and blob access are enabled.

### Features
* Enumerate publicly listable Azure Blob containers
* Download blobs concurrently
* Configurable number of threads
* Preserve blob directory structure
* Automatically handle Azure Blob listing pagination
* No Azure credentials required for publicly accessible containers
* Minimal Python dependencies

## Usage

```bash
python blobdump.py <ACCOUNT_NAME> <CONTAINER_NAME>
```

Example:

```bash
python blobdump.py mystorageaccount public-files
```

Specify the output directory:

```bash
python blobdump.py mystorageaccount public-files -o downloads
```

Increase concurrency:

```bash
python blobdump.py mystorageaccount public-files -t 30
```

## Options

```text
account             Azure Storage account name
container           Azure Blob container name

-o, --output        Output directory
                    Default: downloads

-t, --threads       Number of concurrent download threads
                    Default: 10
```

## Example

```text
$ python blobdump.py mystorageaccount public-files

Author: Muhammad Zeeshan (Xib3rR4dAr)


[+] Account   : mystorageaccount
[+] Container : public-files
[+] Listing blobs...
[+] Found 127 blobs

[1/127] downloaded: documents/report.pdf
[2/127] downloaded: images/logo.png
[3/127] downloaded: backup/database.zip
[4/127] exists: documents/test.docx
...
[127/127] downloaded: archive/data.csv
```

## Output Structure

BlobDump preserves the original blob paths:

```text
downloads/
├── documents/
│   ├── report.pdf
│   └── test.docx
├── images/
│   └── logo.png
└── backup/
    └── database.zip
```

## Requirements

Python 3.8+

Install dependencies:

```bash
pip install -r requirements.txt
```

`requirements.txt`:

```text
requests>=2.31.0
```

## Responsible Use

Use BlobDump only against Azure Storage resources that you own or have explicit authorization to assess or download.

The author is not responsible for misuse of this tool or unauthorized access to data.
