$fn=16;
module LCD(){
    cube([47.7+1,51.35+1,3.68-1.6]);
}

module visable_area(){
    cube([43.2,43.2,10]);
}

module PCB(){
    difference(){
        cube([61,51.35,1.6+0.5]);//add 0.5 for extra pin height
        translate([3.5,8.5,-0.1])cylinder(h=1.6+0.2,d=2.5); //changed all r from 3 then changed from 2.8 to 2.5
        translate([3.5,8.5+34.35,-0.1])cylinder(h=1.6+0.2,d=2.5);
        translate([3.5+54,8.5,-0.1])cylinder(h=1.6+0.2,d=2.5);
        translate([3.5+54,8.5+34.35,-0.1])cylinder(h=1.6+0.2,d=2.5);
    }
}

module ribbon(){
    cube([33,1,3.68]);
}
module screen_all(){
   translate([47.7+6.65,0,3.68]) rotate([0,180,0])union(){ 
       color("red") translate([(-6.65),0,-0.5])PCB();
       color("black") translate([-0.5,-0.5,1.6])LCD();
       color("blue") translate([(47.7-43.2)/2,6.55,1.6]) visable_area();
       color("orange") translate([(47.7-33)/2,-1,0])ribbon();
    }
}
screen_all();