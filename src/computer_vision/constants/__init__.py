#******************************************************************************
# Table Dimensions
# ******************************************************************************

"""  
            All dimensions are in mm

                  table_height
     ◄──────────────────────────────────────►
     ┌──────────────────────────────────────┐▲
     │                                      ││
     │ ┌───────────============───────────┐ ││
     │ │                plr_width        ▲│ ││
     │ │ bumper_width   ◄►               ││ ││
     │ │ ◄► ┌┐          ┌┐          ┌┐   ││ ││
─────┼─┼────┼┼──────────┼┼──────────┼┼───┼┼─┼┼────
     │ │    └┘.         └┘          └┘   ││ ││
     │ │    ┌┐          ┌┐          ┌┐   ││ ││
─────┼─┼────┼┼──────────┼┼──────────┼┼───┼┼─┼┼────
     │ │    └┘          └┘  plr_gap └┘   ││ ││
     │ │    ┌┐          ┌┐◄────────►┌┐   ││ ││
─────┼─┼────┼┼──────────┼┼──────────┼┼───┼┼─┼┼────
     │ │    └┘          └┘          └┘   ││ ││
     │ │                    field_width  ││ ││  table_width
     │ │    ┌┐          ┌┐          ┌┐   ││ ││
─────┼─┼────┼┼──────────┼┼──────────┼┼───┼┼─┼┼────
     │ │    └┘          └┘          └┘   ││ ││
     │ │    ┌┐          ┌┐          ┌┐   ││ ││
─────┼─┼────┼┼──────────┼┼──────────┼┼───┼┼─┼┼────
     │ │    └┘          └┘          └┘   ││ ││
     │ │    ┌┐          ┌┐          ┌┐   ││ ││
─────┼─┼────┼┼──────────┼┼──────────┼┼───┼┼─┼┼────
     │ │    └┘          └┘          └┘   ││ ││
     │ │            field_height         ││ ││
     │ │◄───────────────────────────────►▼│ ││
     │ └───────────============───────────┘ ││
     │                                      ││
     └──────────────────────────────────────┘▼
"""
TABLE_HEIGHT = 675.0
TABLE_WIDTH = 370.0

PLR_WIDTH = 14.0
PLR_GAP = 95.0
BUMPER_WIDTH = 10.0

FIELD_WIDTH = 346.0
FIELD_HEIGHT = 600.0


#******************************************************************************
# Camera Constants
# ******************************************************************************

FPS = 60
CAMERA_ID = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480


