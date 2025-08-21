# 第4章: リアルタイムシステム

リアルタイムシステムの概念を学び、Mermaid図表を使ってシステム構成を理解します。

## リアルタイムシステムの分類

**図4-1: リアルタイムシステムの分類**

```mermaid
graph TD
    A[リアルタイムシステム] --> B[ハードリアルタイム]
    A --> C[ソフトリアルタイム]
    
    B --> D[航空機制御システム]
    B --> E[原子力発電所制御]
    B --> F[医療機器制御]
    
    C --> G[動画ストリーミング]
    C --> H[オンラインゲーム]
    C --> I[音声通話システム]
    
    style B fill:#ffcccc
    style C fill:#ccffcc

```

!!! warning "ハードリアルタイムシステム"
    デッドラインを1回でも守れないとシステム全体が破綻します。
    例：航空機の制御システム、原子力発電所の制御

!!! info "ソフトリアルタイムシステム"
    デッドラインを時々守れなくても、品質が低下するだけです。
    例：動画ストリーミング、オンラインゲーム

## タスクスケジューリング

**図4-2: タスクスケジューリングの流れ**

```mermaid
sequenceDiagram
    participant S as スケジューラ
    participant T1 as タスク1（高優先度）
    participant T2 as タスク2（低優先度）
    participant CPU as CPU
    
    S->>T2: 実行開始
    T2->>CPU: 処理中...
    Note right of T1: 緊急タスク発生！
    T1->>S: 実行要求
    S->>T2: プリエンプション
    T2-->>S: 中断
    S->>T1: 実行開始
    T1->>CPU: 緊急処理
    T1-->>S: 完了
    S->>T2: 実行再開
    T2->>CPU: 処理継続

```

## 組み込みシステムアーキテクチャ

**図4-3: 典型的な組み込みシステム構成**

```mermaid
graph LR
    subgraph "センサー類"
        S1[温度センサー]
        S2[圧力センサー]
        S3[振動センサー]
    end
    
    subgraph "マイクロコントローラー"
        MCU[CPU]
        RAM[RAM]
        ROM[ROM/Flash]
        GPIO[GPIO]
    end
    
    subgraph "アクチュエータ"
        M1[モーター]
        M2[バルブ]
        LED[LED]
    end
    
    subgraph "通信インターフェース"
        UART[UART]
        I2C[I2C]
        SPI[SPI]
    end
    
    S1 --> GPIO
    S2 --> GPIO
    S3 --> GPIO
    
    GPIO --> MCU
    MCU --> RAM
    MCU --> ROM
    
    MCU --> M1
    MCU --> M2
    MCU --> LED
    
    MCU --> UART
    MCU --> I2C
    MCU --> SPI
    
    style MCU fill:#e1f5fe
    style RAM fill:#f3e5f5
    style ROM fill:#f3e5f5

```

## スケジューリングアルゴリズム

**図4-4: 優先度ベーススケジューリング**

```mermaid
gantt
    title 優先度ベーススケジューリング
    dateFormat X
    axisFormat %s
    
    section 高優先度タスク
    タスクA（優先度1）    :active, a1, 0, 2
    タスクA（優先度1）    :active, a2, 5, 3
    
    section 中優先度タスク
    タスクB（優先度2）    :b1, 2, 2
    タスクB（優先度2）    :b2, 8, 2
    
    section 低優先度タスク
    タスクC（優先度3）    :c1, 4, 1
    タスクC（優先度3）    :c2, 10, 2

```

## まとめ

!!! note "第4章の要点"
    - リアルタイムシステムには「ハード」と「ソフト」の2種類がある
    - デッドラインの厳格さが異なる
    - プリエンプションにより優先度の高いタスクが実行される
    - スケジューリングアルゴリズムがシステムの性能を左右する
    - Mermaid図表により複雑なシステムを視覚的に理解できる
