
---

###  `ROADMAP.ja.md` (Detailed - Japanese Version (日本語版))

# 🧭 技術進化ロードマップ (Technical Evolution Roadmap)

このロードマップは、本プロジェクトが **AI × Backend × Infrastructure × Security** を統合した  
「実務レベルの **自律型AIセキュリティエージェント**」へと進化するまでの軌跡を記録するものです。

各フェーズは **スケーラビリティ、セキュリティ、観測性（Observability）** を重視し、  
実際のプロダクション環境を想定して設計されています。

---

## 📶 フェーズ別ステータス

| フェーズ | マイルストーン | ステータス | 技術的な注力分野 |
| :--- | :--- | :--- | :--- |
| **Phase 0** | **RESTful API基盤** | ✅ **完了** | FastAPI, Pydantic, 構造化ロギング |
| **Phase 1** | **AI異常検知 & ルールベース検知** | 🚧 **進行中** | 特徴量エンジニアリング, SQLi/Traversal検知, Traceability, 推論レイテンシ |
| **Phase 2** | **セキュア認証 & DB** | 📅 **計画中** | JWT, PostgreSQL, RBAC, OWASP |
| **Phase 3** | **コンテナセキュリティ** | 📅 **計画中** | **Trivy**, SBOM, 最小ベースイメージ |
| **Phase 4** | **SRE & モデル可観測性** | 📅 **計画中** | **モデルドリフト**, エラー率, Prometheus |
| **Phase 5** | **K8s & クラウドネイティブ** | 📅 **計画中** | Kubernetes, ネットワークポリシー, HPA |
| **Phase 6** | **AIセキュリティエージェント** | 📅 **計画中** | **自律型インシデントレスポンス** |
| **Phase 7** | **AWS & IaC 本番環境** | 📅 **計画中** | **Terraform**, EKS, IRSA, CloudWatch |
| **Phase 8** | **GCP & MLOps** | 📅 **計画中** | Vertex AI, BigQuery ML, Model Registry |
| **Phase 9** | **Azure & エンタープライズAI**| 📅 **計画中** | **Azure OpenAI (LLM)**, Entra ID, Sentinel |
| **Phase 10**| **グローバルスケール基盤** | 📅 **計画中** | マルチリージョン, カオスエンジニアリング, FinOps |

---

## 📋 マイルストーン詳細

### ✅ Phase 0: 基盤構築 (Completed)
- [x] FastAPIを用いた高性能な非同期APIの実装
- [x] Pydantic v2スキーマによるデータ整合性の担保
- [x] 将来的なAI学習（データパイプライン）を見据えた構造化ロギング
- [x] 自動化されたAPIドキュメント (Swagger UI) の構築

### 🚧 Phase 1: AI異常検知 & ルールベース検知 (Current)
**目標:** 機械学習による異常検知と、既知攻撃パターンに対するルールベース検知を組み合わせた、ハイブリッド検知基盤を構築する。
- [x] リアルタイムスコアリング用エンドポイント: `POST /analyze` の実装
- [x] ログベクトルの特徴量エンジニアリング (IP頻度、リクエストパスなど)
- [x] ルールベース検知エンジンの実装
- [x] Regex-based SQL Injection detection
- [x] Regex-based Directory Traversal detection
- [x] `RuleEvaluationResult` によるルール評価結果の構造化
- [x] `RuleMatchInfo` による検知理由の追跡可能性の追加
- [ ] **異常検知モデル**の学習・改善
- [ ] **低レイテンシ推論**のためのモデル・コード最適化
- [ ] Decision Context / Request ID によるエンドツーエンドの追跡性強化
- [ ] Shadow Mode による検知結果の安全な評価

### 📅 Phase 2: セキュリティ & 永続化
**目標:** APIおよびデータストレージの堅牢化。
- [ ] パスワードのセキュアなハッシュ化 (Passlib) と JWT認証
- [ ] PostgreSQLによるデータ永続化とAlembicによるマイグレーション
- [ ] **RBAC (ロールベースアクセス制御)** の実装

### 📅 Phase 3: コンテナセキュリティ
**目標:** コンテナ環境の保護とサプライチェーンの完全性確保。
- [ ] **イメージスキャン (Trivy)**: 脆弱性(CVE)、設定ミス、シークレット漏洩のスキャン
- [ ] **最小ベースイメージ**: `python:3.12-slim` 等を使用し攻撃面(アタックサーフェス)を縮小
- [ ] **非rootコンテナ**: 権限昇格を防ぐため、non-rootユーザーでの実行を強制
- [ ] **依存関係の完全性**: `pip-audit` や `safety` を用いたPythonパッケージの検証
- [ ] **SBOM生成**: 透明性確保のためのソフトウェア部品表 (SBOM) の作成
- [ ] **セキュアなビルドパイプライン**: サプライチェーン攻撃を防ぐためのGitHub Actionsの堅牢化

### 📅 Phase 4: SRE & 可観測性 (AIにおいて重要)
**目標:** 「本番環境におけるAI」のモニタリングと信頼性向上。
- [ ] **モデルドリフト**の追跡: 時間経過に伴うAIの精度劣化検知
- [ ] **推論時間(レイテンシ)** と **APIエラー率** の監視
- [ ] Prometheus/Grafanaを利用した高リスク異常への自動アラート構築

### 📅 Phase 5: Kubernetes & クラウドネイティブ
**目標:** 本番稼働に耐えうる、セキュアでスケーラブルなAIセキュリティバックエンドのデプロイ。
- [ ] **K8sデプロイ**: ローカルの **kind** クラスターから開始し、EKS/GKEへ移行
- [ ] **ネットワークポリシー**: Pod間通信の制限 (最小特権の原則)
- [ ] **Pod Security Standards (PSS)**: *Restricted* プロファイルの強制
  - 特権(privileged)コンテナの禁止
  - hostPathマウントの禁止
  - rootファイルシステムの読み取り専用化
  - non-rootユーザーでの実行
- [ ] **Horizontal Pod Autoscaling (HPA)**: CPUやレイテンシに基づく推論APIのオートスケール
- [ ] **シークレット管理**: K8s Secrets または外部シークレットストア (Vault等) の利用
- [ ] **Ingress + TLS**: HTTPS終端による外部トラフィックの保護

### 📅 Phase 6: AIエージェントの統合
**目標:** 異常検知から対処までのループを完結させる。
- [ ] **自律的対応**の実装: AI主導の自動IPブロック、またはSlackアラート発報
- [ ] AI、バックエンド、インフラストラクチャの最終統合

---

## 🌐 Cloud & Enterprise Expansion（クラウド拡張フェーズ）

### 📅 Phase 7: AWS Integration（AWS本番環境構築 & IaC）
**目標:** AWS 上で IaC を用いた堅牢な本番環境を構築する。
- [ ] **Infrastructure as Code (IaC)**: **Terraform** による VPC / EKS のプロビジョニング
- [ ] **EKS デプロイ**: ECR へのイメージ登録と Helm チャートによる運用管理
- [ ] **AWS セキュリティ**: ALB Ingress Controller + ACM (HTTPS) および IRSA (IAM Roles for Service Accounts) の導入
- [ ] **オブザーバビリティ**: CloudWatch Logs / Metrics による統合監視
**🏆 成果物:**
> Terraform でコード管理された AWS 上のセキュアな本番環境

### 📅 Phase 8: GCP Integration（高度なAI & MLOps）
**目標:** Google Cloud の AI サービスを活用し、モデル運用（MLOps）を自動化する。
- [ ] **Vertex AI**: モデルのバージョン管理 (Model Registry) とサービング（推論API提供）
- [ ] **BigQuery ML**: 大規模ログデータの分析と異常検知の高速化
- [ ] **データパイプライン**: GCS への特徴量保存とデータポータビリティの確保
**🏆 成果物:**
> GCP ベースの高度な AI / MLOps 運用基盤

### 📅 Phase 9: Azure Integration（エンタープライズセキュリティ & LLM）
**目標:** Azure の企業向け機能と LLM を統合し、次世代セキュリティを実現する。
- [ ] **Azure OpenAI Service**: LLM (GPT-4) によるログ解析の自然言語要約と判断根拠の生成 (Explainability)
- [ ] **アイデンティティ管理**: Microsoft Entra ID (旧 Azure AD) との SSO 統合
- [ ] **セキュリティ SIEM**: Microsoft Sentinel とのログ連携による高度な脅威ハンティング
**🏆 成果物:**
> LLM × エンタープライズセキュリティの統合プラットフォーム

### 📅 Phase 10: Global-Scale Security Platform（グローバルスケール最終形態）
**目標:** 世界規模で運用可能な、自己修復・継続学習型のシステムを完成させる。
- [ ] **マルチリージョン冗長化**: リージョン間フェイルオーバーと Global Accelerator による高可用性の実現
- [ ] **カオスエンジニアリング**: 意図的な障害注入によるシステムの回復力 (Resilience) 検証
- [ ] **FinOps (コスト最適化)**: スポットインスタンスの活用と自動スケーリングによるクラウドコストの最適化
- [ ] **オンライン学習 (Online Learning)**: リアルタイムなフィードバックループに基づくモデルの継続的な再学習
**🏆 成果物:**
> 世界規模で稼働する、自律型の AI セキュリティ・プラットフォーム

---

## 🧩 全体像のまとめ（Summary）

本ロードマップは、

**ローカル開発 → AI異常検知 → セキュアAPI → Docker → Kubernetes →  
クラウド本番環境（AWS） → MLOps（GCP） → LLM統合（Azure） → グローバルスケール**

という一貫した成長曲線を描いています。

Phase0〜6 は「学習と基盤構築」、  
Phase7〜10 は「クラウド・AI・エンタープライズ統合による発展フェーズ」として設計されており、  
最終的には **自律型AIセキュリティプラットフォーム** へ到達します。

---

## 📘 関連ドキュメント
- [README.md（英語版）](./README.md)
- [README.ja.md（日本語版）](./README.ja.md)
- [ROADMAP.md（英語版ロードマップ）](./ROADMAP.md)
