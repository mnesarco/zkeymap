from zkeymap.model import Layout, rc


layout = Layout("marz_split_3x6_4", description="Corn like split but 3x6_4")

# Row 0
layout / [
    # Left
    rc(x=0, y=0.75),
    rc(x=1, y=0.75),
    rc(x=2, y=0.25),
    rc(x=3),
    rc(x=4, y=0.35),
    rc(x=5, y=0.45),
    # Right
    rc(x=10, y=0.45),
    rc(x=11, y=0.35),
    rc(x=12),
    rc(x=13, y=0.25),
    rc(x=14, y=0.75),
    rc(x=15, y=0.75),
]

# Row 1
layout.duplicate_row()

# Row 2
layout.duplicate_row()

d = 0.5
# Row 3 - Thumbs row
layout / [
    None,
    None,
    # Left
    rc(x=3.9, y=3.5, r=10),
    rc(x=5.0, y=3.7, r=18),
    rc(x=6.1, y=4.1, r=27),
    rc(x=7.1, y=4.6, r=32),
    # Right

    rc(x=7.9+d,  y=4.85, r=-32, rx=9),
    rc(x=8.85+d, y=4.30, r=-27, rx=10),
    rc(x=9.85+d, y=3.85, r=-18.5, rx=11),
    rc(x=10.9+d, y=3.55, r=-10, rx=12),
]
