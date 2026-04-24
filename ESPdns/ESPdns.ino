#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "DUC MINH";
const char* pass = "24042011ken";

WebServer server(80);

String peers[64];
unsigned long lastSeen[64];
int peerCount = 0;

int findPeer(String ip)
{
  for(int i=0;i<peerCount;i++)
    if(peers[i]==ip) return i;
  return -1;
}

void addPeer(String ip)
{
  int idx = findPeer(ip);

  if(idx >= 0)
  {
    lastSeen[idx] = millis();
    return;
  }

  if(peerCount < 64)
  {
    peers[peerCount] = ip;
    lastSeen[peerCount] = millis();
    peerCount++;
  }
}

void cleanupPeers()
{
  for(int i=0;i<peerCount;i++)
  {
    if(millis() - lastSeen[i] > 300000)
    {
      for(int j=i;j<peerCount-1;j++)
      {
        peers[j]=peers[j+1];
        lastSeen[j]=lastSeen[j+1];
      }
      peerCount--;
      i--;
    }
  }
}

void handlePeers()
{
  String json = "[";

  for(int i=0;i<peerCount;i++)
  {
    json += "\"" + peers[i] + "\"";
    if(i < peerCount-1) json += ",";
  }

  json += "]";
  server.send(200,"application/json",json);
}

void handleHeartbeat()
{
  String ip = server.client().remoteIP().toString();
  addPeer(ip);

  server.send(200,"text/plain","ok");
}

void setup()
{
  Serial.begin(115200);

  WiFi.begin(ssid, pass);
  while(WiFi.status()!=WL_CONNECTED) delay(500);

  Serial.println(WiFi.localIP());

  server.on("/peers", HTTP_GET, handlePeers);
  server.on("/heartbeat", HTTP_POST, handleHeartbeat);

  server.begin();
}

void loop()
{
  server.handleClient();
  cleanupPeers();
}
