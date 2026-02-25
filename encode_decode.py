#!/usr/bin/env python3
import sys
import argparse

def to_bits(s: str) -> str:
    b = ''.join(f'{ord(ch):08b}' for ch in s)
    return b

def from_bits(bits: str) -> str:
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        chars.append(chr(int(byte, 2)))
    return ''.join(chars)

def encode_text(input_path: str, message: str, out_path: str):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    bits = to_bits(message)
    # add a delimiter so decoding knows where to stop
    delimiter = '11111111'  # 0xFF
    bits += delimiter

    # ensure enough lines
    if len(bits) > len(lines) * 1:  # 1 bit per line
        # extend by repeating lines (wrap) but keep simple: append empty lines
        need = (len(bits) - len(lines))
        for _ in range(need):
            lines.append('\n')

    new_lines = []
    for i, line in enumerate(lines):
        bit = bits[i] if i < len(bits) else None
        if bit is None:
            new_lines.append(line)
            continue
        # strip trailing whitespace, then append encoded space/tab
        stripped = line.rstrip('\r\n')
        endchar = ' ' if bit == '0' else '\t'
        new_lines.append(stripped + endchar + '\n')

    with open(out_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

def decode_text(input_path: str) -> str:
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    bits = []
    for line in lines:
        if line.rstrip('\r\n').endswith(' '):
            bits.append('0')
        elif line.rstrip('\r\n').endswith('\t'):
            bits.append('1')
        else:
            # no hidden bit on this line; stop if we already collected delimiter
            bits.append(None)

    # drop trailing None
    bits = [b for b in bits if b is not None]

    # convert bits to text until delimiter 0xFF is found
    bits_str = ''.join(bits)
    # split by 8-bit chunks including possible extra bits after delimiter
    # find delimiter
    delim_index = bits_str.find('11111111')
    if delim_index != -1:
        bits_str = bits_str[:delim_index]

    return from_bits(bits_str)

def main():
    ap = argparse.ArgumentParser(description='Steganographic text encoder/decoder using trailing spaces and tabs.')
    sub = ap.add_subparsers(dest='cmd', required=True)

    en = sub.add_parser('encode', help='Hide a message in a text file')
    en.add_argument('input', help='Input text file path')
    en.add_argument('message', help='Message to hide')
    en.add_argument('output', help='Output text file path with hidden data')

    de = sub.add_parser('decode', help='Extract hidden message from a text file')
    de.add_argument('input', help='Input text file path with hidden data')

    args = ap.parse_args()

    if args.cmd == 'encode':
        encode_text(args.input, args.message, args.output)
    else:
        msg = decode_text(args.input)
        print(msg)

if __name__ == '__main__':
    main()