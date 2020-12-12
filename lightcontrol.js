import xapi from 'xapi';

async function sendPayload(light, payload) {
  xapi.command("HttpClient Post", {
      'Url': 'http://Pi3:8081/tradfri/' + light,
      'Header': 'Content-Type: application/json',
      'Timeout': 2,
    },
    JSON.stringify(payload))
}

xapi.event.on("CallSuccessful", async (event) => {
  sendPayload('Desk%20spot', { 'state': 0 });
  // There's some race in the server
  // It can't receive messages too fast. Oops.
  setTimeout(() => {
    sendPayload('Office%20spot', { 'state': 1 });
  }, 500);
  console.log("Call", event);
});

xapi.event.on("CallDisconnect", async (event) => {
  sendPayload('Desk%20spot', { 'state': 1 });
  setTimeout(() => {
    sendPayload('Office%20spot', { 'state': 0 });
  }, 500);
  console.log("Disconnect", event);
});

