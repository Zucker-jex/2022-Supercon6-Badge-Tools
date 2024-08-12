# By Jex Zucker
import sys
import os
import shutil
import time


def hex2bin(hexfile, binfile):
    with open(hexfile, "r") as f_hex, open(binfile, "wb") as f_bin:
        for line in f_hex:
            if line.startswith(":"):
                byte_count = int(line[1:3], 16)
                address = int(line[3:7], 16)
                record_type = int(line[7:9], 16)
                data = line[9 : 9 + byte_count * 2]
                if record_type == 0:  # Data record
                    f_bin.write(bytes.fromhex(data))
                elif record_type == 1:  # End of file record
                    break


def process_bin_file(binfile, outputfile, align=64):
    with open(binfile, "rb") as f:
        data = f.read()

    # find 47 45 00 00 4E 53
    start_marker = b"\x47\x45\x00\x00\x4E\x53"
    start_idx = data.find(start_marker)
    if start_idx != -1:
        data = data[start_idx:]

    # find E2 01 00 00 80 00 00 00 00 00 00 00
    end_marker = b"\xE2\x01\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00"
    end_idx = data.find(end_marker)
    if end_idx != -1:
        data = data[: end_idx + len(end_marker)]

    padding_length = (align - len(data) % align) % align
    data += b"\xFF" * padding_length

    with open(outputfile, "wb") as f:
        f.write(data)


if __name__ == "__main__":
    # Default hex file path
    default_hex_file = (
        ".\\Badge_firmware\\dist\\default\\production\\Badge_firmware.production.hex"
    )

    if len(sys.argv) == 2:
        hex_file = sys.argv[1]
    else:
        hex_file = default_hex_file
        print(f"No hex file specified. Using default file: {hex_file}")

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    folder_name = f"Badge_{timestamp}"

    firmware_dir = ".\\firmware"

    os.makedirs(firmware_dir, exist_ok=True)

    full_folder_path = os.path.join(firmware_dir, folder_name)

    os.makedirs(full_folder_path, exist_ok=True)

    copied_hex_file = os.path.join(full_folder_path, f"{folder_name}.hex")
    shutil.copy2(hex_file, copied_hex_file)

    bin_file = os.path.join(full_folder_path, f"{folder_name}.bin")
    final_output = os.path.join(full_folder_path, f"{folder_name}_final.bin")

    hex2bin(copied_hex_file, bin_file)

    process_bin_file(bin_file, final_output, align=16)

    print(
        f"Processing completed. The generated files are saved in the folder: {full_folder_path}"
    )
