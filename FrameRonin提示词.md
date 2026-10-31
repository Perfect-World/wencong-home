# FrameRonin 提示词抓取结果

来源：`https://frameronin.com` 前端产物
- 主包 `assets/index-DWbk6816.js`（1.8 MB）
- 71 个懒加载 chunk（`assets/*.js`）
- 预设工作流 `https://frameronin.com/bpset/*.json`

抓取方式：下载全部 JS → 转义感知的字符串扫描 → 按 CJK 密度与提示词特征词过滤。

> 重要结论先说：**"专业模板"的提示词抓不到**，见文末「抓不到的部分」。
> 抓到的是**自由生图 / 场景生成 / 自由序列动作迁移**这条链路的提示词，足够自己搭一套。

---

## 一、自由生图（文生图 / 图生图）

命中文件：`assets/HomeFreeImageGenerator-BgBnSMQ1.js`

### 1.1 三视图角色设定图（角色设计稿）

> 变量：`{{content}}` = 用户填写的角色描述

```
三视图角色设定图，正面、侧面、背面同画面横向排布，full body character turnaround sheet，保持同一角色在三个视角下的脸型、发型、服装、配色、体型与细节完全一致，日式JRPG角色立绘风格，偏2000年代日系游戏官方设定稿风格，干净细致的黑色线稿，清晰准确的轮廓线，传统赛璐璐上色，平涂色块，少量硬边阴影，非厚涂，非写实，头身比约7到7.5头身，小头、窄肩、细腰、长腿，人物从头到脚完整显示，站姿自然中立，正视图双臂自然下垂，侧视图为标准纯侧面，背视图完整展示背部造型，无透视畸变，无夸张动态，无复杂背景，纯白背景，设定图排版清晰，三视图大小一致、对齐整齐，适合作为角色设计参考，避免Q版、避免3D渲染、避免写实皮肤、避免厚涂光影、避免复杂背景、避免镜头透视、避免多余道具遮挡，角色描述：{{content}}
```

### 1.2 像素风渲染补丁（附加到提示词尾部）

```
handcrafted pixel art rendering, crisp hard-edged pixels, consistent pixel density, no anti-aliasing
```

### 1.3 图生图 / 局部重绘的硬约束片段

```
Keep every pixel outside the selected hole unchanged, including any pre-existing transparent background. Blend the new content seamlessly with the surrounding image. Do not leave the selected hole empty or draw a checkerboard pattern.
```

```
Keep every pixel outside the red outline unchanged. Remove the red outline from the final result.
```

```
Preserve the original canvas size, composition, transparency, pixel-art style, lighting, palette, and edge continuity. Return only the final full image.
```

```
Study their art direction, pixel density, brushwork, line quality, palette, lighting, texture, camera feel, and level of detail.
```

### 1.4 游戏道具 / UI 素材

```
Production-ready game inventory sprites, isolated objects, sharp silhouettes, highly detailed.
```

> 站点内置示例（可直接当模板）：

```
一套森林冒险游戏界面，包含背包面板、技能栏和按钮。
统一使用木质边框与藤蔓装饰，正面展示。
```

```
一组森林冒险道具，包含木弓、箭袋、皮靴、药水和地图。
统一使用藤蔓与树叶装饰，每个道具完整展示。
```

### 1.5 "非像素风"改写逻辑（`Ate()` 函数，值得抄）

站点允许把像素模板改写成卡通 / 写实风，做法是在提示词**前后各加一段总纲**，并且：

- 把 `pixel-art style` / `pixel art finish` 等英文替换成 `cartoon style` / `photorealistic style`
- 把中文 `像素风格` / `像素画风` / `像素风` 替换成 `卡通` / `写实`
- 头部追加：`风格优先要求：整张图必须使用<风格>风格。不要像素风，不要像素块、点阵或低分辨率游戏质感。模板仅参考布局、动作、朝向、比例与间距，不继承模板画风。`
- 尾部追加：`最终再次确认：只生成<风格>风格，禁止像素风。`

**持有物开关**（`hasItems`）：

- 关闭 → 删掉 `The character must have empty hands and must not hold any weapons, tools, props, shields, or handheld items.` / `角色双手保持空手，不拿任何物品。`
- 开启 → 头部追加：
  `持有物要求：角色必须持有武器或物品，不要空手。优先按用户描述和角色参考图确定武器或物品；未指定时选择符合角色设定的武器或物品。清楚画出持有物与正确握持关系，所有动作和方向保持同一持有物的外观、配色与比例一致，不得遗漏或删除。`
  尾部追加：`最终再次确认：角色有武器或物品，必须保留并清楚呈现，不要生成空手角色。`

---

## 二、场景生成

命中位置：`assets/index-DWbk6816.js` @240680 附近

### 2.1 TopDown 正视角全景

```
你是一名资深的像素场景画师，你将根据用户描述的场景生成一个topdown类型的俯视正视角的全景像素风场景，建筑全部是正朝向的，不出现人物。你将为我生成：
```

### 2.2 TopDown 45 度视角全景

```
你是一名资深的像素场景画师，你将根据用户描述的场景生成一个topdown类型的俯视45视角的全景像素风场景，不出现人物，山体，天空。建筑朝向都是45度的。你将为我生成：
```

### 2.3 2D 横版街机场景

```
你是一名资深的像素横版街机场景画师。你将根据用户描述，生成一张 2D 横版侧视（Side-scrolling Arcade perspective） 的全景像素场景，风格参考经典动作/格斗街机游戏。

画面规范：

视角： 严格的 2D 侧视视角，展现一个流动的、具有电影感的动作关卡。

构图： 强调水平方向的推进感（Level Flow）。场景必须包含多个视差层（Parallax Layers），以模拟深度：

远景（Far Background）： 遥远的地标（如城市天际线、山脉、巨大的月亮），细节简化。

中景（Midground）： 主要的可通行区域（如街道、平台、工厂内部），细节丰富，包含障碍物。

前景（Foreground）： 快速掠过的景物（如电线杆、栏杆、破碎的车辆），用于增强速度感和深度。

所有的建筑都是正朝镜头。

风格细节：

色彩与光影： 色彩鲜明、饱和度高，具有强烈的戏剧性或环境光效（如霓虹灯、爆炸后的余晖、激光）。光影更强调氛围而非写实。

细节丰富： 场景充满生活气息或破坏痕迹，例如：涂鸦墙、垃圾桶、霓虹招牌、蒸汽管道、破损的机械。

禁忌： 不出现任何玩家人物、UI 界面或文字。

你将为我生成：
```

### 2.4 地图拼接补全 · 斜视角大地图

命中文件：`assets/MapStitch-BlTuxe4o.js`

```
您是一名非常专业的场景画师，擅长绘画isolate场景大地图。 用户会上传一张只有边缘有内容的图片，你将参考图片边缘的内容，补全图中所有透明像素的范围内的图像。整个补全区域保持高分辨率细节和清晰的聚焦，与原图风格统一但更加锐利。 同时您也将结合用户的需求进行补全。 图片无透视感，图片保持高分辨率细节 (high-resolution details), 纹理清晰 (clear textures), 锐利轮廓 (sharp outlines), 细节丰富 (intricate details), 清晰聚焦 (sharp focus)，所有建筑和构筑物都正朝镜头。场景中没有人物、烟雾，看不到远景和天空，不要出现正朝镜头的建筑和构筑物，画面不会因为远景有色差和模糊，自然过渡不同地形
```

### 2.5 地图拼接补全 · 正交前视横版（反透视写得最狠的一段，值得单独收藏）

```
您是一名非常专业的场景画师，擅长绘画横板游戏的正交前视场景大地图。用户会上传一张只有边缘有内容的图片，请参考边缘内容，补全图中所有透明像素区域，并结合用户需求进行绘画。保持原图的风格、比例、色彩、光照和边缘连续性，地形自然衔接。画面必须完全没有任何透视，视角类似严格的正交前视图（front elevation / orthographic front view），镜头水平正对场景。所有建筑、构筑物和地形都正朝前、正对镜头，只能看到正面，绝对看不到任何侧面或顶面。禁止斜视、俯视、仰视、45°等距视角和三分之四视角；禁止消失点、近大远小、透视缩短以及向画面深处收缩或汇聚的线条。所有正面保持与画面平面平行，地形以正面轮廓自然衔接，不展示向纵深延伸的地面。保持高分辨率细节 (high-resolution details)、清晰纹理 (clear textures)、锐利轮廓 (sharp outlines)、丰富细节 (intricate details) 和清晰聚焦 (sharp focus)。场景中没有人物、文字、烟雾，不要因距离产生模糊或色差。只返回与输入画布尺寸相同的完整场景图片。
```

---

## 三、序列帧 / 动作迁移（自由序列）

命中文件：`assets/PixelCreationPage-BUPlG_L3.js`

这是**参考图（角色外观）+ 动作 GIF（动作）→ 逐帧 PNG** 的核心提示词，三语版本都在。

### 3.1 中文版

```
## 主体定义
<主体 1>：参考图 < 图片 1 > 目标角色。严格锁定角色为XXXXX
< 图片 1 > 仅作为角色外观身份参考，不作为目标gif首帧。
<gif 1>：原始gif，**仅取前 {frames} 帧作为动作、姿态、手脚运动、身体转向、动作节奏、停顿、镜头运动、切镜、变焦、构图透视的唯一主参考，禁止改动动作**。
摘要：[动作迁移 + 参考生成] 目标gif基于 < gif 1 > 前{frames}帧做动作迁移，将原gif人物替换为 < 主体 1>，**100% 复刻原gif全部动作、运镜，禁止新增、删减、提前、延迟任何肢体动作。**

只生成一个角色，全身完整可见，角色大小稳定，镜头固定，全程保持角色设计一致。使用纯色背景，颜色以界面设置为准。不添加文字、水印、分镜面板、网格、镜头切换或额外角色。生成连贯的逐帧角色动作，不直接绘制拼图；画面背景颜色为{backgroundColor}，背景保持纯净统一，不要出现复杂场景。
```

### 3.2 英文版

```
Use the character in the reference image as the sole appearance reference. Preserve its identity, silhouette, body proportions, face, hairstyle, costume, equipment, palette and pixel-art style. The image defines appearance, not a fixed pose.

Replace the original character in the motion GIF with this character. Follow the GIF's action order, facing direction, body poses, limb movements and weapon trajectory, preserving the motion rhythm and transitions as closely as possible. Do not hold the image's pose or copy the original GIF character's appearance.

Generate one character, fully visible, at a stable scale with a fixed camera. Keep the character design consistent throughout. Use a plain background in the color selected in the interface. Do not add text, watermarks, panels, grids, scene cuts or additional characters. Generate continuous individual animation frames, not a sprite sheet; the frames will be assembled afterwards.
```

### 3.3 日文版

```
参照画像のキャラクターだけを外観の基準とし、特徴、輪郭、体の比率、顔、髪型、服装、装備、配色、ピクセル画風を維持してください。画像は外観の参考であり、固定ポーズの指定ではありません。

動作 GIF の元のキャラクターを参照画像のキャラクターに置き換えてください。GIF の動作順序、向き、姿勢、手足の動き、武器の軌道に従い、動作のリズムとつながりをできるだけ維持してください。画像のポーズで静止したり、GIF の元のキャラクターの外観をコピーしたりしないでください。

キャラクターは1人だけとし、全身を表示し、大きさとカメラを固定してください。外観を全フレームで統一し、背景は画面設定で選択した単色にしてください。文字、透かし、コマ枠、グリッド、場面切り替え、追加キャラクターは不要です。連続する個別のアニメーションフレームを生成してください。スプライトシートは後から自動で組み立てます。
```

### 3.4 自由序列 · 用户侧写法建议（站点帮助原文）

```
例如：保持角色外观和像素风格一致，角色原地挥剑，固定镜头，角色居中……
```

> 帮助文档还强调：**动作不明显时把提示词写成清楚的起手、过程、收尾，避免同时提出互相冲突的动作要求。**

---

## 四、旁支：FanAIWorld NPC 决策提示词

命中文件：`assets/FanAIWorldPlaceholder-D70DeBhx.js`

```
你是浏览器 MMO 中的 NPC 决策模块。只能从 legalActionMenu 中选恰好一项，不得编造动作、目标、坐标或 ID。只输出 JSON，键：actionType、optionId、targetId、reason、innerMonologue、ambientLine（可选：一句角色口吻的短台词，不讲话则空字符串）。不要 markdown。字段 reason、innerMonologue、ambientLine 必须使用**简体中文**，简短具体。
```

---

## 五、抓不到的部分（重要）

### 5.1 专业模板走服务端，前端拿不到

代码里这个判断是关键：

```js
function Gm(e, t) {
  const n = e.protectedTemplateId?.trim() ?? "";
  return !n
    ? { allowed: t !== "vip", generationApiMode: t, usesProtectedBackend: false }
    : { allowed: (e.allowedApiModes ?? Ioe[n] ?? Toe).includes(t), generationApiMode: "vip", usesProtectedBackend: true };
}
```

命中 `protectedTemplateId` 的模板（`one-image-all-actions-pro`、`one-image-battle-8dir` 等），前端只发 `templateId` + 用户描述，**真正的模板提示词由服务端注入**，请求体里根本没有提示词。这类抓不到。

### 5.2 一部分模板干脆是 Gemini Gem

`assets/GemPixelPotpourriHub` 与首页的「RPGMaker角色生成」「nanobanana预设像素角色生成器V2.3OT」，指向的是 `gemini.google.com/gem/...`。
Gem 的 system prompt 不公开，抓不到。

### 5.3 完整模板清单（供对照，均属上面两类）

| id | 名称 |
|---|---|
| character-v2 / v2-2 / v3 | 常规角色 V2 / V2.2 / V3 |
| character-v2-3ot | V2.3OT |
| horizontal-character / horizontal-swordsman | 横版人物 / 横版剑士 |
| horse-riding / rpg-horse-qianmo | 骑马动作 |
| one-image-all-actions / -2 | 一图全动作 / 全人物类 |
| ronin-v4x3 | 连生动作 V4Tx3 |
| topdown-8dir | 八方向 TopDown 角色生成 |
| rpgmaker-v1 / v1-1 / v3a / v3b / xp / vx / rpg-n | RPGMaker 系列 |
| bird-monster / chicken / zombie-b1 / zombie-b2 | 鸟怪 / 只因 / 僵尸 |
| tunshi-tiandi-s | 吞食天地（S） |
| scene-front-view / scene-45-view / scene-arcade | 正视角 / 45度 / 街机场景 |
| v23ot-256-connected-matte | 2.3ot 一键处理 |

### 5.4 顺带发现的：站点自己就发布了一个 Skill

`assets/CodexSkillPage-Do6mOSLe.js` 显示 FrameRonin 官方提供了两个智能体技能包：

- Codex 版：`$frameronin ...`（示例指令在 chunk 里，共 10 条）
- DeepSeek Harness 桌面端版：`/frameronin-deepseek ...`

主题是「让智能体调用本站工具生成像素角色 / 四八方向动作 / 序列图与 GIF」。也就是说 —— 这个站本身已经把你想做的事做了一遍。

另外，接口层还留着一条自有生图网关：

- 直连：`/v1/draw/nano-banana`、`/v1/draw/result`
- 自有：`/api/generate`、`/v1/api/generate`、`/v1/api/result`
- 任务：`/jobs`
- 兼容层：`openai-compatible` / `openrouter` / `linapi`（Gemini generateContent）/ `yunwu`（fal.ai queue）

也就是说它支持 **自带 Key（BYOK）** 直连 nano-banana / Gemini 出图 —— 我们自己的 Skill 可以复用同一条路。

---

## 六、做成我们自己的 Skill 的三条路

1. **BYOK 直连**：用上面的提示词 + 用户自己的 nano-banana / Gemini Key，走 `openai-compatible` 或 `generateContent`。最接近原站效果，但用户要自备 Key 且按量付费。
2. **本地生图工具**：把提示词固化进 Skill，调用本地/内置的文生图能力出图。零成本、离线可跑，但像素精度和「动作迁移」能力弱于 nano-banana。
3. **只做提示词库**：Skill 只负责把用户需求 → 结构化提示词（三视图 / 场景 / 动作），出图交给任意工具。最轻，最稳。

推荐 **3 + 2**：先把提示词模板固化成 Skill，出图用本地工具兜底；需要高质量动作迁移时再切 1。
