window.quizData = {
  "quizzes": {
    "system-classification": {
      "type": "categorization",
      "question": "以下の要素を「ハードウェア」と「ソフトウェア」に分類してください。",
      "categories": [
        "ハードウェア",
        "ソフトウェア"
      ],
      "items": [
        {
          "name": "CPU",
          "correct_category": 0
        },
        {
          "name": "OS",
          "correct_category": 1
        },
        {
          "name": "RAM",
          "correct_category": 0
        },
        {
          "name": "コンパイラ",
          "correct_category": 1
        },
        {
          "name": "GPIO",
          "correct_category": 0
        },
        {
          "name": "デバイスドライバ",
          "correct_category": 1
        },
        {
          "name": "センサー",
          "correct_category": 0
        },
        {
          "name": "RTOS",
          "correct_category": 1
        }
      ]
    },
    "realtime-applications": {
      "type": "multiple-choice",
      "question": "以下の中でハードリアルタイムシステムに該当するものを全て選択してください。",
      "instruction": "複数の選択肢から正解を全て選んでください",
      "options": [
        "航空機の制御システム",
        "動画ストリーミングサービス",
        "原子力発電所の制御システム",
        "オンラインゲーム",
        "人工呼吸器の制御",
        "Webブラウザ",
        "自動車のエアバッグシステム"
      ],
      "correct": [
        0,
        2,
        4,
        6
      ],
      "explanation": "ハードリアルタイムシステムは、デッドラインを守れない場合に人命や安全に関わる致命的な問題が発生するシステムです。航空機制御、原子力発電所制御制御、人工呼吸器、エアバッグシステムなどがこれに該当します。"
    },
    "communication-protocols": {
      "type": "categorization",
      "question": "以下の通信プロトコルを「有線」と「無線」に分類してください。",
      "categories": [
        "有線通信",
        "無線通信"
      ],
      "items": [
        {
          "name": "UART",
          "correct_category": 0
        },
        {
          "name": "Wi-Fi",
          "correct_category": 1
        },
        {
          "name": "I2C",
          "correct_category": 0
        },
        {
          "name": "Bluetooth",
          "correct_category": 1
        },
        {
          "name": "SPI",
          "correct_category": 0
        },
        {
          "name": "ZigBee",
          "correct_category": 1
        },
        {
          "name": "CAN",
          "correct_category": 0
        },
        {
          "name": "LoRa",
          "correct_category": 1
        }
      ]
    },
    "microcontroller-features": {
      "type": "multiple-choice",
      "question": "組み込みシステムの特徴として正しいものを全て選択してください。",
      "instruction": "複数の選択肢から正解を全て選んでください",
      "options": [
        "リアルタイム性が重要",
        "高性能なGPUが必須",
        "省電力設計が重要",
        "大容量メモリが必要",
        "長時間の安定動作が必要",
        "インターネット接続が必須",
        "決定論的な動作が求められる",
        "高速な3D描画が必要"
      ],
      "correct": [
        0,
        2,
        4,
        6
      ],
      "explanation": "組み込みシステムは、リアルタイム性、省電力性、安定性、決定論的な動作が重要な特徴です。高性能GPU、大容量メモリ、インターネット接続、3D描画は一般的に必須ではありません。"
    }
  }
}