$fn=24;

HOLE_1_X = 1.905;
HOLE_1_Y = 1.905;
HOLE_2_X = 48.895;
HOLE_2_Y = 29.845;

BOARD_X = 51.0;
BOARD_Y = 32;
BOX_X = 71;
BOX_Y = 40;
BOARD_HEIGHT = 1.6;
BOARD_CLEARANCE = 4.0;


SCREW_TERMINAL_X = 29.4;
SCREW_TERMINAL_Y = 2.9;
SCREW_TERMINAL_WX = 21;
SCREW_TERMINAL_WY = 7;
SCREW_TERMINAL_WZ = 9;

BASE_THICKNESS = 3;
ROUNDNESS = 6;

BOX_HEIGHT = BOARD_CLEARANCE+SCREW_TERMINAL_WZ;

module base() {
    translate([0, 0, -BASE_THICKNESS]) 
    linear_extrude(height=BASE_THICKNESS) 
    offset(r=ROUNDNESS) square([BOX_X, BOX_Y]);
}

module plug_hole() {
    plug_dia = 11;
    plug_thickness = 15;
    translate([BOARD_X+5+7, BOX_Y, 6])
    rotate([-90, 0, 0])
    union() {
        cylinder(d=plug_dia, h=plug_thickness, center=true);
        translate([0, -(plug_dia/2), plug_dia/2])
        cube(plug_dia, center=true);
    }
}

module base_wall() {
    union() {
        difference() {
            difference() {
                linear_extrude(height=BOX_HEIGHT) offset(r=ROUNDNESS) square([BOX_X, BOX_Y]);
                translate([0,0,-1]) linear_extrude(height=BOX_HEIGHT+2) offset(r=1) square([BOX_X, BOX_Y]);
            }
            
            // screw terminal hole
            translate([SCREW_TERMINAL_X, -SCREW_TERMINAL_WY, -1])
            cube([SCREW_TERMINAL_WX, SCREW_TERMINAL_WY*2, BOARD_CLEARANCE+SCREW_TERMINAL_WZ+2]);
    
            plug_hole();
        }
        
        hull() {
            y_corner = BOX_Y+3;
            dx=-3;
            size=8;
            translate([dx, y_corner, 0]) cube([1, 1, BOX_HEIGHT]);
            translate([dx, y_corner-size, 0]) cube([1, 1, BOX_HEIGHT]);
            translate([dx+size, y_corner, 0]) cube([1, 1, BOX_HEIGHT]);

        }
        hull() {
            x_corner = BOX_X+3;
            dy=-3;
            size=8;
            translate([x_corner, dy, 0]) cube([1, 1, BOX_HEIGHT]);
            translate([x_corner-size, dy, 0]) cube([1, 1, BOX_HEIGHT]);
            translate([x_corner, dy+size, 0]) cube([1, 1, BOX_HEIGHT]);
        }

    }
    
}

module mounting_holes() {
    translate([HOLE_1_X, HOLE_1_Y, -3])
    cylinder(r=1, h=6);
    translate([HOLE_2_X, HOLE_2_Y, -3])
    cylinder(r=1, h=6);
}

module lid_screws() {
    z_fudge=5;
    screw_dia=2;
    roundness_fudge=screw_dia/2;
    translate([BOX_X+roundness_fudge, -roundness_fudge, -z_fudge]) cylinder(d=screw_dia, h=BOX_HEIGHT+(2*z_fudge));
    translate([-roundness_fudge, BOX_Y+roundness_fudge, -z_fudge]) cylinder(d=screw_dia, h=BOX_HEIGHT+(2*z_fudge));
}

module bottom() {
    union() {
        difference() {
            base();
            mounting_holes();
        }
        difference() {
            base_wall();
            lid_screws();
        }
    }
}

module top() {
    //translate([0, 0, BOARD_CLEARANCE+SCREW_TERMINAL_WZ+5])
    translate([0, 0, BASE_THICKNESS])
    difference() {
        base();
        lid_screws();
    }
}

module plug() {
    translate([7, 0, 6])
    rotate([-90, 0, 0])
    hull() {
        cylinder(h=37, d=10);
        translate([0, 0, 5])
        cube([14, 12, 10], center=true);
    }
}


bottom();
//top();

//%translate([BOARD_X+5, 8, 0])
//plug();
//
