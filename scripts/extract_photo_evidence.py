#!/usr/bin/env python3
"""Extract conservative photo metadata and optional OCR into an evidence JSON file."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from PIL import ExifTags, Image


SAFE_EXIF = {
    "DateTimeOriginal",
    "DateTimeDigitized",
    "Make",
    "Model",
    "LensModel",
    "Orientation",
    "ImageDescription",
    "UserComment",
    "XPTitle",
    "XPComment",
    "GPSInfo",
}


def json_safe(value: Any) -> Any:
    if isinstance(value, bytes):
        for encoding in ("utf-16-le", "utf-8", "latin-1"):
            try:
                return value.decode(encoding).rstrip("\x00")
            except UnicodeDecodeError:
                pass
        return value.hex()
    if isinstance(value, (tuple, list)):
        return [json_safe(item) for item in value]
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    try:
        json.dumps(value)
        return value
    except TypeError:
        return str(value)


def rational_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError, ZeroDivisionError):
        numerator, denominator = value
        return float(numerator) / float(denominator)


def dms_to_decimal(dms: Any, ref: str) -> float:
    degrees, minutes, seconds = (rational_float(part) for part in dms)
    result = degrees + minutes / 60 + seconds / 3600
    return -result if ref.upper() in {"S", "W"} else result


def extract_gps(gps_raw: Any) -> dict[str, Any]:
    if not isinstance(gps_raw, dict):
        return {"raw": json_safe(gps_raw)}
    gps = {ExifTags.GPSTAGS.get(key, str(key)): value for key, value in gps_raw.items()}
    result: dict[str, Any] = {"raw": json_safe(gps)}
    try:
        lat_ref = str(gps["GPSLatitudeRef"])
        lon_ref = str(gps["GPSLongitudeRef"])
        result["latitude"] = round(dms_to_decimal(gps["GPSLatitude"], lat_ref), 7)
        result["longitude"] = round(dms_to_decimal(gps["GPSLongitude"], lon_ref), 7)
    except (KeyError, TypeError, ValueError, ZeroDivisionError):
        pass
    return result


def extract_exif(image: Image.Image) -> dict[str, Any]:
    exif = image.getexif()
    output: dict[str, Any] = {}
    for tag_id, raw_value in exif.items():
        name = ExifTags.TAGS.get(tag_id, str(tag_id))
        if name not in SAFE_EXIF:
            continue
        value = exif.get_ifd(tag_id) if name == "GPSInfo" else raw_value
        output[name] = extract_gps(value) if name == "GPSInfo" else json_safe(value)
    return output


def run_ocr(path: Path, language: str) -> dict[str, Any]:
    executable = shutil.which("tesseract")
    if not executable:
        return {"status": "unavailable", "text": "", "note": "Verify all OCR visually."}
    languages = subprocess.run(
        [executable, "--list-langs"], check=False, capture_output=True, text=True
    )
    available = {
        item.strip()
        for item in languages.stdout.splitlines()
        if item.strip() and not item.lower().startswith("list of available")
    }
    requested = [item for item in language.split("+") if item]
    usable = [item for item in requested if item in available]
    missing = [item for item in requested if item not in available]
    if not usable:
        return {
            "status": "unavailable",
            "requested_languages": requested,
            "missing_languages": missing,
            "text": "",
            "note": "Install a requested OCR language or transcribe visually; never guess.",
        }
    selected_language = "+".join(usable)
    command = [executable, str(path), "stdout", "-l", selected_language]
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    return {
        "status": (
            "completed_partial_language"
            if completed.returncode == 0 and missing
            else "completed"
            if completed.returncode == 0
            else "failed"
        ),
        "requested_languages": requested,
        "used_languages": usable,
        "missing_languages": missing,
        "text": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
        "note": "OCR is only a candidate transcription; verify every character against the image.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--ocr", action="store_true", help="Run local Tesseract OCR when available")
    parser.add_argument("--ocr-language", default="chi_sim+eng")
    args = parser.parse_args()

    with Image.open(args.image) as image:
        report: dict[str, Any] = {
            "source_file": args.image.name,
            "pixel_dimensions": {"width": image.width, "height": image.height},
            "format": image.format,
            "mode": image.mode,
            "exif": extract_exif(image),
            "warnings": [
                "File timestamps and upload time are not capture evidence.",
                "Do not infer a place name from scenery or GPS without reliable confirmation.",
            ],
        }
    if args.ocr:
        report["ocr"] = run_ocr(args.image, args.ocr_language)
    else:
        report["ocr"] = {"status": "not_requested", "text": ""}

    payload = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)


if __name__ == "__main__":
    main()
