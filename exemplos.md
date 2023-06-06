
print "Hello, world!";

var a = 1;

while (a < 10) {
  print a;
  a = a + 1;
}

fun printSum(a, b) {
  print a + b;
}

printSum(10,  15);

var x = true;
var y = 100;

if(10 > y or x) {
  print "1";
} else {
  if(10 < y and !x) {
    print "2";
  } else {
    print "3";
  }
}

fun getSum(a, b) {
  return a + b;
}

var sum = getSum(4, 5);

if(sum > 10) {
  print "yes";
} else {
  print "no";
}


