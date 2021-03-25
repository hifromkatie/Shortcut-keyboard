//V1.03 added extra space for buttons and for the back plate to slide in

$fn=32;
use <screen_v2.scad>

module switch_cutout(){
    translate([-0.25,-0.25,0])cube([14+0.5,14+0.5,1.5]);
    translate([-2,-2,1.5]) cube([18,18,1.5]);
}
//switch_cutout();

module key_plate(){
    difference(){
        union(){ //add box to leave screen mountings
            cube([110,74+51.35+20+10,3]);
            translate([((110-61)/2)+0.25,74+10+0.25,3]) cube([61-0.6,51.35-0.5,1.6+0.5]);
        }
        //side_edge();
        //translate([110,150,0])rotate([0,0,180])side_edge();
        translate([0,2,0])rotate([90+33.69,0,0]) cube([110,4,4]); //bottom edge
        translate([2,0,0]) rotate([0,-33.69-90,0]) cube([4,150,4]); //lefthand side
        translate([110,150,0])rotate([0,0,180])translate([2,0,0]) rotate([0,-33.69-90,0]) cube([4,150,4]); //righthand side
        
        //grid of switches
        translate([12,12,0]) switch_cutout();
        translate([(12+14+10),12,0]) switch_cutout();
        translate([(12+(10*2)+(14*2)),12,0]) switch_cutout();
        translate([110-14-12,12,0]) switch_cutout();
        
        translate([12,(12+14+10),0]) switch_cutout();
        translate([(12+14+10),(12+14+10),0]) switch_cutout();
        translate([(12+(10*2)+(14*2)),(12+14+10),0]) switch_cutout();
        translate([110-14-12,(12+14+10),0]) switch_cutout();

        translate([12,(12+14*2+10*2),0]) switch_cutout();
        translate([(12+14+10),(12+14*2+10*2),0]) switch_cutout();
        translate([(12+(10*2)+(14*2)),(12+14*2+10*2),0]) switch_cutout();
        translate([110-14-12,(12+14*2+10*2),0]) switch_cutout();
        
        translate([(110-61)/2,74+10,3-(3.68-1.6)]) screen_all();

        
    }
}
//key_plate();

module key_plate_to_print(){
    //trim extra length off
    difference(){
        key_plate();
        translate([0,74+51.35+20-0.5,-2.5]) rotate([6,0,0])cube([110,10+5,3+5]);
    }
}
//key_plate_to_print();

module back_panel(){
    difference(){
        rotate ([6,0,0]) union(){
            cube([110,2,15.4+15]); //slot
            //translate([0,2,0]) cube([110,5,3]);
           translate([2,2,0]) cube([110-4,5,(15.7+15)-1]);
        }
        translate([0,0,-5+0.73])cube([110,10,5]);
        translate([0,149.53-145,0]) cube([110,5,30]);
    }
}
//translate([0,170,0]) back_panel();
module new_back_panel(){
    difference(){
        translate([0,74+51.35+20,-5])rotate([6,0,0])cube([110+4,30,35]);
        translate([0,74+51.35+20+2+2,-20]) cube([110+4,50,60]);
        base();
        translate([0,0,-50]) cube([110+4,74+51.35+20+2+10,50]);
        rotate([6,0,0])translate([2,74+51.35+20+2,-15.9])cube([2,2,3.5]);
        rotate([6,0,0])translate([110,74+51.35+20+2,-15.9])cube([2,2,3.5]);
        #rotate([6,0,0])translate([2,74+51.35-8-2+20+0.25,-15-1]) cube([110,2+8,15+15.4+1]);
        
        translate([110/2,74+51.35+5,15+2])rotate([6,0,0])cube([15,20,10]);//hole for usb
        
    }
}
//rotate([-6-90,0,0])new_back_panel();
new_back_panel();
module base(){
    difference(){
        rotate([6,0,0])
        difference(){
            //rotate([6,0,0]) 
            translate([0,0,-20]) cube([110+4,74+51.35+20+2+10,15+20]);
            //#rotate([6,0,0]) 
            translate([4,4,-20]) cube([110-4,74+51.35+20-2+10,15-2+20]);
            
            #translate([110,120,0])rotate([0,90,0])cylinder(h = 4, d=7);//hole for rotary encoder
            
            translate([2,74+51.35+20,-15.4-1]) cube([110,2,15+15.4]); //slot for back panel
            
            
        }
        //translate([2,74+51.35+20,-15.19-1]) back_panel(); //slot for back panel
        
        translate([0,0,-50]) cube([110+4,74+51.35+20+2+10,50]);
        translate([2,2,0]) key_plate();
        
        //make back square/trim base
        translate([0,74+51.35+20+2+2,-20]) cube([110+4,50,60]);
    }
}


//base();
//translate([2,0,0])key_plate_to_print();
//rotate([0,180,0]) translate([0,0,-15]) rotate([-6,0,0]) base();
//rotate([6,0,0])translate([-2,3,15])rotate([0,180,0])key_plate_to_print();
//translate([0,170,0]) back_panel();
//base();
//color("red") translate([2,2,0]) key_plate();