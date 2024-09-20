---
draft: false
toc: true
comments: false
categories:
- Development
tags:
- VS Code
- TypeScript
title: "VS Code Extension Development Notes"
wip: true
snippet: "Notes about creating a Visual Studio Code extension."
---

# Storage
Four types of storage (`ExtensionContext` is passed to the `activate` method as `context`):

* `ExtensionContext.workspaceState`: A workspace storage where you can write
  key/value pairs. VS Code manages the storage and will restore it when the same
  workspace is opened again.
* `ExtensionContext.globalState`: A global storage where you can write key/value
  pairs. VS Code manages the storage and will restore it for each extension
  activation. You can selectively synchronize key/value pairs in global storage
  by setting the keys for sync using `setKeysForSync` method on `globalState`.
* `ExtensionContext.storageUri`: A workspace specific storage URI pointing to a
  local directory where your extension has read/write access. This is a good
  option if you need to store large files that are accessible only from the
  current workspace.
* `ExtensionContext.globalStorageUri`: A global storage URI pointing to a local
  directory where your extension has read/write access. This is a good option if
  you need to store large files that are accessible from all workspaces.

Source: https://code.visualstudio.com/api/extension-capabilities/common-capabilities#data-storage

Example code:

```ts
export function activate(context: vscode.ExtensionContext) {
    // The following usually happens in a registerCommand.

    // If the key does not exist in the storage, it will return `undefined`.
    let configPath: vscode.Uri | undefined =
        context.globalState.get<vscode.Uri>("config_path");
    // Check if the value exists or if it's undefined.
    if (configPath === undefined) {
        // We don't have this path so we assume we're starting from scratch.
        // Get a path from globalStorageUri.
        // This will return a Uri.
        configPath = context.globalStorageUri;
        // The parent directory exists, but the child directory must be created.
        // e.g., /home/parsia/.vscode-server/data/User/globalStorage/undefined_publisher.borrowed-time
        vscode.workspace.fs.createDirectory(configPath).then(() => {
            console.log("Created the global storage path: " + configPath);
            // Store this path in `config_path`.
            context.globalState.update("config_path", configPath);

            // Store the default config in the config path.
        });
    }

    // If we want to delete the key/value pair from globalState or workspaceState,
    // we must replace its value with `undefined`.
    context.globalState.update("config_path", undefined);
}
```

# Validate the Input from an InputBox
The `validateInput` callback does it. In this example, we're checking if the
input is empty. If they press enter when it's empty, the `Please enter a ...`
message will be shown in red under the input box and they cannot continue. The
user can always use escape to cancel the flow.

```ts
let newProject = vscode.commands.registerCommand(
    "borrowed-time.newproject",
    async () => {
        // Get project name from the user.
        const projectName = await vscode.window.showInputBox({
        placeHolder: "",
        prompt: "New Project's Name",
        // Do not let user input an empty project name.
        validateInput: (text) => {
            if (text !== "") return null;
            else {
            return "Please enter a project name";
            }
        },
        });
    }
// Do something with projectName.
);
```