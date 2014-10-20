#include <LiquidCrystal.h>
#define RS 3  // Register Select
#define E 4  // Enable
#define D4 8  // Datenleitung 4
#define D5 9  // Datenleitung 5
#define D6 10  // Datenleitung 6
#define D7 11  // Datenleitung 7
#define COLS 20 // Anzahl der Spalten
#define ROWS 4  // Anzahl der Zeilen

char message[20];
boolean flag = false;

LiquidCrystal lcd(RS, E, D4, D5, D6, D7); // Objekt instanziieren

void setup(){
  lcd.begin(COLS, ROWS);  // Anzahl der Spalten und Zeilen
  lcd.setCursor(0, 1);  // In die 2. Zeile wechseln
  lcd.print("Willkommen zu");
  lcd.setCursor(0, 2);  // In die 2. Zeile wechseln
  lcd.print("Weather Monitor v0.2"); // Ausgabe des Textes  
  Serial.begin(9600);
}

void loop() {
  if(Serial.available() > 0) {
  static int i =0;
  if(i == 0) {
     lcd.clear();
     i++; 
  }
  lcd.home();
  String foo = Serial.readStringUntil('\n');
  draw_to_screen(foo);
  }
}

void print_string(String message, int column) {
  char buffer[20];
  message.toCharArray(buffer,20); 
  lcd.setCursor(0,column); 
  lcd.write(buffer);  
}

void draw_to_screen(String message) {
  //check if string is to long
  static int count = 0;
  
  if(count == 4){
    lcd.clear();
    count = 0;
    lcd.home();
  }
  
  if(message.length() > 20) {
     //print first string
     String temp = message.substring(0,19);
     print_string(temp,count);
     temp = message.substring(19,message.length());
     print_string(temp,count+1);
  } else { 
  print_string(message,count);
  }
    count++;
}
