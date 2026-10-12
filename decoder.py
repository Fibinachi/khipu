"""Defensible Inca khipu number decoder.

Based on Ascher & Ascher, Urton, and OKR conventions:
- Decimal positional notation along pendant cord
- Units cluster nearest the FREE END (largest START_POS, measured from main cord)
- Units: L knot -> NUM_TURNS (digits 2-9); E/EE -> 1; empty -> 0
- Tens/hundreds/thousands: count of S knots = digit; empty -> 0
- TF treated as S-equivalent (positional, value 1 each) per OKR
- SP treated as L-equivalent (digit by turns) per OKR
- LL, BL treated as L-equivalent

Returns (value, confidence, notes). Confidence is 'high' only when:
- All clusters follow standard type/position rules
- No NULL/0-turn L knots in units
- No anomalous turn counts

Anything else gets flagged.
"""

import sqlite3

def decode_cord(conn, cord_id):
    """Decode the numerical value of a single cord.
    Returns dict with value, confidence, notes, clusters.
    """
    c = conn.cursor()
    c.execute("""
        SELECT kc.CLUSTER_ID, kc.ORDINAL, kc.START_POS, kc.NUM_KNOTS
        FROM knot_cluster kc
        WHERE kc.CORD_ID = ?
        ORDER BY kc.START_POS DESC
    """, (cord_id,))
    clusters = c.fetchall()
    
    if not clusters:
        return {'value': 0, 'confidence': 'high', 'notes': 'no clusters (empty cord = 0)',
                'clusters': []}
    
    value = 0
    notes = []
    confidence = 'high'
    cluster_info = []
    
    for place, (cl_id, ordinal, start_pos, num_knots) in enumerate(clusters):
        c.execute("""
            SELECT TYPE_CODE, NUM_TURNS, COUNT(*) as n
            FROM knot WHERE CLUSTER_ID = ?
            GROUP BY TYPE_CODE, NUM_TURNS
        """, (cl_id,))
        knots = c.fetchall()
        
        digit = 0
        cl_notes = []
        
        if place == 0:
            # UNITS position: expect single L (turns=digit 2-9), E/EE (=1), or empty
            total_knots = sum(n for _, _, n in knots)
            if total_knots == 0:
                digit = 0
            elif len(knots) == 1:
                tcode, turns, n = knots[0]
                if tcode in ('L', 'SP', 'LL', 'BL') and n == 1:
                    if turns is None or turns == 0:
                        return {'value': None, 'confidence': 'low',
                                'notes': f'L-type with NULL/0 turns in units',
                                'clusters': cluster_info}
                    elif turns > 9 or turns < 1:
                        return {'value': None, 'confidence': 'low',
                                'notes': f'L-type with {turns} turns in units (anomalous)',
                                'clusters': cluster_info}
                    else:
                        digit = int(turns)
                        if digit < 2:
                            confidence = 'medium'
                            cl_notes.append(f'L with {digit} turn(s), standard is 2-9')
                elif tcode in ('E', 'EE') and n == 1:
                    digit = 1
                elif tcode == 'S':
                    confidence = 'low'
                    cl_notes.append(f'S knot in units (non-standard)')
                    digit = 0  # cannot determine; flag
                elif tcode == 'TF':
                    confidence = 'medium'
                    cl_notes.append(f'TF in units (marker?)')
                    digit = 0
                else:
                    confidence = 'low'
                    cl_notes.append(f'{tcode} x{n} in units (non-standard)')
                    digit = 0
            else:
                # Multiple knot groups in units = non-standard
                confidence = 'low'
                cl_notes.append(f'multiple knot types/groups in units: {knots}')
                # Try: if it's E's only, could be tally? Flag as unknown.
                return {'value': None, 'confidence': 'low',
                        'notes': f'multiple knot groups in units: {knots}',
                        'clusters': cluster_info}
        else:
            # TENS+ positions: expect S knots, count = digit
            for tcode, turns, n in knots:
                if tcode == 'S':
                    digit += n
                elif tcode == 'TF':
                    digit += n  # OKR treats as positional value 1 each
                    cl_notes.append(f'TF counted as S-equivalent')
                    if confidence == 'high':
                        confidence = 'medium'
                elif tcode == 'L' or tcode == 'E' or tcode == 'EE':
                    confidence = 'low'
                    cl_notes.append(f'{tcode} in {place*10}s position (non-standard)')
                else:
                    confidence = 'low'
                    cl_notes.append(f'unknown type {tcode} in {place*10}s')
        
        if digit is None:
            digit = 0
        value += digit * (10 ** place)
        cluster_info.append({
            'cluster_id': cl_id, 'place': 10**place, 'digit': digit,
            'knot_types': [(t, tr, n) for t, tr, n in knots],
            'notes': cl_notes
        })
        notes.extend(cl_notes)
    
    return {'value': value, 'confidence': confidence,
            'notes': '; '.join(notes) if notes else 'standard',
            'clusters': cluster_info}


def decode_khipu(conn, khipu_id, level=1):
    """Decode all level-N cords of a khipu. Returns {cord_id: result}."""
    c = conn.cursor()
    c.execute("""
        SELECT CORD_ID, CORD_ORDINAL FROM cord
        WHERE KHIPU_ID = ? AND CORD_LEVEL = ?
        ORDER BY CORD_ORDINAL
    """, (khipu_id, level))
    cords = c.fetchall()
    return {cid: decode_cord(conn, cid) for cid, _ in cords}
