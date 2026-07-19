#include<WiFi.h>
#include<WebServer.h>

const char* password = "JUt9jcRL"; // our password of the WIFI 
const char*ssid = "Domolink_637688_R"; // our WIFI name 
WebServer server(80); // Choose the port of the server 
short value = 0; // our value to compare with and change (in C++ it's essential to size it in advance)
#define Led_pin 2 // our LED pin 

void handle_update(){
  if(server.hasArg("plain")){ // if we have an argument we recieve the data from a device 
    String recieved_data = server.arg("plain"); //get our data
    int value_updated = recieved_data.toInt(); // then keep it 
    value = value_updated; // and change our value into value_updated 
    server.send(200, "text/plain", "OK" ); // in order to get rid of timeout 
  }
  server.send(400, "text/plain", "No data recieved"); // in order to gett rid of timeout too (and to check our status of server response)
}
void handle_get(){

  server.send(200, "text/plain", String(value)); // we need to give our value back in order to check our status in Melody's system (check it in Visual Studio code)
  
}

void setup(){
Serial.begin(115200); // open ESP32 fast port 
WiFi.begin(ssid, password); // connect it with our WiFi
pinMode(Led_pin, OUTPUT); // then define our led as an OUTPUT (being controlled )


while(WiFi.status() != WL_CONNECTED){ 
Serial.println("The board has not been connected to the Wifi"); // If we did not connected to the WiFi just see this line (in order to be aware of this problem)
delay(1500);
}
Serial.print("it has been connected");
Serial.println(WiFi.localIP());  //  IP!!!!!! paste it into the Melody's system 

server.on("/update", HTTP_POST, handle_update); // run the function
server.on("/get", HTTP_GET, handle_get); // run the function
server.begin(); //run the server

}

void loop(){
server.handleClient(); // in order to get or transmit our data 
if(value == 1){ 
  digitalWrite(Led_pin, HIGH); // if our value is 0 led is ON
}
else{
  digitalWrite(Led_pin, LOW ); //Unless our led is OFF
}
}