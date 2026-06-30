# Install In Excel

This is a personal sideload build for Excel on the local computer.

## Quick Start

Recommended:

```powershell
cd 05_Projects/ChatGptInExcel/addin
.\Start-ExcelAddin.ps1
```

Manual steps:

```powershell
cd 05_Projects/ChatGptInExcel/addin
npm install
npm run certs
npm run validate
npm run excel
```

`npm run excel` starts Excel with the manifest sideloaded. Keep the local server running while the task pane is open.

## Manual Start

In one terminal:

```powershell
cd 05_Projects/ChatGptInExcel/addin
npm start
```

Then sideload `manifest.xml` into Excel using the Office add-in sideload flow for your Excel version.

## Stop

```powershell
npm run stop
```

## Current Limitation

The Excel add-in shell is installable and can read/write the selected range. Direct ChatGPT account login still requires validation of an official provider-supported integration path.
