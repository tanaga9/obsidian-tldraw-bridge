---
tldraw-file: true
tags:
  - tldraw
---


```json !!!_START_OF_TLDRAW_DATA__DO_NOT_CHANGE_THIS_PHRASE_!!!
{
	"meta": {
		"uuid": "04f8f0a0-47bd-48cb-80c2-169b42731125",
		"plugin-version": "1.32.0",
		"tldraw-version": "5.4.0"
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
				"meta": {},
				"id": "binding:nested-edit-start",
				"type": "arrow",
				"fromId": "shape:nested-edit",
				"toId": "shape:nested-agent",
				"props": {
					"isPrecise": false,
					"isExact": false,
					"normalizedAnchor": {
						"x": 0.5,
						"y": 0.5
					},
					"snap": "none",
					"terminal": "start"
				},
				"typeName": "binding"
			},
			{
				"x": 935,
				"y": 590,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:secondary-discovery-note",
				"type": "text",
				"parentId": "shape:nested-agent-instruction-scope",
				"props": {
					"color": "black",
					"size": "s",
					"w": 300,
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
										"text": "Secondary folders do not"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "load these instructions."
									}
								]
							}
						]
					}
				},
				"index": "aXHa2",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:nested-load-project-end",
				"type": "arrow",
				"fromId": "shape:nested-load-project",
				"toId": "shape:nested-agent",
				"props": {
					"isPrecise": false,
					"isExact": false,
					"normalizedAnchor": {
						"x": 0.5,
						"y": 0.5
					},
					"snap": "none",
					"terminal": "end"
				},
				"typeName": "binding"
			},
			{
				"x": 45,
				"y": 470,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:nested-drawing",
				"type": "geo",
				"parentId": "shape:nested-agent-instruction-scope",
				"props": {
					"w": 300,
					"h": 100,
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
										"text": "tldraw note"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Editable drawing"
									}
								]
							}
						]
					}
				},
				"index": "aF57f",
				"typeName": "shape"
			},
			{
				"x": 45,
				"y": 200,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:nested-workspace-title",
				"type": "text",
				"parentId": "shape:nested-agent-instruction-scope",
				"props": {
					"color": "black",
					"size": "m",
					"w": 300,
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
										"text": "Primary folder / vault"
									}
								]
							}
						]
					}
				},
				"index": "a3EWE",
				"typeName": "shape"
			},
			{
				"x": 45,
				"y": 285,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:nested-project-policy",
				"type": "geo",
				"parentId": "shape:nested-agent-instruction-scope",
				"props": {
					"w": 300,
					"h": 100,
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
										"text": "AGENTS.md"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Project instructions"
									}
								]
							}
						]
					}
				},
				"index": "a5Sdf",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:combined-read-external-start",
				"type": "arrow",
				"fromId": "shape:combined-read-external",
				"toId": "shape:combined-external-policy",
				"props": {
					"isPrecise": false,
					"isExact": false,
					"normalizedAnchor": {
						"x": 0.5,
						"y": 0.5
					},
					"snap": "none",
					"terminal": "start"
				},
				"typeName": "binding"
			},
			{
				"x": 935,
				"y": 285,
				"rotation": 0,
				"isLocked": false,
				"opacity": 0.75,
				"meta": {},
				"id": "shape:combined-external-policy",
				"type": "geo",
				"parentId": "shape:nested-agent-instruction-scope",
				"props": {
					"w": 300,
					"h": 100,
					"geo": "rectangle",
					"dash": "dashed",
					"growY": 0,
					"url": "",
					"scale": 1,
					"flipX": false,
					"flipY": false,
					"color": "orange",
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
										"text": "AGENTS.md"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Vault instructions"
									}
								]
							}
						]
					}
				},
				"index": "aNUFT",
				"typeName": "shape"
			},
			{
				"x": 935,
				"y": 200,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:combined-external-title",
				"type": "text",
				"parentId": "shape:nested-agent-instruction-scope",
				"props": {
					"color": "black",
					"size": "m",
					"w": 300,
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
										"text": "Other vault"
									}
								]
							}
						]
					}
				},
				"index": "aK6sb",
				"typeName": "shape"
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
				"x": 780,
				"y": 300,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:external-read-label",
				"type": "text",
				"parentId": "shape:nested-agent-instruction-scope",
				"props": {
					"color": "orange",
					"size": "s",
					"w": 130,
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
										"text": "Explicit read"
									}
								]
							}
						]
					}
				},
				"index": "aWjdI",
				"typeName": "shape"
			},
			{
				"x": 585,
				"y": 205,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:nested-load-other",
				"type": "arrow",
				"parentId": "shape:nested-agent-instruction-scope",
				"props": {
					"kind": "arc",
					"elbowMidPoint": 0.5,
					"dash": "solid",
					"size": "m",
					"fill": "none",
					"color": "blue",
					"labelColor": "black",
					"bend": 0,
					"start": {
						"x": 0,
						"y": 0
					},
					"end": {
						"x": 0,
						"y": 75
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
					"font": "mono",
					"scale": 1
				},
				"index": "aUjU3l",
				"typeName": "shape"
			},
			{
				"x": 585,
				"y": 390,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:nested-edit",
				"type": "arrow",
				"parentId": "shape:nested-agent-instruction-scope",
				"props": {
					"kind": "arc",
					"elbowMidPoint": 0.5,
					"dash": "solid",
					"size": "m",
					"fill": "none",
					"color": "green",
					"labelColor": "green",
					"bend": 0,
					"start": {
						"x": 0,
						"y": 0
					},
					"end": {
						"x": -270,
						"y": 195
					},
					"arrowheadStart": "none",
					"arrowheadEnd": "arrow",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Bridge"
									}
								]
							}
						]
					},
					"labelPosition": 0.5,
					"font": "mono",
					"scale": 1
				},
				"index": "aUOd4G",
				"typeName": "shape"
			},
			{
				"x": 510,
				"y": 280,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:nested-agent",
				"type": "geo",
				"parentId": "shape:nested-agent-instruction-scope",
				"props": {
					"w": 260,
					"h": 110,
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
										"text": "Agent"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Loaded instructions"
									}
								]
							}
						]
					}
				},
				"index": "aU9YU",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:nested-load-project-start",
				"type": "arrow",
				"fromId": "shape:nested-load-project",
				"toId": "shape:nested-project-policy",
				"props": {
					"isPrecise": false,
					"isExact": false,
					"normalizedAnchor": {
						"x": 0.5,
						"y": 0.5
					},
					"snap": "none",
					"terminal": "start"
				},
				"typeName": "binding"
			},
			{
				"meta": {},
				"id": "binding:combined-edit-external-end",
				"type": "arrow",
				"fromId": "shape:combined-edit-external",
				"toId": "shape:combined-external-drawing",
				"props": {
					"isPrecise": false,
					"isExact": false,
					"normalizedAnchor": {
						"x": 0.5,
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
				"x": 935,
				"y": 470,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:combined-external-drawing",
				"type": "geo",
				"parentId": "shape:nested-agent-instruction-scope",
				"props": {
					"w": 300,
					"h": 100,
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
										"text": "tldraw note"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Editable drawing"
									}
								]
							}
						]
					}
				},
				"index": "aMubj",
				"typeName": "shape"
			},
			{
				"x": 335,
				"y": 335,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:nested-load-project",
				"type": "arrow",
				"parentId": "shape:nested-agent-instruction-scope",
				"props": {
					"kind": "arc",
					"elbowMidPoint": 0.5,
					"dash": "solid",
					"size": "m",
					"fill": "none",
					"color": "blue",
					"labelColor": "black",
					"bend": 0,
					"start": {
						"x": 0,
						"y": 0
					},
					"end": {
						"x": 105,
						"y": 0
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
					"font": "mono",
					"scale": 1
				},
				"index": "aVzHUV",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:combined-edit-external-start",
				"type": "arrow",
				"fromId": "shape:combined-edit-external",
				"toId": "shape:nested-agent",
				"props": {
					"isPrecise": false,
					"isExact": false,
					"normalizedAnchor": {
						"x": 0.5,
						"y": 0.5
					},
					"snap": "none",
					"terminal": "start"
				},
				"typeName": "binding"
			},
			{
				"x": 45,
				"y": 590,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:same-root-policy-note",
				"type": "text",
				"parentId": "shape:nested-agent-instruction-scope",
				"props": {
					"color": "blue",
					"size": "s",
					"w": 300,
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
										"text": "Same root folder;"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "one root AGENTS.md."
									}
								]
							}
						]
					}
				},
				"index": "aTW72",
				"typeName": "shape"
			},
			{
				"x": 1320,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:nested-agent-instruction-scope",
				"type": "frame",
				"props": {
					"w": 1280,
					"h": 780,
					"name": "agent-instruction-scope",
					"color": "black"
				},
				"parentId": "page:page",
				"index": "a2M62",
				"typeName": "shape"
			},
			{
				"x": 35,
				"y": 700,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:nested-takeaway",
				"type": "text",
				"parentId": "shape:nested-agent-instruction-scope",
				"props": {
					"color": "black",
					"size": "s",
					"w": 1210,
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
										"text": "Selecting a vault through Bridge does not load AGENTS.md."
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Apply loaded instructions according to their scope and priority."
									}
								]
							}
						]
					}
				},
				"index": "aBGSj",
				"typeName": "shape"
			},
			{
				"x": 855,
				"y": 535,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:combined-read-external",
				"type": "arrow",
				"parentId": "shape:nested-agent-instruction-scope",
				"props": {
					"kind": "arc",
					"elbowMidPoint": 0.5,
					"dash": "dashed",
					"size": "s",
					"fill": "none",
					"color": "orange",
					"labelColor": "black",
					"bend": 0,
					"start": {
						"x": 0,
						"y": 0
					},
					"end": {
						"x": -270,
						"y": -145
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
					"font": "mono",
					"scale": 1
				},
				"index": "aU9s2nl",
				"typeName": "shape"
			},
			{
				"x": 45,
				"y": 395,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:nested-discovery",
				"type": "text",
				"parentId": "shape:nested-agent-instruction-scope",
				"props": {
					"color": "black",
					"size": "s",
					"w": 300,
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
										"text": "Loaded at startup"
									}
								]
							}
						]
					}
				},
				"index": "a6LHb",
				"typeName": "shape"
			},
			{
				"x": 490,
				"y": 130,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:nested-request-skill",
				"type": "geo",
				"parentId": "shape:nested-agent-instruction-scope",
				"props": {
					"w": 300,
					"h": 100,
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
										"text": "Request + Skill"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "+ global instructions"
									}
								]
							}
						]
					}
				},
				"index": "a7rOj",
				"typeName": "shape"
			},
			{
				"x": 935,
				"y": 237,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:combined-external-path",
				"type": "text",
				"parentId": "shape:nested-agent-instruction-scope",
				"props": {
					"color": "black",
					"size": "s",
					"w": 300,
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
										"text": "/notes/team"
									}
								]
							}
						]
					}
				},
				"index": "aL3ov",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:nested-load-other-end",
				"type": "arrow",
				"fromId": "shape:nested-load-other",
				"toId": "shape:nested-agent",
				"props": {
					"isPrecise": false,
					"isExact": false,
					"normalizedAnchor": {
						"x": 0.5,
						"y": 0.5
					},
					"snap": "none",
					"terminal": "end"
				},
				"typeName": "binding"
			},
			{
				"x": 25,
				"y": 180,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:nested-workspace",
				"type": "geo",
				"parentId": "shape:nested-agent-instruction-scope",
				"props": {
					"w": 340,
					"h": 490,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 0,
					"url": "",
					"scale": 1,
					"flipX": false,
					"flipY": false,
					"color": "grey",
					"labelColor": "black",
					"fill": "none",
					"size": "m",
					"font": "sans",
					"align": "start",
					"verticalAlign": "middle",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph"
							}
						]
					}
				},
				"index": "a2Lkj",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:nested-edit-end",
				"type": "arrow",
				"fromId": "shape:nested-edit",
				"toId": "shape:nested-drawing",
				"props": {
					"isPrecise": false,
					"isExact": false,
					"normalizedAnchor": {
						"x": 0.5,
						"y": 0.5
					},
					"snap": "none",
					"terminal": "end"
				},
				"typeName": "binding"
			},
			{
				"x": 935,
				"y": 405,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:combined-external-policy-note",
				"type": "text",
				"parentId": "shape:nested-agent-instruction-scope",
				"props": {
					"color": "orange",
					"size": "s",
					"w": 300,
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
										"text": "Read when the user or loaded"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "project instructions direct it."
									}
								]
							}
						]
					}
				},
				"index": "aRERr",
				"typeName": "shape"
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
				"x": 45,
				"y": 237,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:nested-workspace-path",
				"type": "text",
				"parentId": "shape:nested-agent-instruction-scope",
				"props": {
					"color": "grey",
					"size": "s",
					"w": 300,
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
										"text": "/work/project"
									}
								]
							}
						]
					}
				},
				"index": "a4Sin",
				"typeName": "shape"
			},
			{
				"x": 35,
				"y": 25,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:nested-title",
				"type": "text",
				"parentId": "shape:nested-agent-instruction-scope",
				"props": {
					"color": "black",
					"size": "m",
					"w": 1210,
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
										"text": "Instruction sources and target vaults"
									}
								]
							}
						]
					}
				},
				"index": "a1gYz",
				"typeName": "shape"
			},
			{
				"x": 35,
				"y": 75,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:scope-assumption",
				"type": "text",
				"parentId": "shape:nested-agent-instruction-scope",
				"props": {
					"color": "black",
					"size": "s",
					"w": 1210,
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
										"text": "Codex example: /work/project is the primary folder and working directory."
									}
								]
							}
						]
					}
				},
				"index": "aSn9v",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:combined-read-external-end",
				"type": "arrow",
				"fromId": "shape:combined-read-external",
				"toId": "shape:nested-agent",
				"props": {
					"isPrecise": false,
					"isExact": false,
					"normalizedAnchor": {
						"x": 0.5,
						"y": 0.5
					},
					"snap": "none",
					"terminal": "end"
				},
				"typeName": "binding"
			},
			{
				"x": 915,
				"y": 180,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:combined-external-vault",
				"type": "geo",
				"parentId": "shape:nested-agent-instruction-scope",
				"props": {
					"w": 340,
					"h": 490,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 0,
					"url": "",
					"scale": 1,
					"flipX": false,
					"flipY": false,
					"color": "grey",
					"labelColor": "black",
					"fill": "none",
					"size": "m",
					"font": "sans",
					"align": "start",
					"verticalAlign": "middle",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph"
							}
						]
					}
				},
				"index": "aJ02A",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:nested-load-other-start",
				"type": "arrow",
				"fromId": "shape:nested-load-other",
				"toId": "shape:nested-request-skill",
				"props": {
					"isPrecise": false,
					"isExact": false,
					"normalizedAnchor": {
						"x": 0.5,
						"y": 0.5
					},
					"snap": "none",
					"terminal": "start"
				},
				"typeName": "binding"
			},
			{
				"x": 730,
				"y": 335,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:combined-edit-external",
				"type": "arrow",
				"parentId": "shape:nested-agent-instruction-scope",
				"props": {
					"kind": "arc",
					"elbowMidPoint": 0.5,
					"dash": "solid",
					"size": "m",
					"fill": "none",
					"color": "green",
					"labelColor": "green",
					"bend": 0,
					"start": {
						"x": 0,
						"y": 0
					},
					"end": {
						"x": 125,
						"y": 0
					},
					"arrowheadStart": "none",
					"arrowheadEnd": "arrow",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Bridge"
									}
								]
							}
						]
					},
					"labelPosition": 0.5,
					"font": "mono",
					"scale": 1
				},
				"index": "aUB9SM",
				"typeName": "shape"
			}
		]
	}
}
!!!_END_OF_TLDRAW_DATA__DO_NOT_CHANGE_THIS_PHRASE_!!!
```