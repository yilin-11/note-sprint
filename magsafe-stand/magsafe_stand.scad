// MagSafe / Qi2 phone stand for the Amazon Basics 25W Qi2.2 charging pad (LACC175).
// Based on the idea of "Apple iPhone MagSafe Stand" (printables.com/model/44465):
// an angled plate holding the charger puck in a pocket, with a push-out hole.
//
// Print flat on its base, no supports: PLA/PETG, 0.2 mm layers, 3 walls, 20% infill.
// Open in OpenSCAD (Customizer works too), then F6 + Export STL.

/* [Charger puck] */
// Measure your puck with calipers; listings say 59.9-60.0 mm.
puck_d = 60.0;
puck_h = 8.1;
// Diametral clearance. Go down to 0.1 for a press fit.
fit = 0.3;
// How far the puck face stands above the plate.
proud = 0.6;

/* [Stand] */
// Plate tilt from horizontal (deg).
angle = 70;
plate_w = 74;
// Plate length along the slope.
plate_l = 125;
plate_t = 11;
plate_r = 12;
// Puck centre along the slope, from the base top. Keep > half the phone height.
puck_c = 88;

base_w = 92;
base_d = 100;
base_h = 7;
base_r = 10;

/* [Cable] */
// Through hole for pushing the puck out or passing a cable that exits the back.
push_d = 24;
// Slot through the plate for a cable that exits the puck's edge.
slot_w = 6.5;
groove_w = 5.0;
groove_h = 4.5;
fillet = 16;

/* [Hidden] */
$fn = 128;
eps = 0.01;
pocket_d = puck_d + fit;
pocket_depth = puck_h - proud;
assert(plate_t - pocket_depth >= 2.5, "plate too thin behind the puck");

// Rear-bottom edge of the plate (y, z), and a point 1 mm inside it to avoid slivers.
back_y = plate_t * sin(angle);
fy = back_y - sin(angle);
fz = base_h - plate_t * cos(angle) + cos(angle);

module rounded_rect(w, h, r) {
    offset(r) square([w - 2 * r, h - 2 * r], center = true);
}

// Plate frame: x across, y up the slope, z out of the front face.
module in_plate() {
    translate([0, 0, base_h]) rotate([angle, 0, 0]) children();
}

module body() {
    translate([0, base_d / 2, 0])
        linear_extrude(base_h) rounded_rect(base_w, base_d, base_r);

    // Plate, rounded at the top only (its bottom is buried in the base).
    in_plate() translate([0, 0, -plate_t]) linear_extrude(plate_t)
        intersection() {
            translate([0, plate_l / 2 + plate_r]) rounded_rect(plate_w, plate_l + 2 * plate_r, plate_r);
            translate([-plate_w / 2, 0]) square([plate_w, plate_l]);
        }

    // Fillet between the plate back and the base top.
    rotate([90, 0, 90]) linear_extrude(plate_w, center = true)
        polygon([[fy, fz], [fy + fillet * 1.6, base_h],
                 [fy + fillet * cos(angle), fz + fillet * sin(angle)]]);
}

difference() {
    body();

    in_plate() {
        // Puck pocket.
        translate([0, puck_c, -pocket_depth]) cylinder(h = pocket_depth + 1, d = pocket_d);
        // Push-out hole.
        translate([0, puck_c, -plate_t - 1]) cylinder(h = plate_t + 2, d = push_d);
        // Cable slot from the hole down through the bottom of the plate.
        translate([-slot_w / 2, -20, -plate_t - 1]) cube([slot_w, puck_c + 20, plate_t + 2]);
    }

    // Slot continues down through the base under the plate...
    translate([-slot_w / 2, -1, -1]) cube([slot_w, back_y + 2, base_h + 1 + eps]);
    // ...and an open groove under the base leads the cable out the back.
    translate([-groove_w / 2, -1, -1]) cube([groove_w, base_d + 2, groove_h + 1]);
}
