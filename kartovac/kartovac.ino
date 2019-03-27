void setup() {
  char cards[4][16] = {"127FB2B6", "E47F410E", "ACFA5B47", "A455420E"};

  Serial.begin(9600);
  randomSeed(analogRead(A0));
  Serial.println(cards[random(0,3)]);
}

void loop() {

}
