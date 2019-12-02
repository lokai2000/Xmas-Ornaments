Tol=0.5;

module orn(){
  translate([0,0,25]) sphere(d=50,$fn=128);
}

module base(){
  intersection(){
    orn();
    cylinder(h=25,d2=10, d1=60, $fn=128, center=false);
  }
}

module baseT(){
  cylinder(h=25,d2=10+Tol, d1=60+Tol, $fn=128, center=false);
}


module ring(){
  difference(){  
    intersection(){
      translate([0,0,10]) cylinder(h=10, d=60, $fn=128, center=false);
      orn();
    }
    translate([0,0,5]) import("screwOuterOutset.stl"); 
    baseT();   
  }
}

module bottom(){
  difference(){
    intersection(){
      union(){
        base();
        translate([0,0,5]) import("screwOuterInset.stl"); 
      }
      cylinder(h=28,d=42);
    }
    translate([0,0,4.5]) cylinder(h=22.5,d=25,$fn=64);
    translate([0,0,4.5]) cylinder(h=25,d=12,$fn=64);
  }
}

module top(){
    difference(){
      union(){  
        intersection(){
          orn();
          translate([0,0,20+Tol]) cylinder(h=50, d=60, $fn=128, center=false);      
        }
        translate([0,0,52]) rotate([90,0,0]) rotate_extrude(angle = 360, convexity = 10, $fn=32)
        translate([7, 0, 0])
        circle(r=2.5, $fn=32);
      }
      translate([0,0,25]) intersection(){
        scale([1,1,0.9]) sphere(d=50-2.4,$fn=128);
        translate([0,0,5]) cylinder(h=40,d=100);
      }
      translate([0,0,5]) import("screwOuterOutset.stl");     
      //translate([0,0,35]) cylinder(h=10,d2=5, d1=30, $fn=128, center=false);
    }
}


//top();

rotate([180,0,0]) bottom();

//rotate([180,0,0])  ring();
