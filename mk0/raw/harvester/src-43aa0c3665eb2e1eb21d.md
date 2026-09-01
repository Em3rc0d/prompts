# AIASE 2026 W3 — From Agentic Product to Agentic Engineering

> 莊坤達 Kun-Ta Chuang｜成功大學資訊工程學系

---

## 0. 課程公告

- **HW1 截止**：3/13 23:59（GitHub: `ktchuang/TAICA_AIASE2026`）
- **HW2 公布**：本週課堂公告
- **3/18 特別講座**：AI 驅動的雲端應用部署與架構流程（AWS）
  - 講者：徐任弘 Jack Hsu（AWS 資深合作夥伴解決方案架構師）
  - 講者：莊昆霖 Denny Jhuang（idbean 艾即思科技 Solutions Architect）
  - 議題：Kiro 環境介紹與 Demo、AI 驅動的瀏覽器自動化、AWS 服務架構解析

---

## 1. AI 時代的職場衝擊

### 1.1 AI 盛世引發 2028 全球智識危機？
> 來源：Citrini Research, *The 2028 Global Intelligence Crisis*（2026/02/23）

- **AI 牛市的反面**：生產力暴漲但利得集中，形成「幽靈 GDP」
- **SaaS 護城河崩解**：Agentic coding 讓 AI 快速複製中端 SaaS 核心功能
- **摩擦經濟歸零**：AI Agent 消除人類惰性與資訊不對稱的利潤
- **白領失業螺旋**：AI 提升 → 裁員 → 消費下降 → 再裁員，無自然觸底機制
- **歷史反轉效應失效**：過去技術革命創造新工作，但 AI 能勝任人類想轉進的新職位
- **私募信貸骨牌**：大量押注 SaaS 收入永續成長，AI 可能瓦解其核心價值
- **$13 兆房貸的存在性危機**：AI 結構性破壞白領收入長期穩定性
- **政策困境**：傳統財政與貨幣政策無法解決 AI 造成的結構性失業
- **智識溢價的終結**：人類智識不再是稀缺資源

### 1.2 AI Impact @ 2026
> 來源：Anthropic, *Labor market impacts of AI: A new measure and early evidence*

- AI 技術上限高，但實際落差仍在「結構過渡期」
- 10 大職業被 AI 接手工作內容比例（前三名）：
  1. 電腦程式設計師 74.5%
  2. 客戶服務代表 70.1%
  3. 資料輸入員 67.1%

### 1.3 AI 時代的職場衝擊與應變之道
> 來源：簡立峰老師訪談｜丁菱娟《邊走邊想》ep9

#### 資工系學生面臨最高風險
- 麥肯錫研究：工作能力分為虛擬工作、實體工作、人際 EQ
- **殘酷結論**：電腦工程師的工作幾乎 100% 在虛擬環境，是最容易被 AI 取代的職業之一
- 你每天產生的程式碼、commit 記錄，正是訓練 AI 最豐富的養分

#### 為什麼 AI 特別能取代資工人？
- AI 讀完了幾乎所有技術文獻、Stack Overflow、GitHub Repo
- 演算法、資料結構等基礎教材 AI 早已全部吸收
- 企業已開始「減少徵才」：微軟裁員後補進的是 8 年以上資深工程師，大幅減少 entry-level 職缺

#### 職場即將發生什麼？
- **外包工作大幅減少**：哈佛商業評論調查顯示美國外包工作已平均減少 30%
- **「影子 AI」現象**：MIT 統計 95% 企業導入 AI 初期不順利，但 90% 員工其實早就在偷偷自己用
  - 偷偷用 AI → 讓自己更高效，悄悄拉開差距
  - 不用 AI → 被高效的同事比下去，逐漸邊緣化

### 1.4「2026 年，將是企業 AI 的清算年」
> 來源：簡立峰，《經理人》

- **現象**：大量投入課程培訓、工具、黑客松，但組織整體競爭力未見增強
- **致命盲點**：賦能個人 ≠ 強化組織
- **正確做法**：把 AI 用在核心競爭力上

| 產業核心能力 | AI 的正確切入點 |
|---|---|
| 化工業配方研發 | 讓 AI 閱讀學術論文、找出新組合 |
| 電商導購、訂價 | AI 優化推薦與定價策略 |
| 金融業風控、反詐騙 | AI 強化異常偵測能力 |

- **關鍵**：找「影子 AI」使用者、給予真實業務問題、改變激勵機制
- > 「99% 的人會害怕，不敢過去。我們現在需要的是探險家精神。」— 簡立峰

### 1.5 資工系學生的三個致命陷阱

1. **陷阱一：以為懂 AI 就沒問題**
   - 懂得設計 AI 和懂得善用 AI 是完全不同的能力
   - AI 就像牙膏——你擠的力道好，牙膏的形狀才好

2. **陷阱二：把 AI 當 Google 用**
   - 99% 的人用 AI 的方式是「一問一答」，只是在抄捷徑
   - 公式：一問一答 = 抄襲；十問十答 = 學習；**百問百答 = 創造**

3. **陷阱三：大腦外包**
   - AI 越方便，思考肌肉就越萎縮
   - 哈佛研究：當 AI 幫你完成工作，你本應透過協作建立的信任與人際網絡機會也一起消失

### 1.6 應變策略

#### 從「虛擬技能」走向「EQ＋實體判斷」
- **系統性溝通與說服力**：把技術翻譯成老闆、客戶聽得懂的語言
- **跨團隊協作與談判**：在模糊需求中找到共識
- **現場判斷與應變**：AI 感受不到商業邏輯與組織政治

#### 練習「提問能力」
- **技巧 A**：請 AI 教你怎麼問問題
- **技巧 B**：問完之後加「我還需要提供什麼樣的背景資訊，你才能給我更好的答案？」
- **技巧 C**：先定義角色（用角色框架描述問題）

#### 考慮「AI 原生創業」
- OECD 預測：2025 年全球將新增 200 萬～300 萬家「一人公司」
- 資工背景的三大天然優勢：懂技術 stack、懂 API、懂自動化
- **AI 原生創業思維**：從 Day One 就以「我一個人 ＋ AI 同事」的架構思考

#### 不同族群的優勢與劣勢

| 族群 | 優勢 | 劣勢 |
|---|---|---|
| 資深工程師（10 年以上） | 有專業判斷力，能鑑別 AI 輸出品質 | 容易低估 AI |
| 資工系學生（你） | 正在成為 AI 原生世代，適應力最強 | 基礎技能被 AI 完全覆蓋，初期就業弱勢 |
| 中生代工程師（5~10 年） | 有一定實戰經驗作為緩衝 | 職涯壓力最大，焦慮感最高 |

- **你的真正優勢**：你還沒有需要捍衛的「舊有做法」，可以從第一天就以 AI 原生的思維建立工作習慣

### 1.7 能動性（Agency）決定你的未來

- **核心論點**：未來十年最重要的技能不是寫程式或提示詞工程，而是能動性（Agency）
- **殘酷現狀**：約 80% 的人都在「從眾」，在別人訂好的規則裡打轉

#### 能動性的三大特徵
1. **主動出擊**：不等別人許可，就直接開始行動
2. **視為實驗**：把人生當作實驗，失敗是寶貴的實驗數據
3. **迎難而上**：困難是通往價值的門，而不是擋路的牆

#### AI 時代的競爭邏輯
- 專才 → 被商品化（單一技能過剩，容易被 AI 替代）
- **通才 → 掌握未來**（學習能力更快、收入更高、抗風險能力更強）

### 1.8 AI 能力曲線 vs. 擴散曲線
> 來源：Anthropic CEO Dario Amodei

- **2026–2027**：能力曲線觸頂（AGI 級別能力達成）
- **2027–2030**：擴散曲線瘋狂追趕（真正產生「兆元級營收」的時刻）
- **未來的贏家** = 能最快把「神級智商」塞進「平庸現實」的人

#### 三道無法繞過的「現實之牆」
1. **技術的最後一哩路**：AI 不認識你的系統（老舊伺服器、奇特權限設定）
2. **企業的慣性之牆**：AI 遇上官僚主義（法務、合規、資安層層審批）
3. **物理世界的終極束縛**：位元快，原子慢（動物實驗、人體臨床、FDA 批准，一步都省不了）

> 這中間的落差 ＝ 我們這代人**最大的機會**，也是最大的**焦慮來源**

### 1.9 具體行動建議

#### 五個具體行動
1. **實際深度使用 AI 工具**：帶著真實問題去問，練習提問技巧 A、B、C
2. **練習「百問百答」深度挖掘**：用深度互動的方式研究，而不是一問一答地抄捷徑
3. **用 Deep Research 功能研究技術主題**：讓 AI 幫你蒐集文獻，然後由你主導判讀與驗證
4. **盤點你的不可替代性**：哪些技能是 AI 無法取代的——溝通、現場判斷、人際信任？
5. **構想「一人公司」雛形**：用創業者的眼光看自己的技能

#### 訓練能動性的 5 步回圈框架
1. 找個方向開始
2. 研究別人的路
3. 大膽嘗試與試錯
4. 識別模式與底層邏輯
5. 將方法教給別人

#### 三大行動原則
- **停止盲目追逐新工具**：停下來思考長遠方向
- **把 AI 當作放大器，守住判斷力**：AI 是生產工具，但不是你的大腦
- **立志成為「通才」**：什麼都能做一點，就不怕任何一條路斷掉

---

## 2. 為什麼需要學習 Agentic Engineering？

### 2.1 當 AI 無所不能，我們剩下什麼？
> 來源：中研院院士孔祥重，《經理人》

人類真正的價值在於兩項 AI 至今難以掌握的能力：

1. **系統設計（System Design）**：構成一個穩定可靠的「系統」，需要全局視角與前瞻規劃
2. **定義問題（Defining Problems）**：將模糊目標拆解為具體可測量的指標，將混亂轉化為 AI 可執行的清晰路徑

#### AI 時代軟體開發鐵三角
- **FDE/PM（Navigator）**：市場洞察、策略規劃、價值驗證、敏捷迭代
- **Agent Architect（Human Guardian）**：系統架構設計、資安防護、代碼品質審查、邏輯驗證
- **AI Agents（Drivers）**：自動化編碼、快速原型開發、測試與除錯、CI/CD

### 2.2 Agentic Engineering
> 來源：Andrej Karpathy，X 發文（2026/01）

- 編碼工作流程已從 **80% 手動** 轉為 **80% AI Agent 協助**
- 只需英文描述目標，AI 即自主規劃、寫碼、測試及修正
- **Agentic Engineering** 強調：需人類高階指導、判斷與監督，而非完全自動化

#### The Karpathy Shift：編碼三個時代

| 時代 | 年份 | 模式 | 開發者角色 | 代表工具 |
|---|---|---|---|---|
| Manual Coding Era | 2023–2024 | 80% 手動編碼 | Writer | GitHub Copilot |
| Vibe Coding Era | 2025 | 50% Prompting + 50% AI Generation | Co-pilot | Cursor、ChatGPT |
| Agentic Coding Era | 2026 | 80% Agent Coding + 20% Human Review | Orchestrator | Claude Code、Codex、Devin |

### 2.3 從輔助工具到自主代理：AI 軟體開發第三時代
> 來源：*The third era of AI software development*

#### 三個時代
1. **第一時代：智慧補齊**：開發者手動編碼，AI 提供即時片段的程式碼補齊
2. **第二時代：人機協作代理**：開發者透過「提示與回應」即時引導 AI，但依賴本地機器資源
3. **第三時代：雲端與自主代理**：AI 代理在專屬雲端環境中運行，具備獨立性

#### 開發者角色的典範轉移
1. **角色根本轉變**：從「碼農」到「架構師」，專注系統問題拆解、審核 AI 產出
2. **審查機制升級**：淘汰逐行程式碼差異（Diffs）審查，轉向系統日誌、影片記錄與即時預覽
3. **業界現況**：Cursor 內部已有超過 **35% 的 Pull Requests** 由自主 AI 代理建立

---

## 3. 市場現況與企業挑戰：SaaS 的黃昏與 AI-Native 的黎明

### 3.1 SaaS 股跌勢背後的真相

- 市場正在懲罰「舊時代思維」：缺乏智慧化能力的產品正在失去競爭力
- **護城河的消失**：過去需要數年累積的功能優勢，現在可能被 AI 在數週內複製

### 3.2 從軟體時代邁向 AI-Native

- 典範轉移：**From Software as a Service → Service as a Software**
- 從程式碼競爭到**架構思維競爭**
- AI-Native 新創優勢：3–5 人精實團隊，能構建過去需要數十人才能完成的複雜產品

> **關鍵洞察**：未來的軟體產品若無 AI 深度整合，就如同智慧型手機時代的功能型手機——技術上可行，但已不符合市場期待。AI 能力將從「加分項」變成「基本配備」。

### 3.3 SaaS → Service-as-a-Software

| 維度 | 舊 SaaS 模式 | Service-as-a-Software |
|---|---|---|
| 計費基礎 | 每人／每月訂閱（seat-based） | 按成果計酬（outcome-based） |
| 自動化程度 | Copilot 副駕輔助，人仍是主體 | 全自動端到端執行，AI 是主體 |
| 規模邊界 | 受人力雇用上限制約 | 24/7、指數級無邊際擴展 |

> 全球軟體市場約 3,500 億美元，服務市場卻是數兆美元。AI Agent 打開的，是一個比 SaaS 大十倍以上的市場空間。

### 3.4 為什麼 SaaS 會走向終結？

- **問題一：SaaS 是「最大公約數」解法**：企業必須改變自己的流程去配合工具，本質上是「妥協文化」
- **問題二：客製化成本過去太高**：AI coding 讓客製化解決方案的邊際成本趨近於零

### 3.5 Palantir 案例：垂直深耕 vs 水平鋪開

- **Field Engineer（FDE）**：現場作戰，萃取隱性知識（tacit knowledge），將混沌業務流程轉譯為可被系統化的規格
- **Product Engineer（PD）**：將現場解法產品化、模組化，讓成功經驗能被複製

垂直型 AI 代理的護城河來自四個核心要素：**專業知識、成果導向、數據優勢、滿足未被服務的需求**

### 3.6 個人如何反應

1. **數據分析能力 → 資料是 AI 的原料**：資料工程、清洗、pipeline 設計，是每個參與 AI 系統建構的工程師都需要懂的基本功
2. **成為領域專家 → T 型升級為 π 型人才**：「懂醫療的軟體工程師」、「懂供應鏈的系統架構師」的稀缺性將大幅提升
3. **打造 AI 工具箱 → 實踐重於理論**：從 coding assistant 開始，逐步延伸到 agent workflow
4. **選擇的品味 → 人類最後的不可替代性**：AI 可以快速產出，但你必須知道什麼是好的

> **「Do right thing 將比 do thing right 來得重要。」**

### 3.7 Thinking your Final Project — 三個思考問題

1. **你未來想深耕哪個垂直領域？**：軟體工程師 × 領域專業 = 未來稀缺資源
2. **你能設計一個 outcome-based 的 AI 服務嗎？**：如何定義「成果」並設計計費機制？
3. **你的「選擇品味」是什麼？**：在 AI 大量生成內容與程式碼的時代，你憑什麼判斷好壞？

---

## 4. Agentic Engineering — 從 Coding 到 Architecting

### 4.1 核心能力的本質轉變

- 傳統技能（程式碼產出速度、語法精通度、框架熟悉度）正在迅速貶值
- 未來競爭關鍵：**How to architect & prompt**

#### 三層競爭力
1. **定義問題的精準度**（第一層：問題定義者）：將模糊商業需求拆解為清晰邏輯結構
2. **系統架構的廣度**（第二層：架構設計者）：設計高可用、高擴展、容錯性強的系統
3. **整合 AI 的深度**（第三層：AI 整合專家）：如何在正確場景選用正確模型，設計 AI 與人類的協作流程

---

## 5. CLI 優先的 AI 編程工作流

### 5.1 核心命題

- **Chat 介面**讓你「獲得答案」
- **CLI 整合工具**讓你「完成工程」
- 對 CS 學生而言，兩者的差距，正是學習工程思維的關鍵分水嶺

### 5.2 時代背景：Agentic Era 的工作流典範轉移

| 典範 | 年份 | 互動模式 | 工程師角色 | 代表工具 |
|---|---|---|---|---|
| 對話式 AI | 2022–2024 | 問答、貼上程式碼 | 執行者 | ChatGPT Web、Claude.ai |
| IDE 整合 AI | 2023–2025 | 行內補全、側邊欄對話 | 引導者 | Copilot、Cursor Inline |
| **Agentic CLI** | **2025–** | **自主讀寫、執行測試、提交程式碼** | **督導者** | **Claude Code、Codex CLI** |

### 5.3 Andrej Karpathy 的核心論述

1. **Software 3.0 與提示即程式**：「Prompt 就是程式，AI 的預訓練知識完成了其餘的部分。」CLI 讓提示直接作用於真實工程環境，而非只停留在對話視窗
2. **「Vibe Coding」的邊界**：純粹的 Vibe Coding 適合低風險原型，而不適合正式工程
3. **工程師需掌握全新的「抽象層」**：agents、subagents、prompts、contexts、memory、modes、permissions、tools、plugins、skills、hooks、**MCP**、LSP、slash commands、workflows、IDE integrations

### 5.4 工具能力層級光譜（Autonomy Spectrum）

| Level | 名稱 | 代表工具 | 說明 |
|---|---|---|---|
| 1 | 增強型自動補全 | GitHub Copilot、Tabnine | 逐行建議，純被動反應 |
| 2 ⚠️ | 互動式助理（多數學生停留於此） | ChatGPT Web、Claude.ai Chat | 可產生完整函式，但不執行、不迭代 |
| 3 | 受監督代理 | Cursor、Windsurf、Cline | 可讀寫多個檔案、執行命令，每步請求許可 |
| 4 ✅ | 自主代理（工程師目標） | Claude Code、Aider、Devin AI | 以最小監督執行多步驟計畫，自動迭代失敗 |
| 5 | 實驗性全自主 | 研究階段 | 可自主執行數小時乃至數天的複雜工程專案 |

### 5.5 為什麼 CLI 工具對工程學習更有效？

1. **「迫使透明度」的學習環境**：終端機強制代理必須說明它在做什麼，Chat 介面產生的是「黑盒輸出」
2. **可組合性與可腳本化（Composability & Scriptability）**：可整合進 CI/CD pipeline、在容器中運行
3. **Chat 介面的根本限制：脈絡斷裂問題**：Chat 介面每次對話都是「脈絡孤島」，CLI 工具以整個 repository 為上下文
4. **效能與資源效率**：計算資源集中在「思考」上，而非渲染 UI

### 5.6 主流工具比較：CS 學生的選擇框架

| 工具 | 類型 | Agentic 層級 | 最適場景 | 學習曲線 |
|---|---|---|---|---|
| Claude Code | CLI Agent | Level 4 | 複雜多檔案工程、架構決策 | 中 |
| Codex CLI | CLI Agent | Level 4 | 高速任務自動化、生產環境部署 | 中 |
| Cursor | IDE-embedded | Level 3 | 中小型功能、重構、測試生成 | 低 |
| VSCode + Copilot | IDE Extension | Level 1–2 | 行內補全、快速建議 | 低 |
| Claude.ai / ChatGPT | Web Chat | Level 2 | 概念探索、原型概念驗證 | 最低 |

### 5.7 MCP（Model Context Protocol）：CLI 優先的工程基礎設施

- 2024 年底，Anthropic 開源了 MCP，成為 AI 工具整合的通用標準
- 大型語言模型本身是「stateless」，MCP 解決這個根本性問題

#### MCP 的四大核心能力
1. **讀取整個 Codebase**：即時理解整個程式碼庫結構，跨越數十個檔案的全域脈絡感知
2. **連接工程基礎設施**：整合 Git、CI/CD pipeline、資料庫與外部 API
3. **多 Agent 協同**：讓多個 Agent 協同工作於同一個工程任務
4. **加速新工程師上手**：透過對話式探索程式碼庫

### 5.8 學生的實踐建議

#### 學習路徑
1. **入門期（1–4 週）**：VSCode + Copilot 行內補全；Cursor Tab 模式
2. **發展期（1–2 個月）**：Cursor Agent Mode 多檔案任務委派；Claude.ai Chat 概念探索與 SDD 草稿
3. **成熟期（持續）**：Claude Code CLI 完整 Agentic 工程；Codex CLI 高速任務自動化；MCP 自訂整合

#### 核心學習原則
- **脈絡工程優先**：不要只會「問問題」，要學會「提供脈絡」；CLAUDE.md / AGENTS.md 就是你的 SDD 起點
- **迭代迴圈設計**：計畫 → 執行 → 測試 → 迭代，設計好這個迴圈比寫好單一 Prompt 更重要
- **可驗證性思維**：訓練自己設計「可驗證的任務邊界」
- **工具組合不依賴**：Claude Code + Git hooks + CI/CD + MCP servers 構成完整自動化工程系統

> **關鍵洞察**：「AI 委派直覺」只能在真實工程實踐中培養，而非在 Chat 介面中可以學到的技能。

> Chat 介面是「思考工具」；CLI 工具是「執行工具」。兩者互補，但 CLI 工具是工程主力。

### 5.9 工程師的角色轉型

> 「Karpathy 描述這是一個相轉變（phase change），而非漸進式改進。軟體工程師的角色正在從撰寫個別程式碼行，轉向協調大規模的程式碼行動。」— ShiftMag

- 現在正是最好的時機：AI 工具足夠成熟，讓你能完成真實的工程任務；工具生態又足夠新，讓掌握它的人擁有真實的競爭優勢

> **CLI 優先，不是因為它比較難；而是因為它讓你學到的，是真正的工程。**

---

## 6. Agentic Product：Claude Cowork

### 6.1 Cowork 是什麼？從產品演化看 Agentic 概念

#### 起源：工程師工具意外走紅
- Anthropic 在 2024 年底推出 Claude Code（CLI 終端機工具）
- 發現使用者用它做：度假研究、製作簡報、清理 email、婚禮照片救援、監控植物生長、控制烤箱……

#### 產品抽象化路徑
1. **Claude Code**（CLI, 2024）：CLI 終端機工具，面向開發者，需熟悉命令列操作
2. **Claude Cowork**（Desktop App, Jan 2026）：以 GUI 包裝相同架構，移除技術門檻，人人可用
3. **Microsoft Copilot Cowork**（Cloud, Mar 2026）：移入企業雲端，整合 M365 生態系

> 本質：**Cowork = Claude Code 的無終端機版本**，相同的 Agentic 執行架構，透過 Desktop App GUI 讓非開發者也能使用

### 6.2 Cowork 五大 Agentic 核心概念

#### 概念 1：自主規劃與任務分解（Autonomous Planning & Task Decomposition）
- **傳統 Chat AI**：使用者問 → AI 答 → 結束（單輪對話，被動回應）
- **Agentic AI（Cowork）**：使用者描述目標 → Claude 自動分解子任務 → 依序或並行執行 → 交付最終成果
- 示範：「幫我把過去三個月的出差收據截圖整理成 Excel 報表…」
  - 流程：讀取圖片 → OCR 辨識 → 結構化資料 → 建立試算表 → 加入公式 → 格式化輸出

#### 概念 2：工具使用（Tool Use）

| 工具類型 | 具體能力 | Agentic 術語 |
|---|---|---|
| 📁 檔案系統 | 讀取、建立、編輯、刪除檔案 | File I/O Tool |
| 🌐 瀏覽器 | 點擊、填表、網頁導覽 | Browser Tool |
| 🔌 MCP 連接器 | Google Drive、Slack、DocuSign、Salesforce | External API Tool |
| ⚙️ 程式執行 | 在隔離沙箱中執行程式碼 | Code Execution Tool |

#### 概念 3：長時間執行與背景運作（Long-Running Tasks & Asynchronous Execution）
- **無對話逾時限制**：複雜任務可持續執行數分鐘至數十分鐘
- **排程任務**：可設定週期性自動化工作
- **非同步執行**：描述任務 → 離開 → 回來看結果

#### 概念 4：人機協作迴圈（Human-in-the-Loop）
- Claude 開始執行 → 遇到重要決策 → 等待使用者回饋 → Claude 繼續完成

三大關鍵安全設計：
- 🗑 **刪除保護**：永久刪除動作強制需要明確授權
- 📂 **資料夾沙箱**：Claude 只能存取使用者主動授權的資料夾
- 👁 **透明推理**：每個步驟顯示正在執行的動作

#### 概念 5：Sub-Agent 協作（Multi-Agent Orchestration）
- Claude 扮演 **Orchestrator**，協調多個並行的 Sub-agents 同時工作
- 示範：並行讀取多篇 PDF → 找出研究方法相似的論文群組 → 生成文獻綜述大綱

### 6.3 Cowork 的架構解析（工程背景）

- Simon Willison 逆向工程發現：Cowork 使用 **Apple Virtualization Framework（VZVirtualMachine）**，下載並啟動客製化 Linux root filesystem，將使用者授權的資料夾 mount 進去

| 維度 | Claude Code | Cowork |
|---|---|---|
| 介面 | CLI 終端機 | Desktop App GUI |
| 目標使用者 | 開發者 | 所有人 |
| 沙箱設定 | 使用者手動設定 | 自動配置 VM |
| 技術門檻 | 需懂 CLI、git | 零技術門檻 |
| 底層架構 | 相同 | 相同 |

### 6.4 安全議題：Agentic AI 的必修課

- ⚠️ **風險 1：Prompt Injection 攻擊**：網頁中隱藏的惡意指令可能被 Claude 執行；Anthropic 坦承「目前無法提供 100% 保證」，是整個 AI 產業的開放研究問題
- 💥 **風險 2：破壞性動作**：Agent 有能力刪除檔案、修改資料庫、送出電子郵件，一旦執行可能不可逆
- **設計原則**：最小授權（Principle of Least Privilege）＋ 明確確認機制

### 6.5 Cowork 在 Agentic 光譜中的定位

| Level | 名稱 | 代表產品 |
|---|---|---|
| 1 | 純 Chat 被動回答 | Claude.ai Chat |
| 2 | 加入工具呼叫 | Claude with Tools、MCP |
| **3** | **加入多步驟執行（我們今天討論的位置）** | **Claude Cowork / Claude Code** |
| 4 | 加入多 Agent 協調 | Multi-Agent Systems、LangGraph |
| 5 | 持久記憶與學習 | Fully Autonomous Agents |

> **Cowork 的定位**：具有明確 human-in-the-loop 的**半自主 Agent**，適合生產力任務場景。它是學生從 Chat AI 邁向完整 Agentic 架構理解的**最佳切入點**。

### 6.6 案例範例

#### 案例 A：數據清洗與視覺化
- **指令**：「從 2024 全台上市公司薪資數據中整理出『員工薪資平均數』調整最多的 10 家公司，並與『員工薪資中位數』的成長 % 數，畫出長條圖比較。」
- Claude 在隔離環境執行 Python 腳本，自動完成資料清洗、統計分析與圖表生成
- 優勢：不需要上傳至雲端，所有操作都在本機端完成
- 輸出：完整的 HTML 互動式視覺化檔案

#### 案例 B：收據自動轉 Excel
1. 將收據圖檔放入資料夾
2. 指令：「分析此資料夾中的所有收據，提取日期、項目、金額與稅額，並生成一個帶有總計公式的 Excel 表格。」
3. 直接在本地資料夾開啟產出的 `.xlsx` 檔案

---

## 7. 參考來源

- The New Stack (2025). *AI Coding Tools in 2025: Welcome to the Agentic CLI Era*
- d4b.dev (2026). *My AI Coding Tools Timeline (2021–2026)*
- Ikangai (2025). *Agentic Coding Tools Explained: Complete Setup Guide*
- Faros AI (2026). *Best AI Coding Agents for 2026: Real-World Developer Reviews*
- Anthropic / Augment Code (2026). *2026 Agentic Coding Trends Report*
- MIT Technology Review (2026). *AI Coding Is Now Everywhere. But Not Everyone Is Convinced*
- Stack Overflow (2025). *2025 Developer Survey*
- Descope (2025). *Developers Guide to AI Coding Tools: Claude vs. ChatGPT*
- Pento (2025). *A Year of MCP: From Internal Experiment to Industry Standard*
- Toms Guide (2026). *Claude Code vs ChatGPT Codex: Which AI Coding Agent Is Actually Better?*
- KDnuggets (2025). *Top 5 Agentic Coding CLI Tools*
- ShiftMag (2026). *Andrej Karpathy Admits Software Development Has Changed for Good*
- Latent Space (2025). *Andrej Karpathy on Software 3.0: Software in the Age of AI*
- Futurum (2025). *Karpathy's Thread Signals AI-Driven Development Breakpoint*
- Speak Engineering (2026). *Embracing the Agentic Engineering Era at Speak*
- arXiv (2025). *Generative AI and the Transformation of Software Engineering* (arXiv:2510.10819)
- Citrini Research (2026). *THE 2028 GLOBAL INTELLIGENCE CRISIS*
- Anthropic (2026). *Labor market impacts of AI: A new measure and early evidence*
- 孔祥重，《經理人》：*當 AI 什麼都會做，人類該培養什麼能力？*
- 簡立峰訪談，《經理人》：*花錢讓員工學 AI，公司競爭力卻原地踏步？*

# Agentic Engineering：軟體開發者的實務指南

> **Tags:** `AGENT` `MULTI-AGENT` `TOOL USE` `LLMOPS` `OBSERVABILITY` `RELIABILITY`

---

## 課程目標

學完這堂課，你將具備設計、實作與維運 Agentic 系統的完整工程能力：

1. **理解架構**：用軟體工程師的語言理解 Agent 系統的架構與設計原則
2. **系統設計**：設計並規劃單一 Agent 和 Multi-Agent 的系統架構
3. **Spec 撰寫**：應用 Spec-Driven Development 撰寫結構化 Agent 規格
4. **防禦策略**：識別 Agentic 系統的常見失敗模式，並設計對應的防禦機制
5. **可觀測性**：為 Agent 系統建立完整的 Observability 機制與監控告警
6. **工程選型**：在主流框架與自建方案之間做出合理的工程選型判斷

---

## 一、什麼是 Agentic Engineering？

### 1.1 心智模型的轉變

- **大多數人的第一印象**：使用者輸入 → `[LLM]` → 輸出文字
  - LLM 回答問題，但不主動採取行動，不呼叫工具，不觀察環境
- **Agentic 系統的真實樣貌**：使用者設定目標 → `[Agent]` 思考 → 決定行動 → 執行工具 → 觀察結果 → 繼續推理 → 真實世界的改變
- **關鍵差異**：LLM 不只是回答問題，而是主導程式的控制流程，形成自主的**感知—行動迴圈**

### 1.2 軟體執行模型的演進

| 階段 | 名稱 | 特性 |
|------|------|------|
| 1 | 傳統軟體 | 確定性（Deterministic）。人類定義所有執行路徑，相同輸入保證相同輸出 |
| 2 | 規則引擎 | 人類寫規則，系統根據規則決策。Expert System 仍然是確定性的 |
| 3 | LLM 應用 | 機率性（Probabilistic）。模型決定推理路徑，相同輸入可能產生不同輸出 |
| 4 | Agentic 系統 | 模型控制流程。動態決定下一步行動，可跨越多工具、多迴圈、多模型協作執行 |

### 1.3 LLM 應用的五個層次

| Level | 名稱 | 描述 | 範例 |
|-------|------|------|------|
| 0 | Completion | 單次 Prompt / 回應，無狀態、無迴圈 | 翻譯、摘要 |
| 1 | Chain | 固定多步驟串接，流程由人類定義 | 先摘要再翻譯 |
| 2 | RAG | 動態注入外部知識，增強回答準確性 | 問答系統 + 文件 |
| 3 | Agent | 自主決策 + 工具使用，動態執行路徑 | 自動搜尋並整理報告 |
| 4 | Multi-Agent | 多個 Agent 協作分工，系統級自主執行 | 自動化軟體開發流程 |

> 越高層次的應用，工程複雜度越高，但解決問題的能力也越強。

### 1.4 什麼是「控制流程轉移」？

```python
# ❌ 傳統軟體：人類寫死邏輯
if user_intent == "search":
    result = search_tool(query)
elif user_intent == "summarize":
    result = summarize(text)
# 必須預先定義所有路徑

# ✅ Agentic 系統：LLM 動態決定
response = llm.run(
    messages=[{"role":"user","content":goal}],
    tools=[search_tool, summarize_tool, ...]
)
# LLM 自己決定：要呼叫哪個工具？用什麼參數？要不要繼續？
```

> **工程挑戰的本質轉變**：從「我能確保每條 if/else 路徑正確」，到「我能確保 LLM 在任何情況下做出合理決策」。

### 1.5 Agentic 系統的四大核心挑戰

- 🎲 **不確定性**：相同輸入不保證相同輸出。傳統 SE 中沒有對應概念
- 🔀 **非線性執行**：執行路徑由 LLM 動態產生，難以靜態分析或預先窮舉
- ⏱ **長時執行**：任務可能跨越數分鐘甚至數小時，需要類似分散式系統的狀態管理
- 📡 **錯誤傳播**：早期推理錯誤會在後續步驟中累積並放大，類似 Pipeline 的連鎖失敗

### 1.6 Agent 的四要素模型

| 要素 | 說明 |
|------|------|
| **Perception 感知** | 接收輸入，包含文字、圖片、資料，以及工具回傳的結果。決定 Agent 能「看到」什麼 |
| **Memory 記憶** | 儲存與檢索狀態，分為短期（in-context）與長期（外部資料庫）兩種類型 |
| **Reasoning 推理** | 決定下一步行動，是 LLM 的核心能力。Thought → 規劃 → 決策的迴圈 |
| **Action 行動** | 對環境產生影響：呼叫工具、寫檔案、呼叫 API，讓 Agent 真正改變外部世界 |

### 1.7 Perception — 輸入的工程設計

| 類型 | 範例 | 工程考量 |
|------|------|---------|
| 純文字 | 使用者指令、文件內容 | Tokenization 限制、長度管理 |
| 結構化資料 | JSON、CSV、DB 查詢結果 | 格式化後注入 context，避免歧義 |
| 圖片 / 多媒體 | 截圖、圖表、PDF | 需要 Vision 模型支援 |
| 工具回傳結果 | Tool call response | 格式設計直接影響推理品質 |
| 系統狀態 | 執行環境、錯誤訊息 | 需格式化為模型可理解的文字 |

> **Garbage in, garbage out** 在 Agent 系統中被顯著放大，因為錯誤的輸入會影響後續每一個推理步驟。

### 1.8 Memory — 四種記憶類型

1. **In-Context Memory（短期記憶）**
   - 在 Context Window 內，包含對話紀錄、當前任務狀態、工具執行結果
   - 速度快，但容量有限

2. **Episodic Memory（事件記憶）**
   - 儲存在外部資料庫，包含過去對話摘要、歷史執行紀錄
   - 讓 Agent 記住跨任務的經驗

3. **Semantic Memory（語義記憶）**
   - 知識庫、文件、FAQ
   - 透過 RAG 動態檢索相關知識，不佔用 context window 空間

4. **Procedural Memory（程序記憶）**
   - 可執行的技能：Tools、Functions、Code
   - 是 Agent 能做什麼的能力清單

> **工程關鍵問題**：什麼時候「寫入」記憶？什麼時候「讀取」？什麼時候「遺忘」（清除）？

### 1.9 Reasoning — 主流推理模式

- **ReAct（Reason + Act）**：Thought → Action → Observation 迴圈，最常用的基礎模式
- **Reflection（自我批評）**：Draft Answer → [Critic]「這個答案有什麼問題？」→ Revised Answer，適合需要高品質輸出的場景
- **Chain-of-Thought（思維鏈）**：強制模型逐步推理，讓模型「展示推理過程」
- **Tree-of-Thought（思維樹）**：同時探索多條推理路徑並選擇最佳，適合複雜規劃，計算成本較高

### 1.10 Action — 工具呼叫的工程視角

Tool / Function Calling 的本質：LLM 輸出一段結構化的「意圖」，由外部程式實際執行。LLM 不直接操作世界，而是**表達意圖**。

```json
{
  "tool": "send_email",
  "parameters": {
    "to": "student@example.com",
    "subject": "作業完成通知",
    "body": "你的作業已審閱..."
  }
}
```

- ⚛ **原子性**：一個工具做一件事，讓 LLM 容易理解和正確呼叫
- 🔗 **可組合性**：工具可被串接使用，輸出能成為其他工具的輸入
- 🔒 **安全邊界**：危險操作需要確認機制（Sandboxing），不可逆操作必須有人工確認或回滾設計

### 1.11 Agentic Engineering 與 SE 的對應關係

| Software Engineering | Agentic Engineering |
|---------------------|---------------------|
| Function / Method | Tool / Skill |
| API Contract | Tool JSON Schema |
| Unit Test | Agent Eval（單一行為測試）|
| Integration Test | End-to-End Agent Run |
| Debugger | Trace / Span Viewer |
| Log | LLM Trace（含 Thought + Action）|
| CI/CD Pipeline | LLMOps Pipeline |
| Design Pattern | Agent Pattern（ReAct、RAG、HITL）|
| Code Review | Prompt Review / Eval |
| Production Monitoring | LLM Observability Platform |

---

## 二、Agent 架構設計

### 2.1 單一 Agent 的架構全貌

```
使用者輸入
    ↓
[System Prompt] ← 角色 / 目標 / 限制
    ↓
[LLM Core] ← 思考與工具決策
    ↓
[Tools]
  ├── 工具 A：網路搜尋
  ├── 工具 B：檔案讀寫
  └── 工具 C：API 呼叫
```

> System Prompt 定義 Agent 的規格，LLM Core 負責推理與決策，Tools 是 Agent 與外部世界的接口。三者缺一不可。

### 2.2 ReAct Pattern — 最基礎的 Agent 模式

> **ReAct = Reason + Act**，核心是 Thought → Action → Observation 的迴圈。

```
User: 幫我找三大科技公司的股價並計算平均值

Thought: 我需要找到三大科技公司是哪些
Action: search_web("台灣三大科技公司 2025")
Observation: 台積電、聯發科、鴻海

Thought: 現在我需要三家公司的股價
Action: get_stock_price(symbol="2330") → 850 元
Action: get_stock_price(symbol="2454") → 1200 元
Action: get_stock_price(symbol="2317") → 210 元
Action: calculate("(850+1200+210)/3") → 753.33

Answer: 三大科技公司平均股價為 753.33 元
```

**停止條件：**
- 任務完成判斷：Agent 自行判斷任務已達成目標
- `max_steps` 限制：達到最大步驟數強制停止
- `max_tokens` 限制：達到 Token 上限強制停止
- 不可恢復錯誤：發生無法 retry 的嚴重錯誤

### 2.3 Reflection Pattern — 讓 Agent 自我批評

> 核心概念：**生成 → 批評 → 修正** 的迴圈。

流程：產生草稿 → 批評與評分 → （低於門檻：修正 / 達到門檻：最終結果）

**應用場景：**
- 程式碼品質審查（生成 → 審查 → 修正）
- 文件撰寫（草稿 → 編輯 → 定稿）
- 測試案例設計（生成測試 → 驗證覆蓋率 → 補充）

**工程考量：**
- Critic 的評分標準需要明確定義，避免過於寬鬆
- 設定最大迭代次數，防止無限修正迴圈
- Critic 本身也可能出錯，建議加入 meta-evaluation

### 2.4 Plan-and-Execute Pattern — 長任務的解法

> 先由 Planner 規劃完整計畫，再由 Executor 逐步執行，最後由 Evaluator 評估品質。

```
Phase 1: 規劃者 → 產生完整任務清單與細項
Phase 2: 執行者 → 依序執行清單上的每一步驟
Phase 3: 評估者 → 檢核品質，決定完成或重規劃
```

**與 ReAct 的差異：**
- ReAct：邊想邊做
- Plan-and-Execute：先想清楚再做；在長任務中更穩定，早期的規劃錯誤可以在執行前被發現和修正

### 2.5 為什麼需要 Multi-Agent？

單一 Agent 的四個關鍵瓶頸：

- **Context Window 限制**：超過 context window 就會「遺忘」早期資訊，導致長任務失準
- **專業化不足**：一個 Agent 什麼都做，什麼都不精；每個 Agent 專精一個領域可提升品質
- **無法平行執行**：單一 Agent 只能序列執行；多個獨立任務可以平行分配給多個 Agent
- **缺乏制衡機制**：單一 Agent 的錯誤無法自動偵測；多個 Agent 可以互相驗證（Cross-validation）

### 2.6 Multi-Agent 拓樸

#### 2.6.1 Orchestrator-Subagent

```
User Goal → Orchestrator（協調者）
              ↙           ↘
       Subagent A      Subagent B
       研究專家         寫作專家
           ↓               ↓
      [搜尋工具]       [格式化工具]
      [資料庫]         [寫作工具]
```

- Orchestrator 負責任務分解與結果整合，本身不直接操作工具
- Subagent 只需完成被分配的子任務，各自可擁有不同的工具集
- 適用：任務可以被清楚分解，且子任務相對獨立

#### 2.6.2 Supervisor Pattern

| 特性 | Orchestrator | Supervisor |
|------|-------------|------------|
| 狀態管理 | 分散 | 集中 |
| 路由方式 | 預先規劃 | 動態決策 |
| 適合任務 | 結構清晰 | 動態變化 |

- Supervisor 持有全域狀態，能夠根據當前情況動態決定路由
- Workers 專注執行，不需了解全局

#### 2.6.3 Pipeline

```
輸入 (Input) → 資料蒐集 → 資料清理 → ... → 輸出
```

- ✅ 優點：每個 Agent 職責清晰、容易測試、容易理解和維護
- ⚠ 缺點：任何節點失敗會中斷整個 Pipeline，需要設計好 Checkpoint 和 Retry 機制

#### 2.6.4 Debate（辯論模式）

```
Agent A（提出方案）↔ Agent B（反駁 / 質疑）
              ↓ 辯論迴圈
        Debate Judge（裁判 / 整合者）
              ↓
          宣布最終結論
```

- 應用場景：高風險決策、程式碼安全性審查、複雜設計方案選擇
- 核心優點：透過相互質疑，強制暴露方案的弱點
- 本質是「紅隊演練」（Red Teaming）的自動化實作

### 2.7 Agent 間通訊 — 三種模式

1. **Message Passing（訊息傳遞）**：Agent A 傳送結構化訊息給 Agent B，類似微服務的 REST API。優點：解耦、可非同步、容易測試
2. **Shared State（共享狀態）**：所有 Agent 讀寫同一個共享資料庫或 Memory Store。優點：所有 Agent 看到最新狀態；缺點：Race condition 和寫入衝突
3. **Blackboard Pattern**：所有 Agent 都能讀寫一塊「共享白板」，各自獨立觀察並貢獻資訊。適合問題解法不確定、需要多方協作的場景

### 2.8 MCP — Model Context Protocol

> MCP 是 Anthropic 提出的開放標準，讓 AI Agent 能夠以統一的方式連接外部工具和資源。

- **沒有 MCP**：n 個 Agent × m 個工具 = n×m 個客製整合
- **有 MCP**：任何 Agent 透過統一的 MCP Protocol 連接任何 MCP Server

| 元件 | 說明 | 範例 |
|------|------|------|
| Tools | Agent 可呼叫的功能 | `create_issue`, `send_message` |
| Resources | Agent 可讀取的資料 | 檔案、資料庫、API 回應 |
| Prompts | 預定義的提示模板 | 常用 System Prompt 片段 |

### 2.9 Memory 架構深探 — RAG 作為 Semantic Memory

RAG（Retrieval-Augmented Generation）分為**索引管線**和**查詢管線**兩個 Pipeline。

| Chunking 策略 | 適合場景 | 優缺點 |
|--------------|---------|--------|
| Fixed-size | 通用場景 | 簡單但可能切斷語義邊界 |
| Semantic | 長篇敘述文件 | 保留語義完整性，實作較複雜 |
| Hierarchical | 巢狀文件（PDF）| 保留文件結構，實作最複雜 |

---

## 三、Agentic 系統的工程實踐

### 3.1 Spec-Driven Development for Agents

> **核心理念**：System Prompt 不只是「聊天設定」，它是 Agent 的**架構文件與行為規格**。

```
需求
  ↓
System Prompt（Agent 的 SDD：Role / Goal / Constraints / Output Format）
  ↓
Tool Schema（Agent 的 API Contract：每個工具的 JSON Schema 規格）
  ↓
Eval Cases（Agent 的測試案例集：Golden Dataset + 評分標準）
  ↓
實作 → Eval → 迭代（以 Eval 結果驅動 Prompt 迭代，而非靠直覺修改）
```

### 3.2 System Prompt 的結構化設計

```markdown
## Role（角色）
你是一個專業的架構審查 Agent。
你的專長是分析程式碼並找出架構問題。

## Goal（目標）
你的任務是分析使用者提供的程式碼，
找出架構問題並提供可行的改進建議。

## Constraints（限制）
- 最多處理 5 個檔案
- 不修改程式碼，只提供建議
- 必須附上具體的程式碼範例
- 不確定的地方不能假裝知道

## Output Format（格式）
以 Markdown 格式輸出：
1. 問題清單（Critical / Major / Minor）
2. 每個問題的說明
3. 解決方案（附程式碼範例）
```

| 區塊 | 工程意義 |
|------|---------|
| Role | 能力邊界：定義 Agent 的專業領域，防止超出能力範圍的操作 |
| Goal | 成功標準：明確定義什麼叫「任務完成」，是 Agent 決策的北極星 |
| Constraints | 安全邊界：定義 Agent 不能做什麼，是系統安全的第一道防線 |
| Output Format | 可測試規格：定義輸出格式，讓 Eval 能夠自動化驗證 |

### 3.3 Tool Schema 設計原則

> **核心思維**：Tool Schema 是 LLM 的 API 文件。你怎麼寫 API 文件，就怎麼寫 Tool Schema。

| 原則 | 說明 | 範例 |
|------|------|------|
| 描述要精確 | 說清楚工具的用途、適用情境、不適用情境 | 適用於X，不適用於Y |
| 參數要有型別 | 明確指定 type、format、enum | `type: integer` |
| 加上預設值 | 減少 LLM 需要猜測的地方 | `default: 5` |
| 加上限制範圍 | 防止越界輸入，保護系統安全 | `minimum: 1, maximum: 100` |
| 說明何時呼叫 | 幫助 LLM 判斷正確的呼叫時機 | 當使用者問到XX時使用 |
| 說明回傳格式 | 讓 LLM 知道如何正確解讀回傳值 | 回傳 JSON，包含 results 陣列 |

**範例對比：**

```json
// ❌ 不好的 Tool 定義
{
  "name": "search",
  "description": "",
  "parameters": { "query": { "type": "string" } }
}

// ✅ 好的 Tool 定義
{
  "name": "search_internal_docs",
  "description": "搜尋公司內部技術文件。適用：內部 API 規格、架構文件。不適用：外網搜尋（請用 web_search）。回傳：最多 5 筆文件附來源連結",
  "parameters": {
    "query": {
      "type": "string",
      "description": "支援 AND/OR/NOT 語法"
    },
    "top_k": { "type": "integer", "default": 5, "minimum": 1, "maximum": 10 }
  },
  "required": ["query"]
}
```

### 3.4 雪球式開發 — Incremental Agent Development

> **反模式**：一開始就建立複雜的 Multi-Agent 系統 → 幾乎無法除錯。

```
Step 1：單一工具、單輪對話
  → Agent + 1 個工具 → 確認基礎工具呼叫正確

Step 2：多工具選擇
  → Agent + 3 個工具 → 確認 LLM 能正確選擇工具

Step 3：加入迴圈與停止條件
  → Agent + Tools + ReAct loop → 確認多步驟推理正確

Step 4：加入 Memory
  → Agent + Tools + Memory → 確認記憶讀寫正確

Step 5：加入 Reflection
  → Generator + Critic → 確認自我批評機制有效

Step 6：拆分為 Multi-Agent
  → 只在確認單一 Agent 可靠後，才進行系統拆分
```

### 3.5 Agentic 系統的失敗模式分類

| 層次 | 失敗類型 |
|------|---------|
| **推理層** | 工具幻覺、循環推理、目標失調 |
| **工具層** | 參數錯誤、API 超時、解析失敗、不可逆操作 |
| **流程層** | 死循環、脫節執行、錯誤擴大、未停止 |
| **資源層** | 上下文溢出、頻率限制、Token 成本、時間超時 |

### 3.6 防禦性設計 — Human-in-the-Loop（HITL）

| 風險等級 | 範例 | 處理方式 |
|---------|------|---------|
| ✅ 低風險 | 搜尋網頁、讀取檔案、查詢資料庫（read-only）| 無需確認，直接執行 |
| ⚠ 中風險 | 寫入檔案、傳送通知、呼叫有費用的外部 API | 建議確認 |
| 🚫 高風險 | 刪除資料、執行資金轉移、部署到生產環境 | 必須確認 |

```python
result = agent.plan_action(goal)
if result.risk_level >= RiskLevel.HIGH:
    confirmed = human_approval_request(result.action_description)
    if not confirmed:
        agent.abort()
        return
agent.execute(result)
```

### 3.7 防禦性設計 — Guardrails

```
Input Guardrail 檢查項目：
  - 輸入格式驗證（長度、類型）
  - 有害內容過濾
  - Prompt Injection 攻擊偵測

Output Guardrail 檢查項目：
  - 輸出格式驗證（符合規格）
  - 敏感資訊遮蔽（PII 保護）
  - 行動安全性檢查（不可逆操作攔截）
```

### 3.8 防禦性設計 — 錯誤處理與 Retry 策略

```python
# Layer 1：自動重試（瞬時的網路問題）
@retry(max_attempts=3, backoff=exponential)
def call_external_api(params): ...

# Layer 2：降級策略（使用備用工具）
try:
    result = primary_tool(params)
except ToolUnavailableError:
    result = fallback_tool(params)

# Layer 3：通知 Agent 失敗，讓 Agent 自行決策
if all_attempts_failed:
    return ToolResult(
        success=False,
        error="工具不可用，請使用工具 X 或稍後再試"
    )

# Layer 4：升級 Human（自動通報）
if critical_failure:
    notify_human(incident_details)
    agent.pause_and_wait()
```

### 3.9 防禦性設計 — 最小權限原則

> 每個 Agent 和工具只應擁有完成任務所需的最小權限。過度授權是 Agentic 系統安全事故的主要來源之一。

**Sandboxing 的工程實作：**

| 資源 | 最小權限設計 |
|------|------------|
| 檔案系統 | 限定讀寫目錄路徑 |
| 資料庫 | 分開 read / write 帳號 |
| API | 限制呼叫端點和請求頻率 |
| 程式碼執行 | 使用 Docker / 沙箱環境 |
| 網路存取 | 白名單過濾 |

### 3.10 可觀測性 — 三大支柱

**為何 Agentic 系統更需要 Observability？**
- 執行路徑由 LLM 動態生成，難以預測
- 相同輸入可能產生不同執行路徑
- 錯誤可能在 10 個工具呼叫之後才顯現
- 多個 Agent 的因果鏈追蹤困難

**三大支柱：**

1. **Traces — 完整執行鏈紀錄**

```
Trace ID: task_20250311_001
├─ Span: agent.think [450ms]
├─ Span: tool.web_search [1200ms]
│   ├─ Input: {"query": "台積電股價"}
│   └─ Output: {"results": [...5 items...]}
├─ Span: tool.write_file [50ms]
└─ agent.final_response [200ms]
    └─ Tokens: 4532 input / 1204 output
```

2. **Metrics — 量化監控指標**
   - Latency（P95 > 30s 告警）
   - Token Usage（超預算 80% 告警）
   - Success Rate（< 90% 告警）
   - Tool Call Count（異常高時告警）
   - Retry Rate（> 20% 告警）

3. **Logs — 結構化日誌**

```json
{
  "timestamp": "2025-03-11T10:30:00Z",
  "trace_id": "task_001",
  "level": "INFO",
  "event": "tool_call",
  "tool": "web_search",
  "duration_ms": 1200
}
```

### 3.11 Eval-Driven Development

| Eval 類型 | 說明 | 範例 |
|----------|------|------|
| Exact Match | 輸出完全符合預期 | 工具呼叫參數是否正確 |
| Semantic Match | 意義等同（允許不同表達）| 答案是否包含關鍵資訊 |
| LLM-as-Judge | 讓另一個 LLM 評分 | 答案品質、邏輯一致性 |

**Eval 流程四步驟：**

1. **建立 Golden Dataset**：收集真實任務樣本，標注預期行為
2. **定義評分標準**：哪些輸出算「正確」？用什麼指標評分？
3. **自動化執行 Eval**：每次 Prompt 更動後自動跑 Eval
4. **追蹤 Eval 趨勢**：防止 Prompt 修改造成能力退化（Regression）

### 3.12 Checkpoint 與狀態持久化

```python
class AgentCheckpoint:
    def save(self, state: AgentState):
        """儲存當前狀態"""
        checkpoint = {
            "task_id": state.task_id,
            "completed_steps": state.completed_steps,
            "current_plan": state.current_plan,
            "tool_results": state.tool_results,
            "timestamp": datetime.utcnow().isoformat()
        }
        db.save(f"checkpoint:{state.task_id}", checkpoint)

    def restore(self, task_id: str) -> AgentState:
        """從上次停止的地方恢復"""
        checkpoint = db.get(f"checkpoint:{task_id}")
        return AgentState.from_checkpoint(checkpoint)
```

**建議的 Checkpoint 時機：**
- 每個主要工具呼叫完成後
- 完成一個計畫步驟後
- 高風險操作執行前（確保有可回滾的狀態點）

---

## 四、工具生態與實作選型

### 4.1 主流 Agentic Framework 比較

| 框架 | 定位 | 主要特色 | 學習曲線 |
|------|------|---------|---------|
| LangGraph | 圖形化工作流 | 有狀態、可視化、支援迴圈，適合複雜工作流 | 中等 |
| CrewAI | 角色導向 Multi-Agent | 快速原型、自然語言定義角色，上手快 | 低 |
| AutoGen | 對話式 Multi-Agent | 辯論模式、程式碼生成擅長，研究導向 | 中等 |
| Dify | 低程式碼平台 | GUI 設計、快速部署，適合非技術用戶 | 低 |
| Semantic Kernel | 企業級 | .NET / Azure 整合，微軟生態首選 | 高 |
| 純 SDK | 最大彈性 | 無框架限制、完全自控，效能最佳化空間最大 | 高 |

> **框架的鎖定風險（Vendor Lock-in）**：框架更新頻繁，API 常有 Breaking Changes。建議在框架和業務邏輯之間加一層抽象，核心業務邏輯不應依賴特定框架。

### 4.2 框架選型決策樹

```
您的主要需求是什麼？
├── 快速概念驗證         → CrewAI 或 Dify
├── 複雜的工作流（含條件分支和循環）→ LangGraph
├── 多智能體辯論或代碼生成協作  → AutoGen
├── Azure 和 .NET 生態系統的企業環境 → Semantic Kernel
└── 高度定制或性能優化       → 純 SDK（Anthropic API / OpenAI API）
```

### 4.3 Agent 的部署模式

| 模式 | 適合場景 | 代表技術 | 特點 |
|------|---------|---------|------|
| ⚡ Serverless | < 30 秒的單次任務 | AWS Lambda / Vercel Functions | 自動擴縮、成本低，但有冷啟動延遲和時間限制 |
| 🐳 Container | 分鐘到小時的複雜任務 | Docker + Kubernetes | 可持久化狀態、彈性高，需要管理基礎設施 |
| 📬 Queue-based | 不需要即時回應的任務 | Redis Queue / SQS + Worker Pool | 可靠、可重試、可監控 |

### 4.4 LLMOps — Agent 系統的維運循環

```
開發 → 評估 → 部署 → 監控與迭代 → 開發（循環）
```

LLMOps 是 LLM 系統的 DevOps，包含從開發到監控的完整循環。

### 4.5 Prompt 版本管理

```yaml
# prompts/research_agent/v2.1.0.yaml
version: "2.1.0"
created: "2025-03-11"
author: "kun-ta"
changelog: |
  新增工具使用說明
  修正輸出格式不一致問題
system_prompt: |
  ## Role
  你是專業的研究 Agent...
eval_results:
  golden_dataset: "research_eval_v3"
  pass_rate: 0.94
  avg_tokens: 3200
```

**推薦工具**：LangSmith、Langfuse、Weights & Biases（Weave）

### 4.6 Token 成本控制策略

| 策略 | 說明 | 效果 |
|------|------|------|
| Prompt 壓縮 | 移除冗餘文字，精簡 System Prompt | 中 |
| Context 修剪 | 只保留最近和最重要的對話記錄 | 高 |
| 摘要替換 | 用摘要替換完整的長對話歷史 | 高 |
| 工具結果截斷 | 限制工具回傳的資料量 | 中 |
| 模型分層 | 簡單任務用小模型，複雜任務用大模型 | 高 |
| Cache 機制 | 相似查詢重用之前的結果 | 視情況 |

```python
class CostBudget:
    max_tokens = 50_000
    max_tool_calls = 20
    max_wall_time = 300  # seconds

    def check_budget(self, usage):
        if usage.tokens > self.max_tokens * 0.8:
            agent.warn("即將達到 Token 預算上限")
        if usage.tokens > self.max_tokens:
            agent.abort("已超過 Token 預算")
```

---

## 五、綜合討論與課程總結

### 5.1 Agentic Engineering 的現實挑戰

| 層面 | 挑戰 |
|------|------|
| 🔧 技術層面 | 延遲高（每個 LLM 推理步驟需要時間）；成本高（長任務消耗大量 Token）；測試困難（需要 LLM-as-Judge）|
| ⚙ 工程層面 | Prompt Regression（修改 Prompt 可能破壞已有能力）；觀測困難（多 Agent 因果鏈難以追蹤）；規格難以窮舉 |
| 🏢 組織層面 | 技能轉型（工程師需要理解 LLM 的機率性特性）；責任歸屬（自主行動造成的錯誤由誰負責？）；Human Oversight |

### 5.2 安全與倫理的工程責任

**Agentic 系統的潛在風險：**

1. **Prompt Injection 攻擊**：外部資料（網頁、文件）中藏入惡意指令，Agent 被騙執行非預期的操作
2. **目標偏移（Goal Misalignment）**：Agent 找到「捷徑」達到目標，但方式有害。需要 Constraints 和 Guardrails 防範
3. **過度自主**：Agent 在不該自行決定的地方做出決策。HITL 的設計是最重要的護欄

> **工程品質即倫理責任。** 我們不能以「這是 AI 的決定」為理由推卸設計者的責任。系統的邊界、約束、審查機制，都是工程師的設計選擇。

### 5.3 核心學習回顧

1. **Agent = Perception + Memory + Reasoning + Action**：用軟體工程的眼光拆解 Agent，讓抽象概念變得可設計、可測試
2. **控制流程轉移**：LLM 控制流程 ≠ 人類控制流程，帶來全新的工程挑戰與思維方式
3. **Spec-Driven Development**：System Prompt 是架構文件，Tool Schema 是 API Contract，Eval Cases 是測試規格
4. **雪球式開發**：從最小可用系統開始，逐步驗證每個層次，避免複雜度爆炸
5. **Observability First**：不可見的系統是不可維護的系統。Traces、Metrics、Logs 是生產環境的生命線
6. **安全與可靠性**：最小權限、HITL、Guardrails 是工程基本功，不是選項，是工程師的專業責任

### 5.4 Q&A 討論題

1. 你現在負責或感興趣的系統中，哪個部分最適合導入 Agent 架構？預期效益是什麼？最大的風險是什麼？
2. 如果你要設計一個「自動 Code Review Agent」，你會選哪個 Agent Pattern？需要幾個工具？HITL 的觸發點在哪裡？
3. 如何向團隊說服「要先建立 Eval 機制，才能更動 Prompt」的重要性？你會用什麼論據和數據來支持？

### 5.5 Do it yourself — 三個練習

1. **工具設計練習**：選擇你熟悉的領域，設計 3 個 Tool 的 JSON Schema，要求包含：明確描述、型別、限制、使用時機說明
2. **雪球式開發實作**：用任意 Agent 框架，完成「6 步驟雪球式開發」的 Agent，從單工具開始，最終加入 Reflection 機制
3. **Eval 設計練習**：為你設計的 Agent 建立 10 個 Golden Dataset 測試案例，定義評分標準，說明哪些用 Exact Match，哪些用 LLM-as-Judge

### 5.6 延伸學習資源

- **Anthropic: Building Effective Agents**：Anthropic 官方出版的 Agentic 系統設計指南，深入探討 Agent 模式的實務應用與最佳實踐
- **Chip Huyen: *AI Engineering*（O'Reilly, 2025）**：目前最系統化的 AI 工程化專書，涵蓋從模型評估到 LLMOps 的完整工程視角
- **LangGraph 官方文件**：有狀態 Graph-based Agent 框架的完整文件，含豐富範例與教學
- **Langfuse 官方文件**：Observability 實作的最佳參考
- **OpenAI Cookbook: Agent Patterns**：大量 Agent 設計模式的可執行範例，適合邊讀邊實作

---

## 附錄 A — 術語速查表

| 術語 | 說明 |
|------|------|
| Agent | 能自主決策並執行行動的 LLM 系統 |
| Orchestrator | 負責協調多個 Subagent 的協調者 |
| Tool / Function Calling | LLM 呼叫外部程式的機制，LLM 表達意圖，由外部程式執行 |
| ReAct | Reason + Act 的 Agent 推理模式，Thought → Action → Observation 迴圈 |
| RAG | Retrieval-Augmented Generation，動態注入外部知識 |
| MCP | Model Context Protocol，標準化工具整合協定 |
| HITL | Human-in-the-Loop，關鍵操作需人類確認 |
| Guardrails | 輸入 / 輸出驗證層，防止不合規操作 |
| LLMOps | LLM 系統的 DevOps，包含評估、部署、監控 |
| Eval | 評估 Agent 行為是否符合預期的系統化方法 |
| Trace / Span | Agent 執行的詳細紀錄，用於除錯和監控 |
| Golden Dataset | 預先標注的測試案例集，用於 Eval |
| Prompt Injection | 透過外部資料注入惡意指令的攻擊手法 |

---

## 附錄 B — Agentic Pattern 快速參考

### Single Agent Patterns

| Pattern | 適用場景 |
|---------|---------|
| ReAct | 通用推理 + 工具呼叫，最基礎的 Agent 模式 |
| Reflection | 需要高品質輸出時，生成 → 批評 → 修正迴圈 |
| Plan-Execute | 長任務 / 資源密集型任務，先規劃再執行 |

### Memory Patterns

| Pattern | 適用場景 |
|---------|---------|
| In-context | 短任務、即時狀態管理 |
| RAG | 大量外部知識查詢 |
| Episodic | 需要記憶過去任務的跨任務記憶 |

### Multi-Agent Patterns

| Pattern | 適用場景 |
|---------|---------|
| Orchestrator | 任務可清楚分解，Subagent 各司其職 |
| Supervisor | 需要動態路由，集中狀態管理 |
| Pipeline | 有明確前後依賴，線性執行流程 |
| Debate | 高風險決策 / 需要多角度驗證 |

### Reliability Patterns

| Pattern | 功能 |
|---------|------|
| HITL | 高風險操作人工確認 |
| Guardrails | 輸入 / 輸出安全驗證 |
| Checkpoint | 長任務中斷恢復 |
| Least Privilege | 工具存取權限控制 |