#!/usr/bin/env python3
"""
Project: Fleece Gamma - Reasoning Model Setup Utility
Verifies or downloads GGUF weights directly into models/
"""

import os
import sys
import time
import re
import urllib.request
import urllib.parse
import http.cookiejar

MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")

MODEL_CONFIG = {
    "filename": "Qwen3.5-9B-The-Defiant-Fable-Uncnr-Heretic-plusIQ-TOOLS-NEO-MAX-MTP-Q6_K.gguf",
    "alias": "model.gguf",
    "gdrive_id": "1nXDpB_quZsSKURtLlJ-1e9ApjqBbXiOJ",
    "fallback_url": (
        "https://huggingface.co/DavidAU/"
        "Qwen3.5-9B-The-Defiant-Fable-Uncensored-Heretic-NEO-IMATRIX-MAX-MTP-GGUF/"
        "resolve/main/Qwen3.5-9B-The-Defiant-Fable-Uncnr-Heretic-plusIQ-TOOLS-NEO-MAX-MTP-Q6_K.gguf"
    ),
    "min_bytes": 5_000_000_000,
}


def _ensure_local_alias(target_path: str):
    alias_path = os.path.join(MODEL_DIR, MODEL_CONFIG["alias"])
    if not os.path.exists(alias_path) and not os.path.islink(alias_path):
        try:
            os.symlink(os.path.basename(target_path), alias_path)
        except Exception:
            pass


def _download_stream(resp, target_path, total_size, filename):
    temp_path = target_path + ".download"
    t0 = time.time()
    downloaded = 0
    chunk_size = 1024 * 1024  # 1MB chunks

    with open(temp_path, "wb") as f:
        while True:
            chunk = resp.read(chunk_size)
            if not chunk:
                break
            f.write(chunk)
            downloaded += len(chunk)
            if total_size > 0:
                pct = min(100.0, downloaded * 100.0 / total_size)
                mb_down = downloaded / (1024 * 1024)
                mb_tot = total_size / (1024 * 1024)
                elapsed = time.time() - t0
                speed = mb_down / max(0.1, elapsed)
                sys.stdout.write(
                    f"\rDownloading {filename}: [{mb_down:.1f} / {mb_tot:.1f} MB] ({pct:.1f}%) - {speed:.1f} MB/s   "
                )
                sys.stdout.flush()

    if downloaded >= MODEL_CONFIG["min_bytes"]:
        os.replace(temp_path, target_path)
        _ensure_local_alias(target_path)
        sys.stdout.write(
            f"\n[✓] {filename} verified and ready ({os.path.getsize(target_path) / (1024*1024):.1f} MB).\n"
        )
        sys.stdout.flush()
        return target_path
    else:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise RuntimeError("Download incomplete or corrupt.")


def download_model(force: bool = False) -> str:
    os.makedirs(MODEL_DIR, exist_ok=True)
    target_path = os.path.join(MODEL_DIR, MODEL_CONFIG["filename"])

    if os.path.islink(target_path):
        if not os.path.exists(target_path):
            os.remove(target_path)
        else:
            size = os.path.getsize(target_path)
            if size >= MODEL_CONFIG["min_bytes"]:
                _ensure_local_alias(target_path)
                print(f"[✓] {MODEL_CONFIG['filename']} verified ({size / (1024*1024):.1f} MB).")
                return target_path

    if os.path.exists(target_path) and not force:
        size = os.path.getsize(target_path)
        if size >= MODEL_CONFIG["min_bytes"]:
            _ensure_local_alias(target_path)
            print(f"[✓] {MODEL_CONFIG['filename']} verified ({size / (1024*1024):.1f} MB).")
            return target_path

    filename = MODEL_CONFIG["filename"]
    print(f"[Fleece Gamma] Fetching {filename}...")

    # 1. Primary Origin (Hugging Face Direct Stream for exact plusIQ-TOOLS Q6_K build)
    try:
        req = urllib.request.Request(MODEL_CONFIG["fallback_url"], headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req)
        total_size = int(resp.headers.get("Content-Length", 0))
        return _download_stream(resp, target_path, total_size, filename)
    except Exception:
        pass

    # 2. Secondary Origin (Dedicated GDrive File Link)
    try:
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        url = f"https://drive.google.com/uc?export=download&id={MODEL_CONFIG['gdrive_id']}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = opener.open(req)

        content_type = resp.headers.get("Content-Type", "")
        if "octet-stream" in content_type:
            total_size = int(resp.headers.get("Content-Length", 0))
            return _download_stream(resp, target_path, total_size, filename)
        else:
            html = resp.read().decode("utf-8", errors="ignore")
            form_match = re.search(
                r"<form[^>]*action=[\x27\x22]([^\x27\x22]+)[\x27\x22][^>]*>(.*?)</form>",
                html,
                re.DOTALL,
            )
            if form_match:
                action, body = form_match.groups()
                inputs = dict(
                    re.findall(
                        r"<input[^>]*name=[\x27\x22]([^\x27\x22]+)[\x27\x22][^>]*value=[\x27\x22]([^\x27\x22]*)[\x27\x22]",
                        body,
                    )
                )
                download_url = action + "?" + urllib.parse.urlencode(inputs)
                resp2 = opener.open(urllib.request.Request(download_url, headers={"User-Agent": "Mozilla/5.0"}))
                total_size = int(resp2.headers.get("Content-Length", 0))
                return _download_stream(resp2, target_path, total_size, filename)
    except Exception as exc:
        print(f"\n[✗] Failed to fetch {filename}: {exc}")
        raise


if __name__ == "__main__":
    download_model()
