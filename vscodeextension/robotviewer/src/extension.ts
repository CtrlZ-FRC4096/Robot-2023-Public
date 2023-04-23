// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';

import { NetworkTables } from 'ntcore-ts-client';
import { NetworkTablesTypeInfos } from 'ntcore-ts-client/src/lib/types/types';

const path = require('path');

let nt = null;
let topic = null;

interface Data {
    name: string;
    filename: string;
	firstlineno: number;
	lineno: number | null;
}

const decorationTypeLine = vscode.window.createTextEditorDecorationType({
	isWholeLine: true,
	backgroundColor: "#00ccff",
	overviewRulerColor: "#00ccff",
	color: "#1f1f1f",
	fontWeight: "bold",
	overviewRulerLane: vscode.OverviewRulerLane.Full,
});

const decorationTypeCoro = vscode.window.createTextEditorDecorationType({
	isWholeLine: true,
	backgroundColor: "#ffcc00",
	overviewRulerColor: "#ffcc00",
	color: "#1f1f1f",
	fontWeight: "bold",
	overviewRulerLane: vscode.OverviewRulerLane.Full,
});


// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "robotviewer" is now active!');

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with registerCommand
	// The commandId parameter must match the command field in package.json
	let disposable = vscode.commands.registerCommand('robotviewer.helloWorld', () => {
		// The code you place here will be executed every time your command is executed
		// Display a message box to the user
		vscode.window.showInformationMessage('Hello World from RobotViewer!');
	});

	context.subscriptions.push(disposable);

	nt = NetworkTables.getInstanceByURI('10.40.96.2');
	// nt = NetworkTables.getInstanceByURI('localhost');

	nt.addRobotConnectionListener((connected) => {
		if (!connected) {
			for (const editor of vscode.window.visibleTextEditors) {
				editor.setDecorations(decorationTypeLine, []);
				editor.setDecorations(decorationTypeCoro, []);
			}
		}
	});

	topic = nt.createTopic<string>('/coroutine_logger/data', NetworkTablesTypeInfos.kString);

	topic.subscribe((value) => {
		// console.log(value);
		if (value === null) {
			return;
		}
		let coroDatas: [Data] = JSON.parse(value);

		for (const editor of vscode.window.visibleTextEditors) {
			// console.log(editor.document.fileName);
			let lineDecorations: vscode.DecorationOptions[] = [];
			let coroDecorations: vscode.DecorationOptions[] = [];
			for (const data of coroDatas) {
				if (path.basename(editor.document.fileName) === path.basename(data.filename)) {
					const line = editor.document.lineAt(data.firstlineno - 1);
					const range = line.range;
					lineDecorations.push({ range });

					if (data.lineno !== null) {
						const line = editor.document.lineAt(data.lineno - 1);
						const range = line.range;
						coroDecorations.push({ range });
					}
				}
			}
			editor.setDecorations(decorationTypeLine, lineDecorations);
			editor.setDecorations(decorationTypeCoro, coroDecorations);
		}


	}, true, { periodic: 0.25, all: true});
}

// This method is called when your extension is deactivated
export function deactivate() {}
