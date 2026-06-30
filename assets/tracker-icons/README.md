# Progress-tracker icons (Bestellfortschritt)

16 transparent PNGs, **100 × 100 px, RGBA**. These are the icon + circular frame
for the 5-step order tracker, in every state, for the developer to wire up
dynamically (the active step shifts per email / order status).

## Steps (icons)
| Step | Icon |
|------|------|
| `bestellung` | check |
| `zahlung` | card |
| `produktion` | cog |
| `versand` | truck |
| `lieferung` | house |

## States
| File | State | Frame | Icon |
|------|-------|-------|------|
| `{step}-active.png` | current step ("you are here") | solid teal `#015253` + halo ring `rgba(1,82,83,0.30)` | white |
| `{step}-next.png` | immediate next step | white fill, border `#aac8c8` | `#6da4a4` |
| `{step}-upcoming.png` | later steps | white fill, border `#e0e0e0` | `#cccccc` |
| `completed.png` | any finished step | solid teal `#015253`, no ring | white **check** |

Note: a **completed** step always shows the check (`completed.png`), not its own
icon — so one shared file covers every done step. `bestellung-active.png` is the
check on teal+ring (the order step has no separate glyph).

## Geometry
- Canvas 100 × 100, fully transparent outside the frame.
- Frame circle ø ~76 px, centred. The `active` halo ring extends to ø ~96 px.
- Source icons are the Feather-style 24×24 line icons used inline in the emails.

Generated from the live template SVGs (rendered 1:1 via browser canvas).
