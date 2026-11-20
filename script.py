#!/usr/bin/env python3

import img2pdf
import os
import sys
import logging

# -----------------------------
# CONFIGURATION
# -----------------------------
INPUT_FOLDER = "images/12"
OUTPUT_PDF = "The_Apothecary_Diaries_12.pdf"

# -----------------------------
# LOGGING SETUP
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# -----------------------------
# FUNCTIONS
# -----------------------------


def get_images(folder):
    logging.info(f"Scanning folder: {folder}")

    if not os.path.exists(folder):
        logging.error(f"Folder does not exist: {folder}")
        sys.exit(1)

    images = sorted([
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])

    if not images:
        logging.error("No images found in the folder.")
        sys.exit(1)

    logging.info(f"Total images found: {len(images)}")
    return images


def create_pdf(images, output_file):
    try:
        logging.info("Starting PDF conversion...")

        with open(output_file, "wb") as f:
            pdf_bytes = img2pdf.convert(
                images,
                rotation=img2pdf.Rotation.ifvalid  # Fix EXIF issue
            )
            f.write(pdf_bytes)

        logging.info(f"PDF successfully created: {output_file}")

    except img2pdf.ExifOrientationError as e:
        logging.error("EXIF orientation error detected.")
        logging.error(str(e))
        sys.exit(1)

    except Exception as e:
        logging.exception("Unexpected error during PDF creation:")
        sys.exit(1)


# -----------------------------
# MAIN
# -----------------------------
def main():
    logging.info("=== Image to PDF Script Started ===")

    images = get_images(INPUT_FOLDER)
    create_pdf(images, OUTPUT_PDF)

    logging.info("=== Process Completed Successfully ===")


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    main()
