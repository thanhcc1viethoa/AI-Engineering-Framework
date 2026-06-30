/* global Excel, Office */

const statusEl = document.getElementById("status");
const promptEl = document.getElementById("prompt");
const responseEl = document.getElementById("response");
const readSelectionButton = document.getElementById("read-selection");
const copyPromptButton = document.getElementById("copy-prompt");
const openChatGptButton = document.getElementById("open-chatgpt");
const insertResponseButton = document.getElementById("insert-response");

function setStatus(message) {
  statusEl.textContent = message;
}

Office.onReady((info) => {
  if (info.host !== Office.HostType.Excel) {
    setStatus("Open this add-in in Excel.");
    readSelectionButton.disabled = true;
    copyPromptButton.disabled = true;
    openChatGptButton.disabled = true;
    insertResponseButton.disabled = true;
    return;
  }

  setStatus("Ready in Excel.");
});

copyPromptButton.addEventListener("click", async () => {
  try {
    const value = promptEl.value.trim();

    if (!value) {
      setStatus("Read a selection or write a prompt first.");
      return;
    }

    await navigator.clipboard.writeText(value);
    setStatus("Prompt copied.");
  } catch (error) {
    setStatus(`Copy failed: ${error.message}`);
  }
});

openChatGptButton.addEventListener("click", () => {
  window.open("https://chatgpt.com/", "_blank", "noopener,noreferrer");
  setStatus("ChatGPT opened. Paste the copied prompt there.");
});

readSelectionButton.addEventListener("click", async () => {
  try {
    await Excel.run(async (context) => {
      const range = context.workbook.getSelectedRange();
      range.load(["address", "values", "text"]);
      await context.sync();

      const values = range.text || range.values || [];
      promptEl.value = `Selection: ${range.address}\n\n${values.map((row) => row.join("\t")).join("\n")}`;
      setStatus("Selection loaded.");
    });
  } catch (error) {
    setStatus(`Read failed: ${error.message}`);
  }
});

insertResponseButton.addEventListener("click", async () => {
  try {
    const value = responseEl.value.trim();

    if (!value) {
      setStatus("Write a response before inserting.");
      return;
    }

    await Excel.run(async (context) => {
      const range = context.workbook.getSelectedRange();
      range.values = [[value]];
      await context.sync();
      setStatus("Response inserted.");
    });
  } catch (error) {
    setStatus(`Insert failed: ${error.message}`);
  }
});
