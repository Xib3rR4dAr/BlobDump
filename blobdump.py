#!/usr/bin/env python3

import argparse
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote
import xml.etree.ElementTree as ET


def list_blobs(account, container):
    url = f"https://{account}.blob.core.windows.net/{container}"
    blobs = []
    marker = None

    while True:
        params = {
            "restype": "container",
            "comp": "list",
        }

        if marker:
            params["marker"] = marker

        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()

        root = ET.fromstring(r.text)

        for blob in root.findall(".//Blob"):
            name = blob.findtext("Name")
            if name:
                blobs.append(name)

        marker_node = root.find(".//NextMarker")
        marker = marker_node.text if marker_node is not None else None

        if not marker:
            break

    return blobs


def download_blob(account, container, blob, output_dir):
    url = (
        f"https://{account}.blob.core.windows.net/"
        f"{container}/{quote(blob, safe='/')}"
    )

    # Preserve blob directory structure
    path = os.path.join(output_dir, blob)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    if os.path.exists(path):
        return blob, "exists"

    r = requests.get(url, stream=True, timeout=120)
    r.raise_for_status()

    with open(path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

    return blob, "downloaded"


def main():
    parser = argparse.ArgumentParser(
        description="Multithreaded public Azure Blob container downloader"
    )

    parser.add_argument("account", help="Azure storage account name")
    parser.add_argument("container", help="Azure blob container name")

    parser.add_argument(
        "-o",
        "--output",
        default="downloads",
        help="Output directory (default: downloads)",
    )

    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        default=10,
        help="Number of download threads (default: 10)",
    )

    args = parser.parse_args()

    print(f"[+] Account   : {args.account}")
    print(f"[+] Container : {args.container}")
    print("[+] Listing blobs...")

    blobs = list_blobs(args.account, args.container)

    print(f"[+] Found {len(blobs)} blobs")

    if not blobs:
        return

    os.makedirs(args.output, exist_ok=True)

    completed = 0

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {
            executor.submit(
                download_blob,
                args.account,
                args.container,
                blob,
                args.output,
            ): blob
            for blob in blobs
        }

        for future in as_completed(futures):
            blob = futures[future]

            try:
                _, status = future.result()
                completed += 1
                print(f"[{completed}/{len(blobs)}] {status}: {blob}")

            except Exception as e:
                completed += 1
                print(f"[{completed}/{len(blobs)}] ERROR: {blob} -> {e}")


if __name__ == "__main__":
    main()