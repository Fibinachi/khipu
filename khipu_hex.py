"""Serialize khipu to hexadecimal. Each cord = 4 bytes. Khipu = hex stream.

Byte layout per cord:
  Byte 0: color_id (6 bits) | knot_type (2 bits high)
  Byte 1: knot_type (1 bit low) | direction (2 bits) | level (3 bits) | flags (2 bits)
  Byte 2-3: decoded value, big-endian uint16

Header (8 bytes):
  Bytes 0-3: magic "KHPU"
  Byte 4: format version (0x01)
  Byte 5: document type (0x01=census, 0x02=warehouse, 0x03=tally,
           0x04=sparse, 0x05=south_funerary, 0x06=unknown_office, 0x00=unclassified)
  Bytes 6-7: cord count, big-endian uint16
"""
import sqlite3
import sys
sys.path.insert(0, '/home/hatch/workspace/quipu-analysis')
from decoder import decode_cord

# Lookup tables
KNOT_TYPES = {'S': 0, 'L': 1, 'E': 2, 'EE': 3, 'SP': 4, 'TF': 5, 'LL': 6, 'BL': 7}
DIRECTIONS = {'Z': 0, 'S': 1, 'U': 2}
DOC_TYPES = {
    'census_format_paired': 0x01,
    'deep_hierarchical_grouped': 0x02,
    'large_value_flat': 0x03,
    'deep_sparse_mixed': 0x04,
}

# Build color table from DB
def build_color_table(conn):
    c = conn.cursor()
    c.execute("SELECT DISTINCT COLOR_CD_1 FROM ascher_cord_color WHERE COLOR_CD_1 IS NOT NULL ORDER BY COLOR_CD_1")
    colors = [r[0] for r in c.fetchall()]
    return {col: i for i, col in enumerate(colors)}

def get_doc_type(conn, khipu_id):
    c = conn.cursor()
    # Check cluster file
    try:
        with open('/home/hatch/workspace/quipu-analysis/khipu-clusters-2026-10-11.csv') as f:
            for line in f:
                if line.startswith('#') or line.startswith('KHIPU'):
                    continue
                parts = line.strip().split(',')
                if parts[0] == str(khipu_id) and len(parts) >= 3:
                    return DOC_TYPES.get(parts[2], 0x00)
    except FileNotFoundError:
        pass
    return 0x00

def serialize_khipu(khipu_id):
    conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
    color_table = build_color_table(conn)
    c = conn.cursor()

    c.execute("""
        SELECT c.CORD_ID, c.CORD_ORDINAL, c.CORD_LEVEL, cc.COLOR_CD_1
        FROM cord c
        LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
        WHERE c.KHIPU_ID = ?
        ORDER BY c.CORD_ORDINAL
    """, (khipu_id,))
    cords = c.fetchall()

    # Header
    doc_type = get_doc_type(conn, khipu_id)
    header = b'KHPU' + bytes([0x01, doc_type]) + len(cords).to_bytes(2, 'big')

    body = b''
    for cord_id, ordinal, level, color in cords:
        # Byte 0: color (6 bits) | knot_type_high (2 bits)
        color_id = color_table.get(color, 0) & 0x3F

        # Dominant knot type and direction
        c2 = conn.cursor()
        c2.execute("""
            SELECT TYPE_CODE, DIRECTION, COUNT(*) as n FROM knot
            WHERE CORD_ID = ? GROUP BY TYPE_CODE, DIRECTION ORDER BY n DESC LIMIT 1
        """, (cord_id,))
        row = c2.fetchone()
        knot_code = KNOT_TYPES.get(row[0], 0) if row else 0
        direction = DIRECTIONS.get(row[1], 0) if row and row[1] else 0

        byte0 = (color_id << 2) | ((knot_code >> 1) & 0x03)
        # Byte 1: knot_low (1) | direction (2) | level (3) | reserved (2)
        lvl = min(level or 0, 7)
        byte1 = ((knot_code & 0x01) << 7) | ((direction & 0x03) << 5) | ((lvl & 0x07) << 2)

        # Bytes 2-3: value
        result = decode_cord(conn, cord_id)
        val = result['value'] or 0
        val = min(max(val, 0), 65535)

        body += bytes([byte0, byte1]) + val.to_bytes(2, 'big')

    conn.close()
    return header + body

def hexdump(data, width=16):
    lines = []
    for i in range(0, len(data), width):
        chunk = data[i:i+width]
        hexpart = ' '.join(f'{b:02x}' for b in chunk)
        asciipart = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        lines.append(f'{i:08x}  {hexpart:<{width*3}}  |{asciipart}|')
    return '\n'.join(lines)

def main():
    khipu_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1000270
    data = serialize_khipu(khipu_id)
    print(f"\nKHIPU {khipu_id} → {len(data)} bytes ({len(data)//4} cords + 8-byte header)\n")
    print(hexdump(data[:8 + 16*4]))  # header + first 16 cords
    if len(data) > 8 + 64:
        print(f"  ... ({len(data) - 72} more bytes)")
    print()

if __name__ == '__main__':
    main()
