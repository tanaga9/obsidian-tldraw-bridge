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
				"x": 1160,
				"y": 1520,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-maint-verdicts-decision",
				"type": "arrow",
				"parentId": "shape:ja-guide-system",
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
				"meta": {},
				"id": "binding:ir-test-hypothesis-end-en",
				"type": "arrow",
				"fromId": "shape:ir-test-hypothesis-en",
				"toId": "shape:ir-trial-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"x": 1183.5120922352262,
				"y": 160,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-loop-label-en",
				"type": "text",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"color": "green",
					"size": "m",
					"w": 296.4879077647738,
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
										"text": "Return to diagram work"
									}
								]
							}
						]
					}
				},
				"index": "aoyQn",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:ir-branch-recover-end-en",
				"type": "arrow",
				"fromId": "shape:ir-branch-recover-en",
				"toId": "shape:ir-recover-trigger-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"id": "binding:ir-return-improvement-end-en",
				"type": "arrow",
				"fromId": "shape:ir-return-improvement-en",
				"toId": "shape:ir-resume-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
					"normalizedAnchor": {
						"x": 0.22857142857142856,
						"y": 0
					},
					"snap": "none",
					"terminal": "end"
				},
				"typeName": "binding"
			},
			{
				"x": 810,
				"y": 630,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-recover-trigger-ja",
				"type": "geo",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"w": 640,
					"h": 110,
					"geo": "rectangle",
					"dash": "draw",
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
										"text": "次の変更の根拠がない、または2回修正しても"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "同じ問題が残り、新しい手がかりもない"
									}
								]
							}
						]
					}
				},
				"index": "aDnfb",
				"typeName": "shape"
			},
			{
				"x": 835,
				"y": 800,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-recover-title-ja",
				"type": "text",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"color": "violet",
					"size": "m",
					"w": 590,
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
										"text": "回復：小さな試行で判断材料を得る"
									}
								]
							}
						]
					}
				},
				"index": "aVfMj",
				"typeName": "shape"
			},
			{
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-branch-recover-ja",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-ja",
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
						"x": 930,
						"y": 565
					},
					"end": {
						"x": 1130,
						"y": 630
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
				"index": "aFqev",
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
				"x": 375,
				"y": 1010,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-measure-0-en",
				"type": "geo",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"w": 285,
					"h": 90,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 2,
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
								"content": [
									{
										"type": "text",
										"text": "Time axis +"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "causal connections"
									}
								]
							}
						]
					}
				},
				"index": "aKgBQ",
				"typeName": "shape"
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
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-example-2-ja",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-ja",
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
						"x": 325,
						"y": 1285
					},
					"end": {
						"x": 375,
						"y": 1285
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
				"index": "aREhU",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:ja-pass-end",
				"type": "arrow",
				"fromId": "shape:ja-pass",
				"toId": "shape:ja-refine",
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
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-return-improvement-ja",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-ja",
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
						"x": 370,
						"y": 1520
					},
					"end": {
						"x": 370,
						"y": 1660
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
				"index": "aiTYE",
				"typeName": "shape"
			},
			{
				"x": 410,
				"y": 780,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-candidate-check",
				"type": "arrow",
				"parentId": "shape:ja-guide-system",
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
				"meta": {},
				"id": "binding:ir-inspect-trial-start-ja",
				"type": "arrow",
				"fromId": "shape:ir-inspect-trial-ja",
				"toId": "shape:ir-trial-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"id": "binding:ir-example-2-start-en",
				"type": "arrow",
				"fromId": "shape:ir-example-2-en",
				"toId": "shape:ir-symptom-2-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"x": 50,
				"y": 90,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-subtitle-ja",
				"type": "text",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"color": "black",
					"size": "m",
					"w": 1400,
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
										"text": "問題に具体策を当てる。次の判断に根拠がないときは、小さく試して方向を探る。"
									}
								]
							}
						]
					}
				},
				"index": "a26TQ",
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
				"x": 80,
				"y": 1400,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-apply-ja",
				"type": "geo",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"w": 580,
					"h": 120,
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
										"text": "依頼範囲で提案・編集"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "部分修正も全面再設計も可。情報を引き継ぐ"
									}
								]
							}
						]
					}
				},
				"index": "aSO7b",
				"typeName": "shape"
			},
			{
				"x": 80,
				"y": 1240,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-symptom-2-ja",
				"type": "geo",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"w": 245,
					"h": 90,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 2,
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
								"content": [
									{
										"type": "text",
										"text": "全体表示では"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "文字が読めない"
									}
								]
							}
						]
					}
				},
				"index": "aPGiv",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:ir-loop-up-end-ja",
				"type": "arrow",
				"fromId": "shape:ir-loop-up-ja",
				"toId": "shape:ir-loop-label-ja",
				"props": {
					"isPrecise": true,
					"isExact": false,
					"normalizedAnchor": {
						"x": 1,
						"y": 0.5
					},
					"snap": "edge-point",
					"terminal": "end"
				},
				"typeName": "binding"
			},
			{
				"x": 60,
				"y": 265,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-knowledge",
				"type": "geo",
				"parentId": "shape:ja-guide-system",
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
										"text": "基礎・設計原則"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "知覚・認知"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "意味・設計上のトレードオフ"
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
				"x": 845,
				"y": 1410,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-supported-ja",
				"type": "geo",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"w": 265,
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
										"text": "根拠が得られた"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "次の変更を決める"
									}
								]
							}
						]
					}
				},
				"index": "addwz",
				"typeName": "shape"
			},
			{
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-example-1-ja",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-ja",
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
						"x": 325,
						"y": 1170
					},
					"end": {
						"x": 375,
						"y": 1170
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
				"index": "aOSxQ",
				"typeName": "shape"
			},
			{
				"x": 50,
				"y": 1810,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-boundary-en",
				"type": "text",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"color": "black",
					"size": "s",
					"w": 1400,
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
										"text": "These are conditional aids, not mandatory extra phases. SDK or saving errors use operation recovery."
									}
								]
							}
						]
					}
				},
				"index": "alUzsV",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:ir-example-1-start-en",
				"type": "arrow",
				"fromId": "shape:ir-example-1-en",
				"toId": "shape:ir-symptom-1-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"meta": {
					"diagramId": "diagramming-guide-design-system",
					"language": "ja"
				},
				"id": "page:guide-design-system-ja",
				"name": "Design system / 日本語",
				"index": "a2IQX",
				"typeName": "page"
			},
			{
				"x": 50,
				"y": 780,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-improve-region-en",
				"type": "geo",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"w": 640,
					"h": 780,
					"geo": "rectangle",
					"dash": "draw",
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
				"index": "aGFeM",
				"typeName": "shape"
			},
			{
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-start-improve-ja",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-ja",
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
						"x": 370,
						"y": 710
					},
					"end": {
						"x": 370,
						"y": 865
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
				"index": "aGzz9rX",
				"typeName": "shape"
			},
			{
				"x": 1320,
				"y": 1661,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-feedback",
				"type": "arrow",
				"parentId": "shape:ja-guide-system",
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
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-result-ask-en",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-en",
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
						"x": 1265,
						"y": 1335
					},
					"end": {
						"x": 1272,
						"y": 1410
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
				"index": "agzyi",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:ir-result-supported-start-ja",
				"type": "arrow",
				"fromId": "shape:ir-result-supported-ja",
				"toId": "shape:ir-inspect-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
					"normalizedAnchor": {
						"x": 0.25,
						"y": 1
					},
					"snap": "none",
					"terminal": "start"
				},
				"typeName": "binding"
			},
			{
				"x": 80,
				"y": 1125,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-symptom-1-ja",
				"type": "geo",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"w": 245,
					"h": 90,
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
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "対象を想像しにくい"
									}
								]
							}
						]
					}
				},
				"index": "aMREb",
				"typeName": "shape"
			},
			{
				"x": 743,
				"y": 875,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-fail-label",
				"type": "text",
				"parentId": "shape:ja-guide-system",
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
										"text": "不合格"
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
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-example-0-ja",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-ja",
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
						"x": 325,
						"y": 1055
					},
					"end": {
						"x": 375,
						"y": 1055
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
				"index": "aLKze",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:ja-finish-end",
				"type": "arrow",
				"fromId": "shape:ja-finish",
				"toId": "shape:ja-deliver",
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
				"id": "binding:ja-apply-start",
				"type": "arrow",
				"fromId": "shape:ja-apply",
				"toId": "shape:ja-skill",
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
				"meta": {},
				"id": "binding:ir-ongoing-user-start-ja",
				"type": "arrow",
				"fromId": "shape:ir-ongoing-user-ja",
				"toId": "shape:ir-ongoing-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
					"normalizedAnchor": {
						"x": 0.25,
						"y": 1
					},
					"snap": "none",
					"terminal": "start"
				},
				"typeName": "binding"
			},
			{
				"x": 80,
				"y": 1010,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-symptom-0-ja",
				"type": "geo",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"w": 245,
					"h": 90,
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
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "時系列と因果が混在"
									}
								]
							}
						]
					}
				},
				"index": "aJsWX",
				"typeName": "shape"
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
				"id": "binding:ja-maint-compare-verdicts-end",
				"type": "arrow",
				"fromId": "shape:ja-maint-compare-verdicts",
				"toId": "shape:ja-maint-verdicts",
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
				"id": "binding:ir-start-improve-start-en",
				"type": "arrow",
				"fromId": "shape:ir-start-improve-en",
				"toId": "shape:ir-improve-trigger-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"id": "binding:ir-example-0-start-en",
				"type": "arrow",
				"fromId": "shape:ir-example-0-en",
				"toId": "shape:ir-symptom-0-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"id": "binding:ir-normal-candidate-start-ja",
				"type": "arrow",
				"fromId": "shape:ir-normal-candidate-ja",
				"toId": "shape:ir-candidate-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"id": "binding:ir-normal-refine-end-en",
				"type": "arrow",
				"fromId": "shape:ir-normal-refine-en",
				"toId": "shape:ir-check-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
					"normalizedAnchor": {
						"x": 0.75,
						"y": 0
					},
					"snap": "none",
					"terminal": "end"
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
				"id": "shape:ir-inspect-trial-en",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-en",
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
						"x": 1125,
						"y": 1160
					},
					"end": {
						"x": 1125,
						"y": 1235
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
				"index": "abNtz",
				"typeName": "shape"
			},
			{
				"x": 60,
				"y": 590,
				"rotation": 0,
				"isLocked": false,
				"opacity": 0.5,
				"meta": {},
				"id": "shape:ja-normal",
				"type": "geo",
				"parentId": "shape:ja-guide-system",
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
				"meta": {},
				"id": "binding:ja-maint-diagnose-verdicts-end",
				"type": "arrow",
				"fromId": "shape:ja-maint-diagnose-verdicts",
				"toId": "shape:ja-maint-verdicts",
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
				"meta": {},
				"id": "binding:ir-ongoing-agent-end-en",
				"type": "arrow",
				"fromId": "shape:ir-ongoing-agent-en",
				"toId": "shape:ir-deliver-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"x": 1140,
				"y": 1575,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-wait-note-ja",
				"type": "text",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"color": "black",
					"size": "s",
					"w": 265,
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
										"text": "必要な回答を得てから"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "再開する。"
									}
								]
							}
						]
					}
				},
				"index": "akqXv",
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
				"meta": {},
				"id": "binding:ir-return-recovery-end-en",
				"type": "arrow",
				"fromId": "shape:ir-return-recovery-en",
				"toId": "shape:ir-resume-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
					"normalizedAnchor": {
						"x": 0.6621428571428571,
						"y": 0
					},
					"snap": "none",
					"terminal": "end"
				},
				"typeName": "binding"
			},
			{
				"x": 1000,
				"y": 1340,
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
				"meta": {},
				"id": "binding:ir-branch-improve-start-en",
				"type": "arrow",
				"fromId": "shape:ir-branch-improve-en",
				"toId": "shape:ir-check-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
					"normalizedAnchor": {
						"x": 0.25,
						"y": 1
					},
					"snap": "none",
					"terminal": "start"
				},
				"typeName": "binding"
			},
			{
				"meta": {},
				"id": "binding:ir-start-recover-start-ja",
				"type": "arrow",
				"fromId": "shape:ir-start-recover-ja",
				"toId": "shape:ir-recover-trigger-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"x": 410,
				"y": 622,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-use-subheading",
				"type": "text",
				"parentId": "shape:ja-guide-system",
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
										"text": "依頼から役立つ図へ"
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
				"x": 410,
				"y": 355,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-distill",
				"type": "arrow",
				"parentId": "shape:ja-guide-system",
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
				"x": 390,
				"y": 155,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-ongoing-en",
				"type": "geo",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"w": 720,
					"h": 90,
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
										"text": "ONGOING DIAGRAM CREATION AND IMPROVEMENT"
									}
								]
							}
						]
					}
				},
				"index": "anIIA",
				"typeName": "shape"
			},
			{
				"x": 80,
				"y": 705,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-candidate",
				"type": "geo",
				"parentId": "shape:ja-guide-system",
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
										"text": "エージェントが構造案を作る"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "見た目より先に構造を設計"
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
				"x": 1001.4036461617939,
				"y": 1562.0502397355067,
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
				"id": "binding:ja-pass-start",
				"type": "arrow",
				"fromId": "shape:ja-pass",
				"toId": "shape:ja-conditions",
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
				"x": 390,
				"y": 470,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-check-ja",
				"type": "geo",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"w": 720,
					"h": 95,
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
										"text": "目的と現状を確認する"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "問題に合う施策、または次の仮説を選べるか？"
									}
								]
							}
						]
					}
				},
				"index": "a6K8I",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:ir-test-hypothesis-start-ja",
				"type": "arrow",
				"fromId": "shape:ir-test-hypothesis-ja",
				"toId": "shape:ir-hypothesis-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"id": "binding:ir-return-improvement-start-ja",
				"type": "arrow",
				"fromId": "shape:ir-return-improvement-ja",
				"toId": "shape:ir-apply-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"id": "binding:ir-branch-recover-start-ja",
				"type": "arrow",
				"fromId": "shape:ir-branch-recover-ja",
				"toId": "shape:ir-check-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
					"normalizedAnchor": {
						"x": 0.75,
						"y": 1
					},
					"snap": "none",
					"terminal": "start"
				},
				"typeName": "binding"
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
				"x": 1000,
				"y": 925,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-deliver",
				"type": "geo",
				"parentId": "shape:ja-guide-system",
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
										"text": "役立つ図"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "保存して届ける"
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
				"x": 1140,
				"y": 1410,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-ask-en",
				"type": "geo",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"w": 265,
					"h": 110,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 0,
					"url": "",
					"scale": 1,
					"flipX": false,
					"flipY": false,
					"color": "orange",
					"labelColor": "black",
					"fill": "solid",
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
										"text": "No finding twice?"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Ask one specific question;"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "wait for the answer"
									}
								]
							}
						]
					}
				},
				"index": "aeIjz",
				"typeName": "shape"
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
				"id": "binding:ir-inspect-trial-end-ja",
				"type": "arrow",
				"fromId": "shape:ir-inspect-trial-ja",
				"toId": "shape:ir-inspect-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"id": "binding:ir-example-2-end-en",
				"type": "arrow",
				"fromId": "shape:ir-example-2-en",
				"toId": "shape:ir-measure-2-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-start-recover-en",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-en",
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
						"x": 1130,
						"y": 710
					},
					"end": {
						"x": 1125,
						"y": 865
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
				"index": "aUrd8V",
				"typeName": "shape"
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
				"meta": {},
				"id": "binding:ir-result-ask-start-en",
				"type": "arrow",
				"fromId": "shape:ir-result-ask-en",
				"toId": "shape:ir-inspect-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
					"normalizedAnchor": {
						"x": 0.75,
						"y": 1
					},
					"snap": "none",
					"terminal": "start"
				},
				"typeName": "binding"
			},
			{
				"meta": {},
				"id": "binding:ja-finish-start",
				"type": "arrow",
				"fromId": "shape:ja-finish",
				"toId": "shape:ja-refine",
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
				"id": "binding:ir-example-1-end-en",
				"type": "arrow",
				"fromId": "shape:ir-example-1-en",
				"toId": "shape:ir-measure-1-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"x": 1000,
				"y": 1340,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-maint-verdicts",
				"type": "geo",
				"parentId": "shape:ja-guide-system",
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
										"text": "3つの判定"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "目的の達成"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "影響箇所の品質"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "既存内容の保持"
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
				"x": 50,
				"y": 30,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-title-en",
				"type": "text",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"color": "black",
					"size": "l",
					"w": 1400,
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
										"text": "Improvement and recovery in diagram work"
									}
								]
							}
						]
					}
				},
				"index": "a1ItI",
				"typeName": "shape"
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
				"meta": {},
				"id": "binding:ir-result-supported-end-ja",
				"type": "arrow",
				"fromId": "shape:ir-result-supported-ja",
				"toId": "shape:ir-supported-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"x": 80,
				"y": 1205,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-maintenance-note",
				"type": "text",
				"parentId": "shape:ja-guide-system",
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
										"text": "対象範囲・初期不具合を固定し、経過時間とCLI呼び出し回数を記録"
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
				"meta": {},
				"id": "binding:ja-maint-case-compare-end",
				"type": "arrow",
				"fromId": "shape:ja-maint-case-compare",
				"toId": "shape:ja-maint-compare",
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
				"x": 80,
				"y": 865,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-match-ja",
				"type": "geo",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"w": 580,
					"h": 105,
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
										"text": "兆候 → 施策 → 期待する効果"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "必要なら、直感的な選択肢で確かめる"
									}
								]
							}
						]
					}
				},
				"index": "aIX2X",
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
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-test-hypothesis-en",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-en",
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
						"x": 1125,
						"y": 975
					},
					"end": {
						"x": 1125,
						"y": 1050
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
				"index": "aXo7DV",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:ja-maint-compare-verdicts-start",
				"type": "arrow",
				"fromId": "shape:ja-maint-compare-verdicts",
				"toId": "shape:ja-maint-compare",
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
				"id": "binding:ir-normal-candidate-end-ja",
				"type": "arrow",
				"fromId": "shape:ir-normal-candidate-ja",
				"toId": "shape:ir-check-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
					"normalizedAnchor": {
						"x": 0.25,
						"y": 0
					},
					"snap": "none",
					"terminal": "end"
				},
				"typeName": "binding"
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
				"x": 810,
				"y": 300,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-deliver-ja",
				"type": "geo",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"w": 640,
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
										"text": "エージェントの自律検知"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "具体的な問題・改善の機会・設計の停滞"
									}
								]
							}
						]
					}
				},
				"index": "a84JE",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:ja-maint-verdicts-decision-end",
				"type": "arrow",
				"fromId": "shape:ja-maint-verdicts-decision",
				"toId": "shape:ja-maint-decision",
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
				"id": "binding:ir-ongoing-user-end-ja",
				"type": "arrow",
				"fromId": "shape:ir-ongoing-user-ja",
				"toId": "shape:ir-candidate-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"x": 1000,
				"y": 705,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-refine",
				"type": "geo",
				"parentId": "shape:ja-guide-system",
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
										"text": "仕上げ・検証"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "導線・外観・作業量"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "確認・保存"
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
				"meta": {},
				"id": "binding:ir-example-0-end-en",
				"type": "arrow",
				"fromId": "shape:ir-example-0-en",
				"toId": "shape:ir-measure-0-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"id": "binding:ir-start-improve-end-en",
				"type": "arrow",
				"fromId": "shape:ir-start-improve-en",
				"toId": "shape:ir-improve-region-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-loop-up-ja",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"kind": "elbow",
					"elbowMidPoint": 0.5,
					"dash": "solid",
					"size": "m",
					"fill": "none",
					"color": "green",
					"labelColor": "black",
					"bend": 0,
					"start": {
						"x": 1450,
						"y": 1725
					},
					"end": {
						"x": 1110,
						"y": 200
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
				"index": "apT1I",
				"typeName": "shape"
			},
			{
				"x": 845,
				"y": 1029,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-trial-en",
				"type": "geo",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"w": 560,
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
										"text": "Draw an actual small example"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Core 3–5 elements / one case / two drafts"
									}
								]
							}
						]
					}
				},
				"index": "aXQw6",
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
				"meta": {},
				"id": "binding:ja-maint-diagnose-verdicts-start",
				"type": "arrow",
				"fromId": "shape:ja-maint-diagnose-verdicts",
				"toId": "shape:ja-maint-diagnose",
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
				"id": "binding:ir-ongoing-agent-start-ja",
				"type": "arrow",
				"fromId": "shape:ir-ongoing-agent-ja",
				"toId": "shape:ir-ongoing-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
					"normalizedAnchor": {
						"x": 0.75,
						"y": 1
					},
					"snap": "none",
					"terminal": "start"
				},
				"typeName": "binding"
			},
			{
				"meta": {},
				"id": "binding:ir-normal-refine-start-ja",
				"type": "arrow",
				"fromId": "shape:ir-normal-refine-ja",
				"toId": "shape:ir-deliver-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"id": "binding:ja-candidate-check-end",
				"type": "arrow",
				"fromId": "shape:ja-candidate-check",
				"toId": "shape:ja-conditions",
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
				"x": 530,
				"y": 980,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-retry",
				"type": "arrow",
				"parentId": "shape:ja-guide-system",
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
				"x": 1001.4036461617939,
				"y": 1562.0502397355067,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-maint-decision",
				"type": "geo",
				"parentId": "shape:ja-guide-system",
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
										"text": "維持・簡素化・改訂"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "根拠の範囲で判断"
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
				"meta": {},
				"id": "binding:ir-branch-improve-end-en",
				"type": "arrow",
				"fromId": "shape:ir-branch-improve-en",
				"toId": "shape:ir-improve-trigger-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"x": 375,
				"y": 1240,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-measure-2-ja",
				"type": "geo",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"w": 285,
					"h": 90,
					"geo": "rectangle",
					"dash": "draw",
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
								"content": [
									{
										"type": "text",
										"text": "概要と詳細を分ける"
									}
								]
							}
						]
					}
				},
				"index": "aQpgz",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:ir-start-recover-end-ja",
				"type": "arrow",
				"fromId": "shape:ir-start-recover-ja",
				"toId": "shape:ir-recover-region-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"x": 360,
				"y": 1410,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-maint-case-diagnose",
				"type": "arrow",
				"parentId": "shape:ja-guide-system",
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
				"x": 50,
				"y": 300,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-candidate-ja",
				"type": "geo",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"w": 640,
					"h": 110,
					"geo": "rectangle",
					"dash": "draw",
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
										"text": "ユーザーの声"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "「わかりにくい」「もっと伝わる図にしたい」"
									}
								]
							}
						]
					}
				},
				"index": "a50o6",
				"typeName": "shape"
			},
			{
				"x": 75,
				"y": 800,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-improve-title-ja",
				"type": "text",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"color": "green",
					"size": "m",
					"w": 590,
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
										"text": "改善：問題に合う具体策を選ぶ"
									}
								]
							}
						]
					}
				},
				"index": "aHkrA",
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
				"x": 272.38484174786504,
				"y": 1660,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-resume-ja",
				"type": "geo",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"w": 944.9706844022611,
					"h": 130,
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
										"text": "根拠ある次の一手を得る"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "依頼範囲で修正・確認・仕上げ・保存。不要な試作は整理。"
									}
								]
							}
						]
					}
				},
				"index": "ahD4I",
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
				"x": 50,
				"y": 630,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-improve-trigger-ja",
				"type": "geo",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"w": 640,
					"h": 110,
					"geo": "rectangle",
					"dash": "draw",
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
										"text": "兆候と改善効果を説明でき、"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "具体策を選べる"
									}
								]
							}
						]
					}
				},
				"index": "aCjrz",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:ir-loop-up-start-en",
				"type": "arrow",
				"fromId": "shape:ir-loop-up-en",
				"toId": "shape:ir-resume-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"id": "binding:ir-return-recovery-start-ja",
				"type": "arrow",
				"fromId": "shape:ir-return-recovery-ja",
				"toId": "shape:ir-supported-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"id": "shape:ir-branch-improve-ja",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-ja",
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
						"x": 570,
						"y": 565
					},
					"end": {
						"x": 370,
						"y": 630
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
				"index": "aCssfl",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:ja-fail-end",
				"type": "arrow",
				"fromId": "shape:ja-fail",
				"toId": "shape:ja-revise",
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
				"meta": {
					"diagramId": "diagram-improvement-recovery",
					"language": "ja"
				},
				"id": "page:improvement-recovery-ja",
				"name": "Improvement and recovery / 日本語",
				"index": "a4ic2",
				"typeName": "page"
			},
			{
				"x": 490,
				"y": 1290,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-maint-diagnose",
				"type": "geo",
				"parentId": "shape:ja-guide-system",
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
										"text": "不具合を診断"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "再現 → 修正 → 再確認"
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
				"x": 0,
				"y": 0,
				"z": 1,
				"meta": {},
				"id": "camera:page:guide-design-system-ja",
				"typeName": "camera"
			},
			{
				"x": 425,
				"y": 307,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-distill-label",
				"type": "text",
				"parentId": "shape:ja-guide-system",
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
										"text": "要点を抽出"
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
				"x": 845,
				"y": 1197,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-inspect-en",
				"type": "geo",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"w": 560,
					"h": 130,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 22,
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
										"text": "Inspect: supported / rejected / inconclusive"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Rejected → change the hypothesis"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "before another trial"
									}
								]
							}
						]
					}
				},
				"index": "aYPzR",
				"typeName": "shape"
			},
			{
				"x": 1145,
				"y": 745,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-initial-recovery-en",
				"type": "text",
				"parentId": "shape:improvement-recovery-en",
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
										"text": "Also for initial design."
									}
								]
							}
						]
					}
				},
				"index": "am7eE",
				"typeName": "shape"
			},
			{
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-result-supported-en",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-en",
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
						"x": 985,
						"y": 1335
					},
					"end": {
						"x": 977,
						"y": 1410
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
				"index": "adsKpV",
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
				"x": 375,
				"y": 1125,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-measure-1-ja",
				"type": "geo",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"w": 285,
					"h": 90,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 2,
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
								"content": [
									{
										"type": "text",
										"text": "要所に小さなアイコン"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "ラベルも残す"
									}
								]
							}
						]
					}
				},
				"index": "aNThA",
				"typeName": "shape"
			},
			{
				"x": 920,
				"y": 780,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-pass",
				"type": "arrow",
				"parentId": "shape:ja-guide-system",
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
				"meta": {},
				"id": "binding:ir-test-hypothesis-end-ja",
				"type": "arrow",
				"fromId": "shape:ir-test-hypothesis-ja",
				"toId": "shape:ir-trial-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"x": 1183.5120922352262,
				"y": 160,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-loop-label-ja",
				"type": "text",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"color": "green",
					"size": "m",
					"w": 296.4879077647738,
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
										"text": "通常の作図・改善へ戻る"
									}
								]
							}
						]
					}
				},
				"index": "aoOEn",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:ir-branch-recover-end-ja",
				"type": "arrow",
				"fromId": "shape:ir-branch-recover-ja",
				"toId": "shape:ir-recover-trigger-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"id": "binding:ir-return-improvement-end-ja",
				"type": "arrow",
				"fromId": "shape:ir-return-improvement-ja",
				"toId": "shape:ir-resume-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
					"normalizedAnchor": {
						"x": 0.22857142857142856,
						"y": 0
					},
					"snap": "none",
					"terminal": "end"
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
				"id": "shape:ir-ongoing-agent-en",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-en",
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
						"x": 930,
						"y": 245
					},
					"end": {
						"x": 1130,
						"y": 300
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
				"index": "anTWdl",
				"typeName": "shape"
			},
			{
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-ongoing-user-en",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-en",
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
						"x": 570,
						"y": 245
					},
					"end": {
						"x": 370,
						"y": 300
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
				"index": "ansUkV",
				"typeName": "shape"
			},
			{
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-normal-refine-en",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-en",
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
						"x": 1130,
						"y": 410
					},
					"end": {
						"x": 930,
						"y": 470
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
				"index": "aByfE",
				"typeName": "shape"
			},
			{
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-normal-candidate-en",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-en",
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
						"x": 370,
						"y": 410
					},
					"end": {
						"x": 570,
						"y": 470
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
				"index": "a6goOV",
				"typeName": "shape"
			},
			{
				"x": 375,
				"y": 1010,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-measure-0-ja",
				"type": "geo",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"w": 285,
					"h": 90,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 2,
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
								"content": [
									{
										"type": "text",
										"text": "時間軸と"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "因果の矢印を分ける"
									}
								]
							}
						]
					}
				},
				"index": "aK9hz",
				"typeName": "shape"
			},
			{
				"x": 810,
				"y": 780,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-recover-region-en",
				"type": "geo",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"w": 640,
					"h": 780,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 0,
					"url": "",
					"scale": 1,
					"flipX": false,
					"flipY": false,
					"color": "violet",
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
				"index": "aUZhI",
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
				"x": 50,
				"y": 1810,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-boundary-ja",
				"type": "text",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"color": "black",
					"size": "s",
					"w": 1400,
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
										"text": "毎回必須の工程ではありません。SDK・保存の不具合は、別の操作復旧手順で対応します。"
									}
								]
							}
						]
					}
				},
				"index": "alagQ",
				"typeName": "shape"
			},
			{
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-return-recovery-en",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-en",
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
						"x": 977,
						"y": 1520
					},
					"end": {
						"x": 977,
						"y": 1660
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
				"index": "aj8lv",
				"typeName": "shape"
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
				"x": 80,
				"y": 1688,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-maint-retention",
				"type": "text",
				"parentId": "shape:ja-guide-system",
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
										"text": "実行レポート：ローカル　　再利用できる知見：Git　　適用可能な手順：Skill"
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
				"id": "binding:ir-example-2-start-ja",
				"type": "arrow",
				"fromId": "shape:ir-example-2-ja",
				"toId": "shape:ir-symptom-2-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"x": 60,
				"y": 205,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-author-label",
				"type": "text",
				"parentId": "shape:ja-guide-system",
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
										"text": "ガイド設計の知識"
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
				"x": 845,
				"y": 865,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-hypothesis-en",
				"type": "geo",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"w": 560,
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
										"text": "Name one unknown and one hypothesis"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Define what result would decide the next step"
									}
								]
							}
						]
					}
				},
				"index": "aW7fQ",
				"typeName": "shape"
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
				"meta": {},
				"id": "binding:ir-example-1-start-ja",
				"type": "arrow",
				"fromId": "shape:ir-example-1-ja",
				"toId": "shape:ir-symptom-1-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"x": 50,
				"y": 780,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-improve-region-ja",
				"type": "geo",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"w": 640,
					"h": 780,
					"geo": "rectangle",
					"dash": "draw",
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
				"index": "aGzxB",
				"typeName": "shape"
			},
			{
				"x": 1160,
				"y": 855,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-finish",
				"type": "arrow",
				"parentId": "shape:ja-guide-system",
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
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-result-ask-ja",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-ja",
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
						"x": 1265,
						"y": 1335
					},
					"end": {
						"x": 1272,
						"y": 1410
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
				"index": "agtzD",
				"typeName": "shape"
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
				"meta": {},
				"id": "binding:ja-distill-end",
				"type": "arrow",
				"fromId": "shape:ja-distill",
				"toId": "shape:ja-skill",
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
				"id": "binding:ir-result-ask-end-en",
				"type": "arrow",
				"fromId": "shape:ir-result-ask-en",
				"toId": "shape:ir-ask-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"id": "binding:ja-maint-case-compare-start",
				"type": "arrow",
				"fromId": "shape:ja-maint-case-compare",
				"toId": "shape:ja-maint-case",
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
				"x": 80,
				"y": 610,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-use-label",
				"type": "text",
				"parentId": "shape:ja-guide-system",
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
										"text": "通常の作図"
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
				"meta": {},
				"id": "binding:ja-maint-verdicts-decision-start",
				"type": "arrow",
				"fromId": "shape:ja-maint-verdicts-decision",
				"toId": "shape:ja-maint-verdicts",
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
				"y": 1530,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-maint-compare-verdicts",
				"type": "arrow",
				"parentId": "shape:ja-guide-system",
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
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:improvement-recovery-en",
				"type": "frame",
				"parentId": "page:improvement-recovery-en",
				"props": {
					"w": 1600,
					"h": 1860,
					"name": "improvement-and-recovery",
					"color": "black"
				},
				"index": "a18TA",
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
				"x": 725,
				"y": 540,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-apply",
				"type": "arrow",
				"parentId": "shape:ja-guide-system",
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
				"meta": {},
				"id": "binding:ir-start-improve-start-ja",
				"type": "arrow",
				"fromId": "shape:ir-start-improve-ja",
				"toId": "shape:ir-improve-trigger-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"id": "binding:ir-example-0-start-ja",
				"type": "arrow",
				"fromId": "shape:ir-example-0-ja",
				"toId": "shape:ir-symptom-0-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"meta": {},
				"id": "binding:ir-ongoing-agent-end-ja",
				"type": "arrow",
				"fromId": "shape:ir-ongoing-agent-ja",
				"toId": "shape:ir-deliver-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"id": "binding:ir-normal-refine-end-ja",
				"type": "arrow",
				"fromId": "shape:ir-normal-refine-ja",
				"toId": "shape:ir-check-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
					"normalizedAnchor": {
						"x": 0.75,
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
				"id": "shape:ja-retry-label",
				"type": "text",
				"parentId": "shape:ja-guide-system",
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
										"text": "再試行"
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
				"x": 810,
				"y": 630,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-recover-trigger-en",
				"type": "geo",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"w": 640,
					"h": 110,
					"geo": "rectangle",
					"dash": "draw",
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
										"text": "No supported next change, or two revisions"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "leave the same issue without a new finding"
									}
								]
							}
						]
					}
				},
				"index": "aDAij",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:ja-candidate-check-start",
				"type": "arrow",
				"fromId": "shape:ja-candidate-check",
				"toId": "shape:ja-candidate",
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
				"x": 835,
				"y": 800,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-recover-title-en",
				"type": "text",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"color": "violet",
					"size": "m",
					"w": 590,
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
										"text": "RECOVERY: learn through a small trial"
									}
								]
							}
						]
					}
				},
				"index": "aVKgX",
				"typeName": "shape"
			},
			{
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-branch-recover-en",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-en",
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
						"x": 930,
						"y": 565
					},
					"end": {
						"x": 1130,
						"y": 630
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
				"index": "aFdcv",
				"typeName": "shape"
			},
			{
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-inspect-trial-ja",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-ja",
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
						"x": 1125,
						"y": 1160
					},
					"end": {
						"x": 1125,
						"y": 1235
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
				"index": "abUIe",
				"typeName": "shape"
			},
			{
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-example-2-en",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-en",
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
						"x": 325,
						"y": 1285
					},
					"end": {
						"x": 375,
						"y": 1285
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
				"index": "aRdzq",
				"typeName": "shape"
			},
			{
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-return-improvement-en",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-en",
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
						"x": 370,
						"y": 1520
					},
					"end": {
						"x": 370,
						"y": 1660
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
				"index": "ailsQ",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:ir-inspect-trial-start-en",
				"type": "arrow",
				"fromId": "shape:ir-inspect-trial-en",
				"toId": "shape:ir-trial-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"x": 50,
				"y": 90,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-subtitle-en",
				"type": "text",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"color": "black",
					"size": "m",
					"w": 1400,
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
										"text": "Improve a known problem. Recover when the next design decision has no support."
									}
								]
							}
						]
					}
				},
				"index": "a2WxU",
				"typeName": "shape"
			},
			{
				"x": 80,
				"y": 1400,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-apply-en",
				"type": "geo",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"w": 580,
					"h": 120,
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
										"text": "Recommend / edit within scope"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Local fix or full rebuild; retain useful facts"
									}
								]
							}
						]
					}
				},
				"index": "aS89v",
				"typeName": "shape"
			},
			{
				"x": 80,
				"y": 1240,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-symptom-2-en",
				"type": "geo",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"w": 245,
					"h": 90,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 2,
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
								"content": [
									{
										"type": "text",
										"text": "Overview text"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "is too small"
									}
								]
							}
						]
					}
				},
				"index": "aPRIQ",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:ir-loop-up-end-en",
				"type": "arrow",
				"fromId": "shape:ir-loop-up-en",
				"toId": "shape:ir-loop-label-en",
				"props": {
					"isPrecise": true,
					"isExact": false,
					"normalizedAnchor": {
						"x": 1,
						"y": 0.5
					},
					"snap": "edge-point",
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
				"id": "instance_page_state:page:guide-design-system-ja",
				"pageId": "page:guide-design-system-ja",
				"typeName": "instance_page_state"
			},
			{
				"meta": {},
				"id": "binding:ir-return-recovery-end-ja",
				"type": "arrow",
				"fromId": "shape:ir-return-recovery-ja",
				"toId": "shape:ir-resume-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
					"normalizedAnchor": {
						"x": 0.6621428571428571,
						"y": 0
					},
					"snap": "none",
					"terminal": "end"
				},
				"typeName": "binding"
			},
			{
				"x": 845,
				"y": 1410,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-supported-en",
				"type": "geo",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"w": 265,
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
										"text": "Evidence supports"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "the next change"
									}
								]
							}
						]
					}
				},
				"index": "adMdr",
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
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-example-1-en",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-en",
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
						"x": 325,
						"y": 1170
					},
					"end": {
						"x": 375,
						"y": 1170
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
				"index": "aOAOz",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:ir-branch-improve-start-ja",
				"type": "arrow",
				"fromId": "shape:ir-branch-improve-ja",
				"toId": "shape:ir-check-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
					"normalizedAnchor": {
						"x": 0.25,
						"y": 1
					},
					"snap": "none",
					"terminal": "start"
				},
				"typeName": "binding"
			},
			{
				"x": 80,
				"y": 1688,
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
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-start-improve-en",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-en",
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
						"x": 370,
						"y": 710
					},
					"end": {
						"x": 370,
						"y": 865
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
				"index": "aGrtGV",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:ja-feedback-end",
				"type": "arrow",
				"fromId": "shape:ja-feedback",
				"toId": "shape:ja-skill",
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
				"id": "binding:ir-result-supported-start-en",
				"type": "arrow",
				"fromId": "shape:ir-result-supported-en",
				"toId": "shape:ir-inspect-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
					"normalizedAnchor": {
						"x": 0.25,
						"y": 1
					},
					"snap": "none",
					"terminal": "start"
				},
				"typeName": "binding"
			},
			{
				"x": 80,
				"y": 1125,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-symptom-1-en",
				"type": "geo",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"w": 245,
					"h": 90,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 2,
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
								"content": [
									{
										"type": "text",
										"text": "Entities are hard"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "to picture"
									}
								]
							}
						]
					}
				},
				"index": "aMAtv",
				"typeName": "shape"
			},
			{
				"x": 540,
				"y": 218.91371270584597,
				"rotation": 0,
				"isLocked": false,
				"opacity": 0.5,
				"meta": {},
				"id": "shape:ja-skill",
				"type": "geo",
				"parentId": "shape:ja-guide-system",
				"props": {
					"w": 800,
					"h": 291.10191229415403,
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
				"id": "shape:ir-example-0-en",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-en",
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
						"x": 325,
						"y": 1055
					},
					"end": {
						"x": 375,
						"y": 1055
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
				"index": "aL9YI",
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
				"meta": {},
				"id": "binding:ja-fail-start",
				"type": "arrow",
				"fromId": "shape:ja-fail",
				"toId": "shape:ja-conditions",
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
				"x": 390,
				"y": 155,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-ongoing-ja",
				"type": "geo",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"w": 720,
					"h": 90,
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
										"text": "通常の作図・改善"
									}
								]
							}
						]
					}
				},
				"index": "anuQA",
				"typeName": "shape"
			},
			{
				"x": 933,
				"y": 742,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-pass-label",
				"type": "text",
				"parentId": "shape:ja-guide-system",
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
										"text": "合格"
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
				"meta": {},
				"id": "binding:ir-ongoing-user-start-en",
				"type": "arrow",
				"fromId": "shape:ir-ongoing-user-en",
				"toId": "shape:ir-ongoing-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
					"normalizedAnchor": {
						"x": 0.25,
						"y": 1
					},
					"snap": "none",
					"terminal": "start"
				},
				"typeName": "binding"
			},
			{
				"x": 80,
				"y": 1010,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-symptom-0-en",
				"type": "geo",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"w": 245,
					"h": 90,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 2,
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
								"content": [
									{
										"type": "text",
										"text": "Order and cause"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "are mixed"
									}
								]
							}
						]
					}
				},
				"index": "aJQ9f",
				"typeName": "shape"
			},
			{
				"x": 530,
				"y": 705,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-conditions",
				"type": "geo",
				"parentId": "shape:ja-guide-system",
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
										"text": "必須条件"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "意味・目的"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "可読性・編集の整合性"
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
				"x": 60,
				"y": 100,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-subtitle",
				"type": "text",
				"parentId": "shape:ja-guide-system",
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
										"text": "エージェントの実行に必要な知識を抽出し、根拠に基づいて改善する。"
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
				"x": 530,
				"y": 925,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-revise",
				"type": "geo",
				"parentId": "shape:ja-guide-system",
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
										"text": "構造を修正"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "既定値を調整"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "意味を維持"
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
				"meta": {},
				"id": "binding:ja-retry-end",
				"type": "arrow",
				"fromId": "shape:ja-retry",
				"toId": "shape:ja-candidate",
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
				"meta": {},
				"id": "binding:ir-normal-candidate-start-en",
				"type": "arrow",
				"fromId": "shape:ir-normal-candidate-en",
				"toId": "shape:ir-candidate-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"x": 60,
				"y": 1137.2163813286618,
				"rotation": 0,
				"isLocked": false,
				"opacity": 0.5,
				"meta": {},
				"id": "shape:ja-maintenance",
				"type": "geo",
				"parentId": "shape:ja-guide-system",
				"props": {
					"w": 1280,
					"h": 590.7836186713382,
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
				"x": 1140,
				"y": 1410,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-ask-ja",
				"type": "geo",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"w": 265,
					"h": 110,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 0,
					"url": "",
					"scale": 1,
					"flipX": false,
					"flipY": false,
					"color": "orange",
					"labelColor": "black",
					"fill": "solid",
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
										"text": "2回試しても手がかりなし"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "具体的に一つ聞き、"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "必要な回答を待つ"
									}
								]
							}
						]
					}
				},
				"index": "ae3Hf",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:ir-example-2-end-ja",
				"type": "arrow",
				"fromId": "shape:ir-example-2-ja",
				"toId": "shape:ir-measure-2-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"x": 950.26171875,
				"y": 364.08984375,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-cue",
				"type": "geo",
				"parentId": "shape:ja-guide-system",
				"props": {
					"w": 344.375,
					"h": 80,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 0,
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
										"text": "該当する手順に短い根拠を添える"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "判断に役立つ場合だけ"
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
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-start-recover-ja",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-ja",
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
						"x": 1130,
						"y": 710
					},
					"end": {
						"x": 1125,
						"y": 865
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
				"index": "aUyWyG",
				"typeName": "shape"
			},
			{
				"x": 490,
				"y": 1438,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-maint-compare",
				"type": "geo",
				"parentId": "shape:ja-guide-system",
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
										"text": "ガイドを比較"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "固定課題・条件を揃えた実行"
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
				"meta": {},
				"id": "binding:ja-maint-case-diagnose-end",
				"type": "arrow",
				"fromId": "shape:ja-maint-case-diagnose",
				"toId": "shape:ja-maint-diagnose",
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
				"x": 1140,
				"y": 1575,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-wait-note-en",
				"type": "text",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"color": "black",
					"size": "s",
					"w": 265,
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
										"text": "Resume only after the"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "needed answer is obtained."
									}
								]
							}
						]
					}
				},
				"index": "akzKs",
				"typeName": "shape"
			},
			{
				"x": 60,
				"y": 465,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-author-note",
				"type": "text",
				"parentId": "shape:ja-guide-system",
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
										"text": "一般理論は保守担当者向けの"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "文書に置く。"
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
				"meta": {},
				"id": "binding:ja-distill-start",
				"type": "arrow",
				"fromId": "shape:ja-distill",
				"toId": "shape:ja-knowledge",
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
				"id": "binding:ir-result-ask-start-ja",
				"type": "arrow",
				"fromId": "shape:ir-result-ask-ja",
				"toId": "shape:ir-inspect-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
					"normalizedAnchor": {
						"x": 0.75,
						"y": 1
					},
					"snap": "none",
					"terminal": "start"
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
				"id": "binding:ir-example-1-end-ja",
				"type": "arrow",
				"fromId": "shape:ir-example-1-ja",
				"toId": "shape:ir-measure-1-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"x": 50,
				"y": 30,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-title-ja",
				"type": "text",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"color": "black",
					"size": "l",
					"w": 1400,
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
										"text": "図の改善と、行き詰まりからの回復"
									}
								]
							}
						]
					}
				},
				"index": "a1Y1j",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:ir-start-recover-start-en",
				"type": "arrow",
				"fromId": "shape:ir-start-recover-en",
				"toId": "shape:ir-recover-trigger-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"x": 360,
				"y": 1470,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-maint-case-compare",
				"type": "arrow",
				"parentId": "shape:ja-guide-system",
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
				"meta": {},
				"id": "binding:ir-start-improve-end-ja",
				"type": "arrow",
				"fromId": "shape:ir-start-improve-ja",
				"toId": "shape:ir-improve-region-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"id": "binding:ir-example-0-end-ja",
				"type": "arrow",
				"fromId": "shape:ir-example-0-ja",
				"toId": "shape:ir-measure-0-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-test-hypothesis-ja",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-ja",
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
						"x": 1125,
						"y": 975
					},
					"end": {
						"x": 1125,
						"y": 1050
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
				"index": "aXzpMWV",
				"typeName": "shape"
			},
			{
				"x": 540,
				"y": 218.91371270584597,
				"rotation": 0,
				"isLocked": false,
				"opacity": 0.5,
				"meta": {},
				"id": "shape:skill",
				"type": "geo",
				"parentId": "shape:guide-system",
				"props": {
					"w": 800,
					"h": 291.10191229415403,
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
				"x": 732.1914714825828,
				"y": 618.0762237421297,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-apply-label",
				"type": "text",
				"parentId": "shape:ja-guide-system",
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
										"text": "ガイドを適用"
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
				"x": 845,
				"y": 1029,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-trial-ja",
				"type": "geo",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"w": 560,
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
										"text": "実際に小さく描く"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "核の3〜5要素・具体例1件・ラフ2案"
									}
								]
							}
						]
					}
				},
				"index": "aXzJu",
				"typeName": "shape"
			},
			{
				"x": 390,
				"y": 470,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-check-en",
				"type": "geo",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"w": 720,
					"h": 95,
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
										"text": "ASSESS THE PURPOSE AND CURRENT DIAGRAM"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Is there a supported measure or next hypothesis?"
									}
								]
							}
						]
					}
				},
				"index": "a6AUB",
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
					"h": 1779.2942613079692,
					"name": "From design knowledge to useful diagrams",
					"color": "black"
				},
				"parentId": "page:page",
				"index": "a1v7v",
				"typeName": "shape"
			},
			{
				"x": 470,
				"y": 1172,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-maintenance-subheading",
				"type": "text",
				"parentId": "shape:ja-guide-system",
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
										"text": "問いに応じて検証方法を選ぶ"
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
				"meta": {},
				"id": "binding:ir-test-hypothesis-start-en",
				"type": "arrow",
				"fromId": "shape:ir-test-hypothesis-en",
				"toId": "shape:ir-hypothesis-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"id": "binding:ir-return-improvement-start-en",
				"type": "arrow",
				"fromId": "shape:ir-return-improvement-en",
				"toId": "shape:ir-apply-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"id": "binding:ir-branch-recover-start-en",
				"type": "arrow",
				"fromId": "shape:ir-branch-recover-en",
				"toId": "shape:ir-check-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
					"normalizedAnchor": {
						"x": 0.75,
						"y": 1
					},
					"snap": "none",
					"terminal": "start"
				},
				"typeName": "binding"
			},
			{
				"x": 80,
				"y": 655,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-normal-start",
				"type": "text",
				"parentId": "shape:ja-guide-system",
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
										"text": "ユーザの依頼：目的・事実・閲覧条件"
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
				"meta": {
					"diagramId": "diagramming-guide-design-system",
					"language": "en"
				},
				"id": "page:page",
				"name": "Design system / English",
				"index": "a1",
				"typeName": "page"
			},
			{
				"meta": {},
				"id": "binding:ir-branch-improve-end-ja",
				"type": "arrow",
				"fromId": "shape:ir-branch-improve-ja",
				"toId": "shape:ir-improve-trigger-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"gridSize": 10,
				"name": "",
				"meta": {
					"multilingualDiagrams": {
						"diagramming-guide-design-system": {
							"schemaVersion": 1,
							"editingSourcePageId": "page:page",
							"languages": {
								"en": "page:page",
								"ja": "page:guide-design-system-ja"
							},
							"translations": {
								"ja": {
									"sourcePageId": "page:page",
									"sourceHash": "9b5d763725b5ea6052eaec68e22fd405c157abf61addc493b1734e025db9186b",
									"targetHash": "c3bedec5a6f531e237701419d39ddbed180550cba030acfbb12c04d82d48db21",
									"generatedAt": "2026-10-24T04:03:03.396Z",
									"status": "generated",
									"hashAlgorithm": "sha256-page-records-v1"
								}
							},
							"hashPolicy": {
								"records": "page descendant shapes and their bindings, sorted by id",
								"exclude": [
									"meta",
									"isLocked"
								],
								"serialization": "recursive sorted object keys; arrays preserve order"
							},
							"automation": "none; freshness must be checked explicitly",
							"layoutReview": {
								"reviewedAt": "2026-10-24T05:14:00.729Z",
								"classification": "layout-only",
								"editingSourcePageId": "page:page",
								"sourceOfLayoutPageId": "page:guide-design-system-ja",
								"pageHashes": {
									"en": "b2011c6d844f5b8787ab508cf446e472c338dcd28cd741875f455762ba173c25",
									"ja": "55a66b5f326974a269cb83a68d0446da645d5884597c448db362a96e0024d9c5"
								},
								"note": "Japanese layout adjustments applied to English; English text and all bindings preserved. Original translation baselines retained."
							}
						},
						"diagram-improvement-recovery": {
							"schemaVersion": 2,
							"editingSourcePageId": "page:improvement-recovery-en",
							"languages": {
								"en": "page:improvement-recovery-en",
								"ja": "page:improvement-recovery-ja"
							},
							"checkpoints": {
								"ja": {
									"algorithm": "page-content-v2",
									"sourcePageId": "page:improvement-recovery-en",
									"source": {
										"full": "008ce9d2a7f3eacbae1dfc0522670d99594d78f49bd9cb7b7e011b7874372895",
										"content": "e7deb9c6ef4f42fd4f4e796fda6a17e52a11be8c52a582535eb3fd666a9d014a",
										"legacy": "1fc1d4145e04d3a242770d0e43a220fe8086044c0a28310138f27d1df2e9be1d",
										"hasAssets": false
									},
									"target": {
										"full": "f9a7fa57c94b2d48e75bb04785d1c5700f43aa6eb5fbfd8127a2927e9d8b5304",
										"content": "b928fa3621929342a16b81234f2d9bc085ed1c70e4cb7711a7d4e301380e350f",
										"legacy": "e9993a4e76442d78d1409b981c0d41953de564e00ce349cf297ba1679014d91f",
										"hasAssets": false
									},
									"kind": "translation",
									"reason": "Reviewed clarified stall condition in both rendered languages: unresolved issue after two revisions without a useful new finding, or no supported next change. All user geometry, bindings, and other labels preserved.",
									"reviewedAt": "2026-10-25T12:09:18.729Z"
								}
							}
						}
					}
				},
				"id": "document:document",
				"typeName": "document"
			},
			{
				"meta": {},
				"id": "binding:ir-inspect-trial-end-en",
				"type": "arrow",
				"fromId": "shape:ir-inspect-trial-en",
				"toId": "shape:ir-inspect-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"x": 60,
				"y": 1137.2163813286618,
				"rotation": 0,
				"isLocked": false,
				"opacity": 0.5,
				"meta": {},
				"id": "shape:maintenance",
				"type": "geo",
				"parentId": "shape:guide-system",
				"props": {
					"w": 1280,
					"h": 590.7836186713382,
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
				"x": 870,
				"y": 1350,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-maint-diagnose-verdicts",
				"type": "arrow",
				"parentId": "shape:ja-guide-system",
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
				"x": 490,
				"y": 1438,
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
				"x": 950.26171875,
				"y": 364.08984375,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:cue",
				"type": "geo",
				"parentId": "shape:guide-system",
				"props": {
					"w": 344.375,
					"h": 80,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 0,
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
				"meta": {},
				"id": "binding:ir-loop-up-start-ja",
				"type": "arrow",
				"fromId": "shape:ir-loop-up-ja",
				"toId": "shape:ir-resume-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"y": 1368,
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
				"id": "binding:ja-feedback-start",
				"type": "arrow",
				"fromId": "shape:ja-feedback",
				"toId": "shape:ja-maint-decision",
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
				"x": 560.98828125,
				"y": 251.66015625,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-skill-label",
				"type": "text",
				"parentId": "shape:ja-guide-system",
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
										"text": "配布するSkill"
									}
								]
							}
						]
					}
				},
				"index": "a6uir",
				"typeName": "shape"
			},
			{
				"x": 60,
				"y": 40,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-title",
				"type": "text",
				"parentId": "shape:ja-guide-system",
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
										"text": "設計知識から、役立つ図へ"
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
				"meta": {},
				"id": "binding:ir-result-supported-end-en",
				"type": "arrow",
				"fromId": "shape:ir-result-supported-en",
				"toId": "shape:ir-supported-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"x": 845,
				"y": 1197,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-inspect-ja",
				"type": "geo",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"w": 560,
					"h": 130,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 22,
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
										"text": "描画結果を確認"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "仮説を支持・否定・判断できない"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "否定なら、仮説を変えて再試行"
									}
								]
							}
						]
					}
				},
				"index": "aYmqQ",
				"typeName": "shape"
			},
			{
				"x": 1145,
				"y": 745,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-initial-recovery-ja",
				"type": "text",
				"parentId": "shape:improvement-recovery-ja",
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
										"text": "初期設計の迷いも対象。"
									}
								]
							}
						]
					}
				},
				"index": "am2WA",
				"typeName": "shape"
			},
			{
				"x": 560,
				"y": 316.6290228659914,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-runtime",
				"type": "geo",
				"parentId": "shape:ja-guide-system",
				"props": {
					"w": 760,
					"h": 161.75378963400863,
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
										"text": "判断・既定値・例外"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "構造案 → 確認 → 仕上げ → 保存"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "ツール操作と保存に関する契約"
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
				"x": 725,
				"y": 855,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-fail",
				"type": "arrow",
				"parentId": "shape:ja-guide-system",
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
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-result-supported-ja",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-ja",
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
						"x": 985,
						"y": 1335
					},
					"end": {
						"x": 977,
						"y": 1410
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
				"index": "adwZZV",
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
				"meta": {},
				"id": "binding:ja-apply-end",
				"type": "arrow",
				"fromId": "shape:ja-apply",
				"toId": "shape:ja-conditions",
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
				"x": 810,
				"y": 780,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-recover-region-ja",
				"type": "geo",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"w": 640,
					"h": 780,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 0,
					"url": "",
					"scale": 1,
					"flipX": false,
					"flipY": false,
					"color": "violet",
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
				"index": "aUeKf",
				"typeName": "shape"
			},
			{
				"x": 810,
				"y": 300,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-deliver-en",
				"type": "geo",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"w": 640,
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
										"text": "AGENT OBSERVATION"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "A concrete issue, improvement opportunity, or stall"
									}
								]
							}
						]
					}
				},
				"index": "a8LzW",
				"typeName": "shape"
			},
			{
				"x": 732.1914714825828,
				"y": 618.0762237421297,
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
				"id": "binding:ir-ongoing-user-end-en",
				"type": "arrow",
				"fromId": "shape:ir-ongoing-user-en",
				"toId": "shape:ir-candidate-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-ongoing-agent-ja",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-ja",
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
						"x": 930,
						"y": 245
					},
					"end": {
						"x": 1130,
						"y": 300
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
				"index": "anvm0E",
				"typeName": "shape"
			},
			{
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-ongoing-user-ja",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-ja",
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
						"x": 570,
						"y": 245
					},
					"end": {
						"x": 370,
						"y": 300
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
				"index": "anyJzZ",
				"typeName": "shape"
			},
			{
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-normal-refine-ja",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-ja",
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
						"x": 1130,
						"y": 410
					},
					"end": {
						"x": 930,
						"y": 470
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
				"index": "aBkUq",
				"typeName": "shape"
			},
			{
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-normal-candidate-ja",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-ja",
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
						"x": 370,
						"y": 410
					},
					"end": {
						"x": 570,
						"y": 470
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
				"index": "a6k3pV",
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
				"id": "binding:ja-retry-start",
				"type": "arrow",
				"fromId": "shape:ja-retry",
				"toId": "shape:ja-revise",
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
				"x": 80,
				"y": 865,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-match-en",
				"type": "geo",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"w": 580,
					"h": 105,
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
										"text": "Observed symptom → measure → benefit"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Ask intuitive choices if needed"
									}
								]
							}
						]
					}
				},
				"index": "aIdaQ",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:ir-normal-candidate-end-en",
				"type": "arrow",
				"fromId": "shape:ir-normal-candidate-en",
				"toId": "shape:ir-check-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
					"normalizedAnchor": {
						"x": 0.25,
						"y": 0
					},
					"snap": "none",
					"terminal": "end"
				},
				"typeName": "binding"
			},
			{
				"x": 845,
				"y": 865,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-hypothesis-ja",
				"type": "geo",
				"parentId": "shape:improvement-recovery-ja",
				"props": {
					"w": 560,
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
										"text": "不明点と仮説を一つに絞る"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "何が分かれば次を決められるか定める"
									}
								]
							}
						]
					}
				},
				"index": "aWL6A",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:ja-maint-case-diagnose-start",
				"type": "arrow",
				"fromId": "shape:ja-maint-case-diagnose",
				"toId": "shape:ja-maint-case",
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
				"meta": {},
				"id": "binding:ir-ongoing-agent-start-en",
				"type": "arrow",
				"fromId": "shape:ir-ongoing-agent-en",
				"toId": "shape:ir-ongoing-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
					"normalizedAnchor": {
						"x": 0.75,
						"y": 1
					},
					"snap": "none",
					"terminal": "start"
				},
				"typeName": "binding"
			},
			{
				"meta": {},
				"id": "binding:ir-normal-refine-start-en",
				"type": "arrow",
				"fromId": "shape:ir-normal-refine-en",
				"toId": "shape:ir-deliver-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"id": "shape:ja-guide-system",
				"type": "frame",
				"props": {
					"w": 1440,
					"h": 1779.2942613079692,
					"name": "diagramming-guide-design-system.ja",
					"color": "black"
				},
				"parentId": "page:guide-design-system-ja",
				"index": "a1v7v",
				"typeName": "shape"
			},
			{
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-return-recovery-ja",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-ja",
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
						"x": 977,
						"y": 1520
					},
					"end": {
						"x": 977,
						"y": 1660
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
				"index": "ajURa",
				"typeName": "shape"
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
				"x": 80,
				"y": 1160,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-maintenance-label",
				"type": "text",
				"parentId": "shape:ja-guide-system",
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
										"text": "ガイドの保守"
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
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-loop-up-en",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"kind": "elbow",
					"elbowMidPoint": 0.5,
					"dash": "solid",
					"size": "m",
					"fill": "none",
					"color": "green",
					"labelColor": "black",
					"bend": 0,
					"start": {
						"x": 1450,
						"y": 1725
					},
					"end": {
						"x": 1110,
						"y": 200
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
				"index": "apFl6",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:ir-start-recover-end-en",
				"type": "arrow",
				"fromId": "shape:ir-start-recover-en",
				"toId": "shape:ir-recover-region-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"x": 50,
				"y": 300,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-candidate-en",
				"type": "geo",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"w": 640,
					"h": 110,
					"geo": "rectangle",
					"dash": "draw",
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
										"text": "USER FEEDBACK"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "“Hard to understand” / “Make it clearer”"
									}
								]
							}
						]
					}
				},
				"index": "a5TGf",
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
				"x": 75,
				"y": 800,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-improve-title-en",
				"type": "text",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"color": "green",
					"size": "m",
					"w": 590,
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
										"text": "IMPROVEMENT: choose a concrete measure"
									}
								]
							}
						]
					}
				},
				"index": "aHyJ2",
				"typeName": "shape"
			},
			{
				"x": 272.38484174786504,
				"y": 1660,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-resume-en",
				"type": "geo",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"w": 944.9706844022611,
					"h": 130,
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
										"text": "GAIN A SUPPORTED NEXT STEP"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "Revise, check, refine, and save within scope. Retire unused drafts when appropriate."
									}
								]
							}
						]
					}
				},
				"index": "ahLIf",
				"typeName": "shape"
			},
			{
				"x": 50,
				"y": 630,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-improve-trigger-en",
				"type": "geo",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"w": 640,
					"h": 110,
					"geo": "rectangle",
					"dash": "draw",
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
										"text": "A concrete measure can be linked"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "to an observed symptom and reading benefit"
									}
								]
							}
						]
					}
				},
				"index": "aCJPX",
				"typeName": "shape"
			},
			{
				"meta": {},
				"id": "binding:ir-return-recovery-start-en",
				"type": "arrow",
				"fromId": "shape:ir-return-recovery-en",
				"toId": "shape:ir-supported-en",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"id": "shape:ir-branch-improve-en",
				"type": "arrow",
				"parentId": "shape:improvement-recovery-en",
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
						"x": 570,
						"y": 565
					},
					"end": {
						"x": 370,
						"y": 630
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
				"index": "aCiqH",
				"typeName": "shape"
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
				"meta": {},
				"id": "binding:ir-result-ask-end-ja",
				"type": "arrow",
				"fromId": "shape:ir-result-ask-ja",
				"toId": "shape:ir-ask-ja",
				"props": {
					"isPrecise": true,
					"isExact": true,
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
				"x": 1320,
				"y": 1661,
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
				"x": 375,
				"y": 1240,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-measure-2-en",
				"type": "geo",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"w": 285,
					"h": 90,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 2,
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
								"content": [
									{
										"type": "text",
										"text": "Linked overview"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "and detail"
									}
								]
							}
						]
					}
				},
				"index": "aQWrj",
				"typeName": "shape"
			},
			{
				"x": 560,
				"y": 316.6290228659914,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:runtime",
				"type": "geo",
				"parentId": "shape:guide-system",
				"props": {
					"w": 760,
					"h": 161.75378963400863,
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
				"x": 80,
				"y": 1368,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ja-maint-case",
				"type": "geo",
				"parentId": "shape:ja-guide-system",
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
										"text": "事例の選定"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "検証する問いを選ぶ"
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
				"x": 560.98828125,
				"y": 251.66015625,
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
			},
			{
				"x": 0,
				"y": 0,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:improvement-recovery-ja",
				"type": "frame",
				"parentId": "page:improvement-recovery-ja",
				"props": {
					"w": 1600,
					"h": 1860,
					"name": "improvement-and-recovery.ja",
					"color": "black"
				},
				"index": "a1USe",
				"typeName": "shape"
			},
			{
				"x": 375,
				"y": 1125,
				"rotation": 0,
				"isLocked": false,
				"opacity": 1,
				"meta": {},
				"id": "shape:ir-measure-1-en",
				"type": "geo",
				"parentId": "shape:improvement-recovery-en",
				"props": {
					"w": 285,
					"h": 90,
					"geo": "rectangle",
					"dash": "draw",
					"growY": 2,
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
								"content": [
									{
										"type": "text",
										"text": "A few recognizable"
									}
								]
							},
							{
								"type": "paragraph",
								"content": [
									{
										"type": "text",
										"text": "icons with labels"
									}
								]
							}
						]
					}
				},
				"index": "aNvmA",
				"typeName": "shape"
			},
			{
				"meta": {
					"diagramId": "diagram-improvement-recovery",
					"language": "en"
				},
				"id": "page:improvement-recovery-en",
				"name": "Improvement and recovery / English",
				"index": "a3igX",
				"typeName": "page"
			}
		]
	}
}
!!!_END_OF_TLDRAW_DATA__DO_NOT_CHANGE_THIS_PHRASE_!!!
```