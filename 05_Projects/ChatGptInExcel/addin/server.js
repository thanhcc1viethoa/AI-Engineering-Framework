const fs = require("fs");
const https = require("https");
const path = require("path");
const devCerts = require("office-addin-dev-certs");

const root = path.join(__dirname, "src");
const port = Number(process.env.PORT || 3000);

const contentTypes = {
  ".css": "text/css",
  ".html": "text/html",
  ".js": "text/javascript",
  ".json": "application/json",
  ".png": "image/png",
  ".svg": "image/svg+xml"
};

const iconPng = Buffer.from(
  "iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAAfUlEQVR4nO3QMQEAAAgDINc/9K3hBwwk0h5mZgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwGcB0kAAAW7mG9QAAAAASUVORK5CYII=",
  "base64"
);

function send(res, status, body, type = "text/plain") {
  res.writeHead(status, {
    "Content-Type": type,
    "Cache-Control": "no-store"
  });
  res.end(body);
}

function resolveFile(urlPath) {
  const cleanPath = decodeURIComponent(urlPath.split("?")[0]);
  const relativePath = cleanPath === "/" ? "taskpane.html" : cleanPath.replace(/^\/+/, "");
  const filePath = path.normalize(path.join(root, relativePath));

  if (!filePath.startsWith(root)) {
    return null;
  }

  return filePath;
}

async function main() {
  const options = await devCerts.getHttpsServerOptions();

  https
    .createServer(options, (req, res) => {
      if ((req.url || "").startsWith("/assets/icon-")) {
        send(res, 200, iconPng, "image/png");
        return;
      }

      const filePath = resolveFile(req.url || "/");

      if (!filePath) {
        send(res, 403, "Forbidden");
        return;
      }

      fs.readFile(filePath, (err, data) => {
        if (err) {
          send(res, 404, "Not found");
          return;
        }

        send(res, 200, data, contentTypes[path.extname(filePath)] || "application/octet-stream");
      });
    })
    .listen(port, () => {
      console.log(`ChatGPT in Excel add-in server running at https://localhost:${port}`);
      console.log("Use npm run excel to sideload the manifest into Excel.");
    });
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
