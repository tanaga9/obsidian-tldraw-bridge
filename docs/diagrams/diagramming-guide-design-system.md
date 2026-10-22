---
tldraw-file: true
tags:
  - tldraw
---


```json !!!_START_OF_TLDRAW_DATA__DO_NOT_CHANGE_THIS_PHRASE_!!!
{
	"meta": {
		"uuid": "bcbe4f79-22a3-409b-8b48-60b0a39b2666",
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
				"x": 60,
				"y": 590,
				"rotation": 0,
				"isLocked": false,
				"opacity": 0.5,
				"meta": {},
				"id": "shape:normal",
				"type": "geo",
				"parentId": "shape:guide-system",
				"props": {
					"w": 1280,
					"h": 500,
					"geo": "rectangle",
					"dash": "solid",
					"growY": 0,
					"url": "",
					"scale": 1,
					"flipX": false,
					"flipY": false,
					"color": "green",
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
								"type": "paragraph",
								"content": []
							}
						]
					}
				},
				"index": "aCPt6",
				"typeName": "shape"
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
				"x": 80,
				"y": 1160,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:maintenance-label",
				"type": "text",
				"parentId": "shape:guide-system",
				"props": {
					"color": "violet",
					"size": "l",
					"w": 350,
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
										"text": "MAINTENANCE"
									}
								]
							}
						]
					}
				},
				"index": "aVBGb",
				"typeName": "shape"
			},
			{
				"x": 410,
				"y": 622,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:use-subheading",
				"type": "text",
				"parentId": "shape:guide-system",
				"props": {
					"color": "green",
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
										"text": "Request to useful diagram"
									}
								]
							}
						]
					}
				},
				"index": "ajsJE",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:retry-end",
				"type": "arrow",
				"fromId": "shape:retry",
				"toId": "shape:candidate",
				"props": {
					"isPrecise": true,
					"isExact": false,
					"normalizedAnchor": {
						"x": 0.5,
						"y": 1
					},
					"snap": "none",
					"terminal": "end"
				},
				"typeName": "binding"
			},
			{
				"meta": {},
				"id": "binding:fail-end",
				"type": "arrow",
				"fromId": "shape:fail",
				"toId": "shape:revise",
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
				"id": "binding:maint-case-diagnose-end",
				"type": "arrow",
				"fromId": "shape:maint-case-diagnose",
				"toId": "shape:maint-diagnose",
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
				"id": "binding:distill-start",
				"type": "arrow",
				"fromId": "shape:distill",
				"toId": "shape:knowledge",
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
				"id": "binding:maint-case-compare-start",
				"type": "arrow",
				"fromId": "shape:maint-case-compare",
				"toId": "shape:maint-case",
				"props": {
					"isPrecise": true,
					"isExact": false,
					"normalizedAnchor": {
						"x": 1,
						"y": 0.75
					},
					"snap": "none",
					"terminal": "start"
				},
				"typeName": "binding"
			},
			{
				"x": 1160,
				"y": 1520,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:maint-verdicts-decision",
				"type": "arrow",
				"parentId": "shape:guide-system",
				"props": {
					"kind": "arc",
					"elbowMidPoint": 0.5,
					"dash": "solid",
					"size": "s",
					"fill": "none",
					"color": "grey",
					"labelColor": "black",
					"bend": 0,
					"start": {
						"x": 0,
						"y": 0
					},
					"end": {
						"x": 0,
						"y": 70
					},
					"arrowheadStart": "none",
					"arrowheadEnd": "arrow",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph",
								"content": []
							}
						]
					},
					"labelPosition": 0.5,
					"font": "draw",
					"scale": 1
				},
				"index": "agr4v",
				"typeName": "shape"
			},
			{
				"x": 80,
				"y": 1205,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:maintenance-note",
				"type": "text",
				"parentId": "shape:guide-system",
				"props": {
					"color": "black",
					"size": "s",
					"w": 1200,
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
										"text": "Freeze scope & initial defects • record elapsed time + CLI calls"
									}
								]
							}
						]
					}
				},
				"index": "aWyxf",
				"typeName": "shape"
			},
			{
				"x": 1000,
				"y": 1350,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:maint-verdicts",
				"type": "geo",
				"parentId": "shape:guide-system",
				"props": {
					"w": 320,
					"h": 170,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 0,
					"url": "",
					"scale": 1,
					"flipX": false,
					"flipY": false,
					"color": "violet",
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
										"text": "Three verdicts"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Task • affected quality"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Preservation"
									}
								]
							}
						]
					}
				},
				"index": "aabNn",
				"typeName": "shape"
			},
			{
				"x": 410,
				"y": 780,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:candidate-check",
				"type": "arrow",
				"parentId": "shape:guide-system",
				"props": {
					"kind": "arc",
					"elbowMidPoint": 0.5,
					"dash": "solid",
					"size": "s",
					"fill": "none",
					"color": "grey",
					"labelColor": "black",
					"bend": 0,
					"start": {
						"x": 0,
						"y": 0
					},
					"end": {
						"x": 120,
						"y": 0
					},
					"arrowheadStart": "none",
					"arrowheadEnd": "arrow",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph",
								"content": []
							}
						]
					},
					"labelPosition": 0.5,
					"font": "draw",
					"scale": 1
				},
				"index": "aGoKzG",
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
				"x": 60,
				"y": 265,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:knowledge",
				"type": "geo",
				"parentId": "shape:guide-system",
				"props": {
					"w": 350,
					"h": 180,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 0,
					"url": "",
					"scale": 1,
					"flipX": false,
					"flipY": false,
					"color": "violet",
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
										"text": "Foundations & principles"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Perception • cognition"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Meaning • design trade-offs"
									}
								]
							}
						]
					}
				},
				"index": "a4p6I",
				"typeName": "shape"
			},
			{
				"x": 1000,
				"y": 705,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:refine",
				"type": "geo",
				"parentId": "shape:guide-system",
				"props": {
					"w": 320,
					"h": 150,
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
										"text": "Refine & verify"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Navigation • style • effort"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Check • save"
									}
								]
							}
						]
					}
				},
				"index": "aHUtg",
				"typeName": "shape"
			},
			{
				"x": 1000,
				"y": 1590,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:maint-decision",
				"type": "geo",
				"parentId": "shape:guide-system",
				"props": {
					"w": 320,
					"h": 110,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 0,
					"url": "",
					"scale": 1,
					"flipX": false,
					"flipY": false,
					"color": "violet",
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
										"text": "Keep / simplify / revise"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Within the evidence"
									}
								]
							}
						]
					}
				},
				"index": "abvJr",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:apply-end",
				"type": "arrow",
				"fromId": "shape:apply",
				"toId": "shape:conditions",
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
				"id": "binding:fail-start",
				"type": "arrow",
				"fromId": "shape:fail",
				"toId": "shape:conditions",
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
				"meta": {},
				"id": "binding:feedback-end",
				"type": "arrow",
				"fromId": "shape:feedback",
				"toId": "shape:skill",
				"props": {
					"isPrecise": true,
					"isExact": false,
					"normalizedAnchor": {
						"x": 1,
						"y": 0.5
					},
					"snap": "none",
					"terminal": "end"
				},
				"typeName": "binding"
			},
			{
				"meta": {},
				"id": "binding:retry-start",
				"type": "arrow",
				"fromId": "shape:retry",
				"toId": "shape:revise",
				"props": {
					"isPrecise": true,
					"isExact": false,
					"normalizedAnchor": {
						"x": 0,
						"y": 0.5
					},
					"snap": "none",
					"terminal": "start"
				},
				"typeName": "binding"
			},
			{
				"meta": {},
				"id": "binding:maint-case-diagnose-start",
				"type": "arrow",
				"fromId": "shape:maint-case-diagnose",
				"toId": "shape:maint-case",
				"props": {
					"isPrecise": true,
					"isExact": false,
					"normalizedAnchor": {
						"x": 1,
						"y": 0.25
					},
					"snap": "none",
					"terminal": "start"
				},
				"typeName": "binding"
			},
			{
				"x": 490,
				"y": 1290,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:maint-diagnose",
				"type": "geo",
				"parentId": "shape:guide-system",
				"props": {
					"w": 380,
					"h": 120,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 0,
					"url": "",
					"scale": 1,
					"flipX": false,
					"flipY": false,
					"color": "violet",
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
										"text": "Diagnose a failure"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Reproduce → fix → recheck"
									}
								]
							}
						]
					}
				},
				"index": "aYBTn",
				"typeName": "shape"
			},
			{
				"x": 920,
				"y": 780,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:pass",
				"type": "arrow",
				"parentId": "shape:guide-system",
				"props": {
					"kind": "arc",
					"elbowMidPoint": 0.5,
					"dash": "solid",
					"size": "s",
					"fill": "none",
					"color": "green",
					"labelColor": "black",
					"bend": 0,
					"start": {
						"x": 0,
						"y": 0
					},
					"end": {
						"x": 80,
						"y": 0
					},
					"arrowheadStart": "none",
					"arrowheadEnd": "arrow",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph",
								"content": []
							}
						]
					},
					"labelPosition": 0.5,
					"font": "draw",
					"scale": 1
				},
				"index": "aHsWKV",
				"typeName": "shape"
			},
			{
				"x": 80,
				"y": 705,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:candidate",
				"type": "geo",
				"parentId": "shape:guide-system",
				"props": {
					"w": 330,
					"h": 150,
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
										"text": "Agent: design candidate"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Structure before polish"
									}
								]
							}
						]
					}
				},
				"index": "aFNRA",
				"typeName": "shape"
			},
			{
				"x": 410,
				"y": 355,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:distill",
				"type": "arrow",
				"parentId": "shape:guide-system",
				"props": {
					"kind": "arc",
					"elbowMidPoint": 0.5,
					"dash": "solid",
					"size": "s",
					"fill": "none",
					"color": "grey",
					"labelColor": "black",
					"bend": 0,
					"start": {
						"x": 0,
						"y": 0
					},
					"end": {
						"x": 130,
						"y": 0
					},
					"arrowheadStart": "none",
					"arrowheadEnd": "arrow",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph",
								"content": []
							}
						]
					},
					"labelPosition": 0.5,
					"font": "draw",
					"scale": 1
				},
				"index": "a5jkW",
				"typeName": "shape"
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
				"x": 60,
				"y": 205,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:author-label",
				"type": "text",
				"parentId": "shape:guide-system",
				"props": {
					"color": "violet",
					"size": "l",
					"w": 380,
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
										"text": "Authoring knowledge"
									}
								]
							}
						]
					}
				},
				"index": "a3Kif",
				"typeName": "shape"
			},
			{
				"x": 1000,
				"y": 925,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:deliver",
				"type": "geo",
				"parentId": "shape:guide-system",
				"props": {
					"w": 320,
					"h": 110,
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
										"text": "Useful diagram"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Saved & delivered"
									}
								]
							}
						]
					}
				},
				"index": "aJhTb",
				"typeName": "shape"
			},
			{
				"x": 1160,
				"y": 855,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:finish",
				"type": "arrow",
				"parentId": "shape:guide-system",
				"props": {
					"kind": "arc",
					"elbowMidPoint": 0.5,
					"dash": "solid",
					"size": "s",
					"fill": "none",
					"color": "green",
					"labelColor": "black",
					"bend": 0,
					"start": {
						"x": 0,
						"y": 0
					},
					"end": {
						"x": 0,
						"y": 70
					},
					"arrowheadStart": "none",
					"arrowheadEnd": "arrow",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph",
								"content": []
							}
						]
					},
					"labelPosition": 0.5,
					"font": "draw",
					"scale": 1
				},
				"index": "aJzmKl",
				"typeName": "shape"
			},
			{
				"x": 870,
				"y": 1530,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:maint-compare-verdicts",
				"type": "arrow",
				"parentId": "shape:guide-system",
				"props": {
					"kind": "elbow",
					"elbowMidPoint": 0.5,
					"dash": "solid",
					"size": "s",
					"fill": "none",
					"color": "grey",
					"labelColor": "black",
					"bend": 0,
					"start": {
						"x": 0,
						"y": 0
					},
					"end": {
						"x": 130,
						"y": -52.5
					},
					"arrowheadStart": "none",
					"arrowheadEnd": "arrow",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph",
								"content": []
							}
						]
					},
					"labelPosition": 0.5,
					"font": "draw",
					"scale": 1
				},
				"index": "aaj6o8",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:apply-start",
				"type": "arrow",
				"fromId": "shape:apply",
				"toId": "shape:skill",
				"props": {
					"isPrecise": true,
					"isExact": false,
					"normalizedAnchor": {
						"x": 0.23125,
						"y": 1
					},
					"snap": "none",
					"terminal": "start"
				},
				"typeName": "binding"
			},
			{
				"x": 530,
				"y": 980,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:retry",
				"type": "arrow",
				"parentId": "shape:guide-system",
				"props": {
					"kind": "elbow",
					"elbowMidPoint": 0.5,
					"dash": "solid",
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
						"x": -285,
						"y": -125
					},
					"arrowheadStart": "none",
					"arrowheadEnd": "arrow",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph",
								"content": []
							}
						]
					},
					"labelPosition": 0.5,
					"font": "draw",
					"scale": 1
				},
				"index": "aIM9AV",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:feedback-start",
				"type": "arrow",
				"fromId": "shape:feedback",
				"toId": "shape:maint-decision",
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
				"id": "binding:maint-diagnose-verdicts-end",
				"type": "arrow",
				"fromId": "shape:maint-diagnose-verdicts",
				"toId": "shape:maint-verdicts",
				"props": {
					"isPrecise": true,
					"isExact": false,
					"normalizedAnchor": {
						"x": 0,
						"y": 0.25
					},
					"snap": "none",
					"terminal": "end"
				},
				"typeName": "binding"
			},
			{
				"x": 360,
				"y": 1410,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:maint-case-diagnose",
				"type": "arrow",
				"parentId": "shape:guide-system",
				"props": {
					"kind": "elbow",
					"elbowMidPoint": 0.5,
					"dash": "solid",
					"size": "s",
					"fill": "none",
					"color": "grey",
					"labelColor": "black",
					"bend": 0,
					"start": {
						"x": 0,
						"y": 0
					},
					"end": {
						"x": 130,
						"y": -60
					},
					"arrowheadStart": "none",
					"arrowheadEnd": "arrow",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph",
								"content": []
							}
						]
					},
					"labelPosition": 0.5,
					"font": "draw",
					"scale": 1
				},
				"index": "aYn6xV",
				"typeName": "shape"
			},
			{
				"x": 530,
				"y": 705,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:conditions",
				"type": "geo",
				"parentId": "shape:guide-system",
				"props": {
					"w": 390,
					"h": 150,
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
										"text": "Required conditions"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Meaning • purpose"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Readability • edit integrity"
									}
								]
							}
						]
					}
				},
				"index": "aGOAU",
				"typeName": "shape"
			},
			{
				"x": 425,
				"y": 307,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:distill-label",
				"type": "text",
				"parentId": "shape:guide-system",
				"props": {
					"color": "black",
					"size": "s",
					"w": 110,
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
										"text": "Distill"
									}
								]
							}
						]
					}
				},
				"index": "aBADr",
				"typeName": "shape"
			},
			{
				"x": 530,
				"y": 925,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:revise",
				"type": "geo",
				"parentId": "shape:guide-system",
				"props": {
					"w": 390,
					"h": 110,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 12,
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
										"text": "Revise structure"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Adjust defaults"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Preserve meaning"
									}
								]
							}
						]
					}
				},
				"index": "aI21b",
				"typeName": "shape"
			},
			{
				"x": 933,
				"y": 742,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:pass-label",
				"type": "text",
				"parentId": "shape:guide-system",
				"props": {
					"color": "black",
					"size": "s",
					"w": 65,
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
										"text": "Pass"
									}
								]
							}
						]
					}
				},
				"index": "aMuIQ",
				"typeName": "shape"
			},
			{
				"x": 60,
				"y": 100,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:subtitle",
				"type": "text",
				"parentId": "shape:guide-system",
				"props": {
					"color": "black",
					"size": "m",
					"w": 1310,
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
										"text": "Distill what the agent needs to act, then improve it with evidence."
									}
								]
							}
						]
					}
				},
				"index": "a2JUm",
				"typeName": "shape"
			},
			{
				"x": 360,
				"y": 1470,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:maint-case-compare",
				"type": "arrow",
				"parentId": "shape:guide-system",
				"props": {
					"kind": "elbow",
					"elbowMidPoint": 0.5,
					"dash": "solid",
					"size": "s",
					"fill": "none",
					"color": "grey",
					"labelColor": "black",
					"bend": 0,
					"start": {
						"x": 0,
						"y": 0
					},
					"end": {
						"x": 130,
						"y": 60
					},
					"arrowheadStart": "none",
					"arrowheadEnd": "arrow",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph",
								"content": []
							}
						]
					},
					"labelPosition": 0.5,
					"font": "draw",
					"scale": 1
				},
				"index": "aZpp0V",
				"typeName": "shape"
			},
			{
				"x": 80,
				"y": 1720,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:maint-retention",
				"type": "text",
				"parentId": "shape:guide-system",
				"props": {
					"color": "black",
					"size": "s",
					"w": 1200,
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
										"text": "Run report: local     Reusable lessons: Git     Applicable actions: Skill"
									}
								]
							}
						]
					}
				},
				"index": "aiRoI",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:pass-end",
				"type": "arrow",
				"fromId": "shape:pass",
				"toId": "shape:refine",
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
				"x": 725,
				"y": 540,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:apply",
				"type": "arrow",
				"parentId": "shape:guide-system",
				"props": {
					"kind": "arc",
					"elbowMidPoint": 0.5,
					"dash": "solid",
					"size": "s",
					"fill": "none",
					"color": "grey",
					"labelColor": "black",
					"bend": 0,
					"start": {
						"x": 0,
						"y": 0
					},
					"end": {
						"x": 0,
						"y": 165
					},
					"arrowheadStart": "none",
					"arrowheadEnd": "arrow",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph",
								"content": []
							}
						]
					},
					"labelPosition": 0.5,
					"font": "draw",
					"scale": 1
				},
				"index": "aGWval",
				"typeName": "shape"
			},
			{
				"x": 80,
				"y": 610,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:use-label",
				"type": "text",
				"parentId": "shape:guide-system",
				"props": {
					"color": "green",
					"size": "l",
					"w": 310,
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
										"text": "NORMAL USE"
									}
								]
							}
						]
					}
				},
				"index": "aDVwX",
				"typeName": "shape"
			},
			{
				"x": 470,
				"y": 1172,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:maintenance-subheading",
				"type": "text",
				"parentId": "shape:guide-system",
				"props": {
					"color": "violet",
					"size": "s",
					"w": 850,
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
										"text": "Select the path for the question"
									}
								]
							}
						]
					}
				},
				"index": "akk0z",
				"typeName": "shape"
			},
			{
				"x": 80,
				"y": 655,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:normal-start",
				"type": "text",
				"parentId": "shape:guide-system",
				"props": {
					"color": "black",
					"size": "s",
					"w": 550,
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
										"text": "User request: purpose • facts • viewing context"
									}
								]
							}
						]
					}
				},
				"index": "aEU7J",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:finish-end",
				"type": "arrow",
				"fromId": "shape:finish",
				"toId": "shape:deliver",
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
				"x": 270,
				"y": 935,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:retry-label",
				"type": "text",
				"parentId": "shape:guide-system",
				"props": {
					"color": "black",
					"size": "s",
					"w": 230,
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
										"text": "Try again"
									}
								]
							}
						]
					}
				},
				"index": "aQrcb",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:maint-verdicts-decision-end",
				"type": "arrow",
				"fromId": "shape:maint-verdicts-decision",
				"toId": "shape:maint-decision",
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
				"id": "binding:maint-compare-verdicts-end",
				"type": "arrow",
				"fromId": "shape:maint-compare-verdicts",
				"toId": "shape:maint-verdicts",
				"props": {
					"isPrecise": true,
					"isExact": false,
					"normalizedAnchor": {
						"x": 0,
						"y": 0.75
					},
					"snap": "none",
					"terminal": "end"
				},
				"typeName": "binding"
			},
			{
				"meta": {},
				"id": "binding:maint-diagnose-verdicts-start",
				"type": "arrow",
				"fromId": "shape:maint-diagnose-verdicts",
				"toId": "shape:maint-diagnose",
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
				"id": "binding:candidate-check-end",
				"type": "arrow",
				"fromId": "shape:candidate-check",
				"toId": "shape:conditions",
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
				"x": 725,
				"y": 855,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:fail",
				"type": "arrow",
				"parentId": "shape:guide-system",
				"props": {
					"kind": "arc",
					"elbowMidPoint": 0.5,
					"dash": "solid",
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
						"x": 0,
						"y": 70
					},
					"arrowheadStart": "none",
					"arrowheadEnd": "arrow",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph",
								"content": []
							}
						]
					},
					"labelPosition": 0.5,
					"font": "draw",
					"scale": 1
				},
				"index": "aIqfq",
				"typeName": "shape"
			},
			{
				"x": 540,
				"y": 190,
				"rotation": 0,
				"isLocked": false,
				"opacity": 0.5,
				"meta": {},
				"id": "shape:skill",
				"type": "geo",
				"parentId": "shape:guide-system",
				"props": {
					"w": 800,
					"h": 350,
					"geo": "rectangle",
					"dash": "solid",
					"growY": 0,
					"url": "",
					"scale": 1,
					"flipX": false,
					"flipY": false,
					"color": "blue",
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
								"type": "paragraph",
								"content": []
							}
						]
					}
				},
				"index": "a5SRI",
				"typeName": "shape"
			},
			{
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:guide-system",
				"type": "frame",
				"props": {
					"w": 1440,
					"h": 1820,
					"name": "From design knowledge to useful diagrams",
					"color": "black"
				},
				"parentId": "page:page",
				"index": "a1v7v",
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
				"x": 60,
				"y": 1140,
				"rotation": 0,
				"isLocked": false,
				"opacity": 0.5,
				"meta": {},
				"id": "shape:maintenance",
				"type": "geo",
				"parentId": "shape:guide-system",
				"props": {
					"w": 1280,
					"h": 620,
					"geo": "rectangle",
					"dash": "solid",
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
								"type": "paragraph",
								"content": []
							}
						]
					}
				},
				"index": "aUSuQ",
				"typeName": "shape"
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
				"x": 490,
				"y": 1470,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:maint-compare",
				"type": "geo",
				"parentId": "shape:guide-system",
				"props": {
					"w": 380,
					"h": 120,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 0,
					"url": "",
					"scale": 1,
					"flipX": false,
					"flipY": false,
					"color": "violet",
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
										"text": "Compare guides"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Fixed tasks • matched runs"
									}
								]
							}
						]
					}
				},
				"index": "aZd4A",
				"typeName": "shape"
			},
			{
				"x": 580,
				"y": 425,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:cue",
				"type": "geo",
				"parentId": "shape:guide-system",
				"props": {
					"w": 720,
					"h": 70,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 10,
					"url": "",
					"scale": 1,
					"flipX": false,
					"flipY": false,
					"color": "blue",
					"labelColor": "black",
					"fill": "none",
					"size": "s",
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
										"text": "Brief rationale at the relevant step"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Only when it helps a decision"
									}
								]
							}
						]
					}
				},
				"index": "a8Okj",
				"typeName": "shape"
			},
			{
				"x": 60,
				"y": 465,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:author-note",
				"type": "text",
				"parentId": "shape:guide-system",
				"props": {
					"color": "black",
					"size": "s",
					"w": 350,
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
										"text": "General theory stays in"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "maintainer documentation."
									}
								]
							}
						]
					}
				},
				"index": "a975U",
				"typeName": "shape"
			},
			{
				"x": 80,
				"y": 1380,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:maint-case",
				"type": "geo",
				"parentId": "shape:guide-system",
				"props": {
					"w": 280,
					"h": 120,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 0,
					"url": "",
					"scale": 1,
					"flipX": false,
					"flipY": false,
					"color": "violet",
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
										"text": "Selected case"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Choose the question"
									}
								]
							}
						]
					}
				},
				"index": "aXwkr",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:pass-start",
				"type": "arrow",
				"fromId": "shape:pass",
				"toId": "shape:conditions",
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
				"x": 750,
				"y": 600,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:apply-label",
				"type": "text",
				"parentId": "shape:guide-system",
				"props": {
					"color": "black",
					"size": "s",
					"w": 220,
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
										"text": "Apply guidance"
									}
								]
							}
						]
					}
				},
				"index": "aTRyf",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:distill-end",
				"type": "arrow",
				"fromId": "shape:distill",
				"toId": "shape:skill",
				"props": {
					"isPrecise": true,
					"isExact": false,
					"normalizedAnchor": {
						"x": 0,
						"y": 0.4714285714285714
					},
					"snap": "none",
					"terminal": "end"
				},
				"typeName": "binding"
			},
			{
				"meta": {},
				"id": "binding:finish-start",
				"type": "arrow",
				"fromId": "shape:finish",
				"toId": "shape:refine",
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
				"meta": {},
				"id": "binding:maint-case-compare-end",
				"type": "arrow",
				"fromId": "shape:maint-case-compare",
				"toId": "shape:maint-compare",
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
				"id": "binding:maint-verdicts-decision-start",
				"type": "arrow",
				"fromId": "shape:maint-verdicts-decision",
				"toId": "shape:maint-verdicts",
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
				"x": 870,
				"y": 1350,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:maint-diagnose-verdicts",
				"type": "arrow",
				"parentId": "shape:guide-system",
				"props": {
					"kind": "elbow",
					"elbowMidPoint": 0.5,
					"dash": "solid",
					"size": "s",
					"fill": "none",
					"color": "grey",
					"labelColor": "black",
					"bend": 0,
					"start": {
						"x": 0,
						"y": 0
					},
					"end": {
						"x": 130,
						"y": 42.5
					},
					"arrowheadStart": "none",
					"arrowheadEnd": "arrow",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph",
								"content": []
							}
						]
					},
					"labelPosition": 0.5,
					"font": "draw",
					"scale": 1
				},
				"index": "aaxVeV",
				"typeName": "shape"
			},
			{
				"x": 743,
				"y": 875,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:fail-label",
				"type": "text",
				"parentId": "shape:guide-system",
				"props": {
					"color": "black",
					"size": "s",
					"w": 170,
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
										"text": "Fail"
									}
								]
							}
						]
					}
				},
				"index": "aOk2A",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:maint-compare-verdicts-start",
				"type": "arrow",
				"fromId": "shape:maint-compare-verdicts",
				"toId": "shape:maint-compare",
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
				"id": "binding:candidate-check-start",
				"type": "arrow",
				"fromId": "shape:candidate-check",
				"toId": "shape:candidate",
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
				"x": 1320,
				"y": 1645,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:feedback",
				"type": "arrow",
				"parentId": "shape:guide-system",
				"props": {
					"kind": "elbow",
					"elbowMidPoint": 0.5,
					"dash": "dashed",
					"size": "s",
					"fill": "none",
					"color": "violet",
					"labelColor": "black",
					"bend": 0,
					"start": {
						"x": 0,
						"y": 0
					},
					"end": {
						"x": 20,
						"y": -1280
					},
					"arrowheadStart": "none",
					"arrowheadEnd": "arrow",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph",
								"content": []
							}
						]
					},
					"labelPosition": 0.5,
					"font": "draw",
					"scale": 1
				},
				"index": "ahFsI",
				"typeName": "shape"
			},
			{
				"x": 560,
				"y": 265,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:runtime",
				"type": "geo",
				"parentId": "shape:guide-system",
				"props": {
					"w": 760,
					"h": 250,
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
					"verticalAlign": "start",
					"richText": {
						"type": "doc",
						"content": [
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Decisions, defaults & exceptions"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Draft → check → refine → save"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Tool and persistence contracts"
									}
								]
							}
						]
					}
				},
				"index": "a7wdj",
				"typeName": "shape"
			},
			{
				"x": 60,
				"y": 40,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:title",
				"type": "text",
				"parentId": "shape:guide-system",
				"props": {
					"color": "black",
					"size": "xl",
					"w": 1310,
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
										"text": "From design knowledge to useful diagrams"
									}
								]
							}
						]
					}
				},
				"index": "a1MHj",
				"typeName": "shape"
			},
			{
				"x": 560,
				"y": 210,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:skill-label",
				"type": "text",
				"parentId": "shape:guide-system",
				"props": {
					"color": "blue",
					"size": "l",
					"w": 750,
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
										"text": "Distributed Skill"
									}
								]
							}
						]
					}
				},
				"index": "a6uir",
				"typeName": "shape"
			}
		]
	}
}
!!!_END_OF_TLDRAW_DATA__DO_NOT_CHANGE_THIS_PHRASE_!!!
```