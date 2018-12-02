$fn=96;

HOLE_1_X = 1.905;
HOLE_1_Y = 1.905;
HOLE_2_X = 48.895;
HOLE_2_Y = 29.845;

BOARD_X = 51.0;
BOARD_Y = 32;
BOARD_HEIGHT = 1.6;


module pcb(){
    
    difference(){
        color([0.2,1.0,0.5])
        cube([BOARD_X, BOARD_Y, BOARD_HEIGHT]);
        
        translate([HOLE_1_X,HOLE_1_Y, 0])
        cylinder(r=1,h=5);
        
        translate([HOLE_2_X,HOLE_2_Y, 0])
        cylinder(r=1,h=5);
    }
}



module wifi(){
        
    // pcb
    color([0.3,0.3,0.3])
    cube([24.3, 16, 1.0]);
    
    // shield
    translate([1,1,1])
    cube([16.6, 14, 2.1]);
}

module screw_terminal(){
    
    color([0.1,1.0,0.7]) 
    cube([20.8, 6.6, 8.5]);
}

module usb(){
    
    cube([5.8, 7.7, 2.8]);
}


module board(){

    pcb();
    
    translate([0,0,1.6]){
        translate([17.4,5.8,0.0])
        rotate([0,0,90])
        wifi();
        
        translate([29.4,2.9,0.0])
        screw_terminal();
        
        translate([46.3,16.7,0.0])
        usb();
    }
}



board();

