knob_dia = 6;
knob_height =12;
knob_flat = 4.5;
$fn=32;

module spindle_hole()
{
    difference()
    {
        cylinder(d=knob_dia+0.5,h=knob_height);
        translate([knob_flat - (knob_dia/2)+0.25,-5,-1]) cube([10,10,knob_height+2]);
        translate([knob_flat - (knob_dia/2)+.5,0,-1]) cylinder(d=1,h=knob_height+2, $fn=16);
    }
}

module knob_outer()
{
    union()
    {
        cylinder(d1=15,d2=13,h=knob_height+3);
        difference()
        {
            cylinder(d1=15.5,d2=13.5,h=knob_height+3);
            translate([0,0,(knob_height+3)/2]) rotate([0,0,0]) cube([2,18,knob_height+5], center=true);
            translate([0,0,(knob_height+3)/2]) rotate([0,0,45]) cube([2,18,knob_height+5], center=true);
            translate([0,0,(knob_height+3)/2]) rotate([0,0,90]) cube([2,18,knob_height+5], center=true);
            translate([0,0,(knob_height+3)/2]) rotate([0,0,-45]) cube([2,18,knob_height+5], center=true);
        }
    }
}

module knob_complete()
{
    difference()
    {
        knob_outer();
        translate([0,0,-0.1]) spindle_hole();
    }
}

knob_complete();