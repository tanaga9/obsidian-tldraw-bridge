---
tldraw-file: true
tags:
  - tldraw
tldraw-preview: "[[docs/diagrams/note-creation-recovery.webp]]"
---


```json !!!_START_OF_TLDRAW_DATA__DO_NOT_CHANGE_THIS_PHRASE_!!!
{
	"meta": {
		"uuid": "87040816-363b-42fe-8f83-eafc918f02e0",
		"plugin-version": "1.35.1",
		"tldraw-version": "5.6.0"
	},
	"raw": {
		"tldrawFileFormatVersion": 1,
		"schema": {
			"schemaVersion": 2,
			"sequences": {
				"com.tldraw.store": 5,
				"com.tldraw.asset": 1,
				"com.tldraw.camera": 1,
				"com.tldraw.document": 2,
				"com.tldraw.instance": 26,
				"com.tldraw.instance_page_state": 5,
				"com.tldraw.page": 1,
				"com.tldraw.instance_presence": 6,
				"com.tldraw.pointer": 1,
				"com.tldraw.shape": 4,
				"com.tldraw.user": 1,
				"com.tldraw.asset.image": 6,
				"com.tldraw.asset.video": 5,
				"com.tldraw.asset.bookmark": 2,
				"com.tldraw.shape.arrow": 8,
				"com.tldraw.shape.bookmark": 2,
				"com.tldraw.shape.draw": 5,
				"com.tldraw.shape.embed": 4,
				"com.tldraw.shape.frame": 1,
				"com.tldraw.shape.geo": 12,
				"com.tldraw.shape.group": 0,
				"com.tldraw.shape.highlight": 4,
				"com.tldraw.shape.image": 5,
				"com.tldraw.shape.line": 5,
				"com.tldraw.shape.note": 13,
				"com.tldraw.shape.text": 4,
				"com.tldraw.shape.video": 4,
				"com.tldraw.binding.arrow": 1
			}
		},
		"records": [
			{
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:write-to-wait",
				"type": "arrow",
				"parentId": "shape:note-creation-recovery",
				"props": {
					"kind": "arc",
					"elbowMidPoint": 0.5,
					"dash": "solid",
					"size": "s",
					"fill": "none",
					"color": "black",
					"labelColor": "black",
					"bend": 0,
					"start": {
						"x": 0,
						"y": 0
					},
					"end": {
						"x": 100,
						"y": 60
					},
					"arrowheadStart": "none",
					"arrowheadEnd": "arrow",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph"
							}
						]
					},
					"labelPosition": 0.5,
					"font": "draw",
					"scale": 1
				},
				"index": "a5sAAV",
				"typeName": "shape"
			},
			{
				"x": 0,
				"y": 0,
				"lastActivityTimestamp": 0,
				"meta": {},
				"id": "pointer:pointer",
				"typeName": "pointer"
			},
			{
				"name": "",
				"color": "#7B66DC",
				"imageUrl": "",
				"meta": {},
				"id": "user:3SS4w0vnXHWo1Bpp_W95n",
				"typeName": "user"
			},
			{
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:note-creation-recovery",
				"type": "frame",
				"props": {
					"w": 1270,
					"h": 620,
					"name": "note-creation-recovery",
					"color": "black"
				},
				"parentId": "page:page",
				"index": "a13Br",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:wait-to-rename-start",
				"type": "arrow",
				"fromId": "shape:wait-to-rename",
				"toId": "shape:wait",
				"props": {
					"isPrecise": true,
					"isExact": false,
					"normalizedAnchor": {
						"x": 0.5,
						"y": 1
					},
					"snap": "none",
					"terminal": "start"
				},
				"typeName": "binding"
			},
			{
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:validate-to-invalid",
				"type": "arrow",
				"parentId": "shape:note-creation-recovery",
				"props": {
					"kind": "arc",
					"elbowMidPoint": 0.5,
					"dash": "dashed",
					"size": "s",
					"fill": "none",
					"color": "black",
					"labelColor": "black",
					"bend": 0,
					"start": {
						"x": 0,
						"y": 0
					},
					"end": {
						"x": 100,
						"y": 60
					},
					"arrowheadStart": "none",
					"arrowheadEnd": "arrow",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph"
							}
						]
					},
					"labelPosition": 0.5,
					"font": "draw",
					"scale": 1
				},
				"index": "a7zoUU",
				"typeName": "shape"
			},
			{
				"x": 990,
				"y": 152,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:open",
				"type": "geo",
				"parentId": "shape:note-creation-recovery",
				"props": {
					"w": 248,
					"h": 112,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 0,
					"url": "",
					"scale": 1,
					"flipX": false,
					"flipY": false,
					"color": "green",
					"labelColor": "black",
					"fill": "solid",
					"size": "m",
					"font": "sans",
					"align": "start",
					"verticalAlign": "middle",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Open the editor",
										"marks": [
											{
												"type": "bold"
											}
										]
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "and verify saving",
										"marks": [
											{
												"type": "bold"
											}
										]
									}
								]
							}
						]
					}
				},
				"index": "a6Ymn",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:validate-to-write-start",
				"type": "arrow",
				"fromId": "shape:validate-to-write",
				"toId": "shape:validate",
				"props": {
					"isPrecise": true,
					"isExact": false,
					"normalizedAnchor": {
						"x": 1,
						"y": 0.5
					},
					"snap": "none",
					"terminal": "start"
				},
				"typeName": "binding"
			},
			{
				"x": 0,
				"y": 0,
				"z": 1,
				"meta": {},
				"id": "camera:page:page",
				"typeName": "camera"
			},
			{
				"x": 30,
				"y": 482,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:invalid-action",
				"type": "text",
				"parentId": "shape:note-creation-recovery",
				"props": {
					"color": "black",
					"size": "m",
					"w": 560,
					"font": "sans",
					"textAlign": "start",
					"autoSize": false,
					"scale": 1,
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "No file created",
										"marks": [
											{
												"type": "bold"
											}
										]
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Fix the body, then run create again."
									}
								]
							}
						]
					}
				},
				"index": "a9fxz",
				"typeName": "shape"
			},
			{
				"x": 350,
				"y": 152,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:write",
				"type": "geo",
				"parentId": "shape:note-creation-recovery",
				"props": {
					"w": 248,
					"h": 112,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 0,
					"url": "",
					"scale": 1,
					"flipX": false,
					"flipY": false,
					"color": "blue",
					"labelColor": "black",
					"fill": "solid",
					"size": "m",
					"font": "sans",
					"align": "start",
					"verticalAlign": "middle",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Create the note",
										"marks": [
											{
												"type": "bold"
											}
										]
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "and save its body",
										"marks": [
											{
												"type": "bold"
											}
										]
									}
								]
							}
						]
					}
				},
				"index": "a4zQi",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:wait-to-open-end",
				"type": "arrow",
				"fromId": "shape:wait-to-open",
				"toId": "shape:open",
				"props": {
					"isPrecise": true,
					"isExact": false,
					"normalizedAnchor": {
						"x": 0,
						"y": 0.5
					},
					"snap": "none",
					"terminal": "end"
				},
				"typeName": "binding"
			},
			{
				"editingShapeId": null,
				"croppingShapeId": null,
				"selectedShapeIds": [],
				"hoveredShapeId": null,
				"erasingShapeIds": [],
				"hintingShapeIds": [],
				"focusedGroupId": null,
				"meta": {},
				"id": "instance_page_state:page:page",
				"pageId": "page:page",
				"typeName": "instance_page_state"
			},
			{
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:validate-to-write",
				"type": "arrow",
				"parentId": "shape:note-creation-recovery",
				"props": {
					"kind": "arc",
					"elbowMidPoint": 0.5,
					"dash": "solid",
					"size": "s",
					"fill": "none",
					"color": "black",
					"labelColor": "black",
					"bend": 0,
					"start": {
						"x": 0,
						"y": 0
					},
					"end": {
						"x": 100,
						"y": 60
					},
					"arrowheadStart": "none",
					"arrowheadEnd": "arrow",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph"
							}
						]
					},
					"labelPosition": 0.5,
					"font": "draw",
					"scale": 1
				},
				"index": "a4zqqpV",
				"typeName": "shape"
			},
			{
				"x": 670,
				"y": 482,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:rename-action",
				"type": "text",
				"parentId": "shape:note-creation-recovery",
				"props": {
					"color": "black",
					"size": "m",
					"w": 562,
					"font": "sans",
					"textAlign": "start",
					"autoSize": false,
					"scale": 1,
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "File and body retained",
										"marks": [
											{
												"type": "bold"
											}
										]
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Check the path in CREATE_INCOMPLETE."
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Open that note and verify it with saved."
									}
								]
							}
						]
					}
				},
				"index": "aArcA",
				"typeName": "shape"
			},
			{
				"x": 670,
				"y": 152,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:wait",
				"type": "geo",
				"parentId": "shape:note-creation-recovery",
				"props": {
					"w": 248,
					"h": 112,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 0,
					"url": "",
					"scale": 1,
					"flipX": false,
					"flipY": false,
					"color": "blue",
					"labelColor": "black",
					"fill": "solid",
					"size": "m",
					"font": "sans",
					"align": "start",
					"verticalAlign": "middle",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Wait for Obsidian",
										"marks": [
											{
												"type": "bold"
											}
										]
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "to index the note",
										"marks": [
											{
												"type": "bold"
											}
										]
									}
								]
							}
						]
					}
				},
				"index": "a5hzm",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:wait-to-open-start",
				"type": "arrow",
				"fromId": "shape:wait-to-open",
				"toId": "shape:wait",
				"props": {
					"isPrecise": true,
					"isExact": false,
					"normalizedAnchor": {
						"x": 1,
						"y": 0.5
					},
					"snap": "none",
					"terminal": "start"
				},
				"typeName": "binding"
			},
			{
				"x": 30,
				"y": 152,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:validate",
				"type": "geo",
				"parentId": "shape:note-creation-recovery",
				"props": {
					"w": 248,
					"h": 112,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 0,
					"url": "",
					"scale": 1,
					"flipX": false,
					"flipY": false,
					"color": "grey",
					"labelColor": "black",
					"fill": "solid",
					"size": "m",
					"font": "sans",
					"align": "start",
					"verticalAlign": "middle",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Check the",
										"marks": [
											{
												"type": "bold"
											}
										]
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "initial body",
										"marks": [
											{
												"type": "bold"
											}
										]
									}
								]
							}
						]
					}
				},
				"index": "a3MNn",
				"typeName": "shape"
			},
			{
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:wait-to-rename",
				"type": "arrow",
				"parentId": "shape:note-creation-recovery",
				"props": {
					"kind": "arc",
					"elbowMidPoint": 0.5,
					"dash": "dashed",
					"size": "s",
					"fill": "none",
					"color": "black",
					"labelColor": "black",
					"bend": 0,
					"start": {
						"x": 0,
						"y": 0
					},
					"end": {
						"x": 100,
						"y": 60
					},
					"arrowheadStart": "none",
					"arrowheadEnd": "arrow",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph"
							}
						]
					},
					"labelPosition": 0.5,
					"font": "draw",
					"scale": 1
				},
				"index": "a8srJV",
				"typeName": "shape"
			},
			{
				"x": 30,
				"y": 72,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:subtitle",
				"type": "text",
				"parentId": "shape:note-creation-recovery",
				"props": {
					"color": "black",
					"size": "m",
					"w": 1230,
					"font": "sans",
					"textAlign": "start",
					"autoSize": false,
					"scale": 1,
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "The bridge tried to open inventory.md before Obsidian recognized the saved file as a drawing."
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "After the fix, creation follows the steps below."
									}
								]
							}
						]
					}
				},
				"index": "a2alv",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:write-to-wait-end",
				"type": "arrow",
				"fromId": "shape:write-to-wait",
				"toId": "shape:wait",
				"props": {
					"isPrecise": true,
					"isExact": false,
					"normalizedAnchor": {
						"x": 0,
						"y": 0.5
					},
					"snap": "none",
					"terminal": "end"
				},
				"typeName": "binding"
			},
			{
				"meta": {},
				"id": "binding:validate-to-invalid-end",
				"type": "arrow",
				"fromId": "shape:validate-to-invalid",
				"toId": "shape:invalid",
				"props": {
					"isPrecise": true,
					"isExact": false,
					"normalizedAnchor": {
						"x": 0.5,
						"y": 0
					},
					"snap": "none",
					"terminal": "end"
				},
				"typeName": "binding"
			},
			{
				"x": 670,
				"y": 346,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:rename",
				"type": "geo",
				"parentId": "shape:note-creation-recovery",
				"props": {
					"w": 248,
					"h": 114,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 8,
					"url": "",
					"scale": 1,
					"flipX": false,
					"flipY": false,
					"color": "yellow",
					"labelColor": "black",
					"fill": "solid",
					"size": "m",
					"font": "sans",
					"align": "start",
					"verticalAlign": "middle",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "What if the note"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "is renamed during"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "the wait?"
									}
								]
							}
						]
					}
				},
				"index": "a8TvI",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:write-to-wait-start",
				"type": "arrow",
				"fromId": "shape:write-to-wait",
				"toId": "shape:write",
				"props": {
					"isPrecise": true,
					"isExact": false,
					"normalizedAnchor": {
						"x": 1,
						"y": 0.5
					},
					"snap": "none",
					"terminal": "start"
				},
				"typeName": "binding"
			},
			{
				"meta": {},
				"id": "page:page",
				"name": "Page 1",
				"index": "a1",
				"typeName": "page"
			},
			{
				"gridSize": 10,
				"name": "",
				"meta": {},
				"id": "document:document",
				"typeName": "document"
			},
			{
				"followingUserId": null,
				"opacityForNextShape": 1,
				"stylesForNextShape": {},
				"brush": null,
				"scribbles": [],
				"cursor": {
					"type": "default",
					"rotation": 0
				},
				"isFocusMode": false,
				"exportBackground": true,
				"isDebugMode": false,
				"isToolLocked": false,
				"screenBounds": {
					"x": 0,
					"y": 0,
					"w": 1080,
					"h": 720
				},
				"insets": [
					false,
					false,
					false,
					false
				],
				"zoomBrush": null,
				"isGridMode": false,
				"isPenMode": false,
				"chatMessage": "",
				"isChatting": false,
				"highlightedUserIds": [],
				"isFocused": false,
				"devicePixelRatio": 2,
				"isCoarsePointer": false,
				"isHoveringCanvas": null,
				"openMenus": [],
				"isChangingStyle": false,
				"isReadonly": false,
				"meta": {},
				"duplicateProps": null,
				"cameraState": "idle",
				"id": "instance:instance",
				"currentPageId": "page:page",
				"typeName": "instance"
			},
			{
				"meta": {},
				"id": "binding:wait-to-rename-end",
				"type": "arrow",
				"fromId": "shape:wait-to-rename",
				"toId": "shape:rename",
				"props": {
					"isPrecise": true,
					"isExact": false,
					"normalizedAnchor": {
						"x": 0.5,
						"y": 0
					},
					"snap": "none",
					"terminal": "end"
				},
				"typeName": "binding"
			},
			{
				"meta": {},
				"id": "binding:validate-to-invalid-start",
				"type": "arrow",
				"fromId": "shape:validate-to-invalid",
				"toId": "shape:validate",
				"props": {
					"isPrecise": true,
					"isExact": false,
					"normalizedAnchor": {
						"x": 0.5,
						"y": 1
					},
					"snap": "none",
					"terminal": "start"
				},
				"typeName": "binding"
			},
			{
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:wait-to-open",
				"type": "arrow",
				"parentId": "shape:note-creation-recovery",
				"props": {
					"kind": "arc",
					"elbowMidPoint": 0.5,
					"dash": "solid",
					"size": "s",
					"fill": "none",
					"color": "black",
					"labelColor": "black",
					"bend": 0,
					"start": {
						"x": 0,
						"y": 0
					},
					"end": {
						"x": 100,
						"y": 60
					},
					"arrowheadStart": "none",
					"arrowheadEnd": "arrow",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph"
							}
						]
					},
					"labelPosition": 0.5,
					"font": "draw",
					"scale": 1
				},
				"index": "a6ogXV",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:validate-to-write-end",
				"type": "arrow",
				"fromId": "shape:validate-to-write",
				"toId": "shape:write",
				"props": {
					"isPrecise": true,
					"isExact": false,
					"normalizedAnchor": {
						"x": 0,
						"y": 0.5
					},
					"snap": "none",
					"terminal": "end"
				},
				"typeName": "binding"
			},
			{
				"x": 30,
				"y": 346,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:invalid",
				"type": "geo",
				"parentId": "shape:note-creation-recovery",
				"props": {
					"w": 248,
					"h": 114,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 0,
					"url": "",
					"scale": 1,
					"flipX": false,
					"flipY": false,
					"color": "yellow",
					"labelColor": "black",
					"fill": "solid",
					"size": "m",
					"font": "sans",
					"align": "start",
					"verticalAlign": "middle",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Body is missing"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "its final newline"
									}
								]
							}
						]
					}
				},
				"index": "a7vl6",
				"typeName": "shape"
			},
			{
				"x": 28,
				"y": 16,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:title",
				"type": "text",
				"parentId": "shape:note-creation-recovery",
				"props": {
					"color": "black",
					"size": "l",
					"w": 1240,
					"font": "sans",
					"textAlign": "start",
					"autoSize": false,
					"scale": 1,
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Why did create fail if the note is already there?",
										"marks": [
											{
												"type": "bold"
											}
										]
									}
								]
							}
						]
					}
				},
				"index": "a1zzwV",
				"typeName": "shape"
			}
		]
	}
}
!!!_END_OF_TLDRAW_DATA__DO_NOT_CHANGE_THIS_PHRASE_!!!
```