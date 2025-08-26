"""
学習分析・フィードバック機能
学習者の行動データを収集・分析し、適応的な学習体験を提供する
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class LearningEvent:
    """学習イベントのデータ構造"""
    user_id: str
    event_type: str  # 'page_view', 'quiz_attempt', 'quiz_correct', 'time_spent', etc.
    content_id: str  # chapter_id, quiz_id, etc.
    timestamp: datetime
    metadata: Dict[str, Any] = None  # 追加データ (正答率、滞在時間など)
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data


@dataclass
class LearningProgress:
    """学習進捗の分析結果"""
    user_id: str
    content_completion: Dict[str, float]  # コンテンツID -> 完了率
    quiz_performance: Dict[str, float]    # クイズID -> 正答率
    time_spent: Dict[str, float]          # コンテンツID -> 滞在時間(分)
    difficulty_areas: List[str]           # 苦手分野のリスト
    recommended_content: List[str]        # 推奨コンテンツ
    last_updated: datetime


class LearningAnalyzer:
    """
    学習分析・フィードバック機能の中核クラス
    学習者の行動データを収集・分析し、パーソナライズされた学習体験を提供
    """
    
    def __init__(self, data_dir: Path = None):
        """
        初期化
        
        Args:
            data_dir: データ保存ディレクトリ
        """
        self.data_dir = data_dir or Path("data/learning_analytics")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 学習イベントのメモリ内キャッシュ
        self._event_cache: List[LearningEvent] = []
        self._progress_cache: Dict[str, LearningProgress] = {}
        
        # 設定
        self.cache_size_limit = 1000
        self.difficulty_threshold = 0.6  # 正答率がこれ以下だと苦手分野と判定
        self.time_window_days = 30  # 分析対象期間
        
    def log_event(self, event: LearningEvent) -> None:
        """
        学習イベントをログに記録
        
        Args:
            event: 学習イベント
        """
        try:
            # メモリキャッシュに追加
            self._event_cache.append(event)
            
            # キャッシュサイズ制限をチェック
            if len(self._event_cache) > self.cache_size_limit:
                self._flush_events_to_disk()
            
            logger.debug(f"学習イベントを記録: {event.event_type} - {event.content_id}")
            
        except Exception as e:
            logger.error(f"学習イベントのログ記録中にエラー: {e}")
    
    def _flush_events_to_disk(self) -> None:
        """メモリキャッシュのイベントをディスクに保存"""
        if not self._event_cache:
            return
            
        try:
            # 日付別にファイルを分ける
            events_by_date = defaultdict(list)
            for event in self._event_cache:
                date_str = event.timestamp.strftime('%Y-%m-%d')
                events_by_date[date_str].append(event.to_dict())
            
            # ファイルに保存
            for date_str, events in events_by_date.items():
                file_path = self.data_dir / f"events_{date_str}.json"
                
                # 既存ファイルがあれば読み込んで結合
                existing_events = []
                if file_path.exists():
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            existing_events = json.load(f)
                    except (json.JSONDecodeError, IOError) as e:
                        logger.warning(f"既存イベントファイルの読み込みに失敗: {e}")
                
                # 新しいイベントを追加
                all_events = existing_events + events
                
                # ファイルに書き込み
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(all_events, f, ensure_ascii=False, indent=2)
            
            # キャッシュをクリア
            self._event_cache.clear()
            logger.info(f"{len(events_by_date)}日分の学習イベントをディスクに保存しました")
            
        except Exception as e:
            logger.error(f"学習イベントのディスク保存中にエラー: {e}")
    
    def analyze_user_progress(self, user_id: str) -> Optional[LearningProgress]:
        """
        ユーザーの学習進捗を分析
        
        Args:
            user_id: ユーザーID
            
        Returns:
            学習進捗分析結果
        """
        try:
            # キャッシュされた分析結果をチェック
            if user_id in self._progress_cache:
                cached_progress = self._progress_cache[user_id]
                # 最新データから1時間以内ならキャッシュを使用
                if datetime.now() - cached_progress.last_updated < timedelta(hours=1):
                    return cached_progress
            
            # イベントデータを読み込み
            events = self._load_user_events(user_id)
            if not events:
                logger.info(f"ユーザー {user_id} の学習イベントが見つかりません")
                return None
            
            # 分析を実行
            progress = self._calculate_progress(user_id, events)
            
            # キャッシュに保存
            self._progress_cache[user_id] = progress
            
            return progress
            
        except Exception as e:
            logger.error(f"学習進捗分析中にエラー: {e}")
            return None
    
    def _load_user_events(self, user_id: str) -> List[LearningEvent]:
        """ユーザーのイベントデータを読み込み"""
        events = []
        
        # メモリキャッシュからユーザーのイベントを取得
        for event in self._event_cache:
            if event.user_id == user_id:
                events.append(event)
        
        # ディスクからも読み込み (過去30日間)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=self.time_window_days)
        
        for i in range(self.time_window_days + 1):
            date = start_date + timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            file_path = self.data_dir / f"events_{date_str}.json"
            
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        day_events = json.load(f)
                    
                    # ユーザーのイベントのみを抽出
                    for event_data in day_events:
                        if event_data.get('user_id') == user_id:
                            event = LearningEvent(
                                user_id=event_data['user_id'],
                                event_type=event_data['event_type'],
                                content_id=event_data['content_id'],
                                timestamp=datetime.fromisoformat(event_data['timestamp']),
                                metadata=event_data.get('metadata', {})
                            )
                            events.append(event)
                            
                except Exception as e:
                    logger.warning(f"イベントファイル {file_path} の読み込みに失敗: {e}")
        
        return events
    
    def _calculate_progress(self, user_id: str, events: List[LearningEvent]) -> LearningProgress:
        """学習進捗を計算"""
        content_completion = {}
        quiz_performance = {}
        time_spent = defaultdict(float)
        quiz_attempts = defaultdict(list)
        
        # イベントデータを分析
        for event in events:
            content_id = event.content_id
            
            if event.event_type == 'page_view':
                content_completion[content_id] = content_completion.get(content_id, 0) + 0.1
            
            elif event.event_type == 'time_spent':
                if event.metadata and 'duration_minutes' in event.metadata:
                    time_spent[content_id] += event.metadata['duration_minutes']
            
            elif event.event_type == 'quiz_attempt':
                if event.metadata:
                    quiz_attempts[content_id].append({
                        'correct': event.metadata.get('correct', False),
                        'timestamp': event.timestamp
                    })
        
        # コンテンツ完了率を正規化 (最大1.0)
        for content_id in content_completion:
            content_completion[content_id] = min(1.0, content_completion[content_id])
        
        # クイズ性能を計算
        for quiz_id, attempts in quiz_attempts.items():
            if attempts:
                correct_count = sum(1 for attempt in attempts if attempt['correct'])
                quiz_performance[quiz_id] = correct_count / len(attempts)
        
        # 苦手分野を特定
        difficulty_areas = [
            quiz_id for quiz_id, performance in quiz_performance.items()
            if performance < self.difficulty_threshold
        ]
        
        # 推奨コンテンツを生成
        recommended_content = self._generate_recommendations(
            content_completion, quiz_performance, difficulty_areas
        )
        
        return LearningProgress(
            user_id=user_id,
            content_completion=content_completion,
            quiz_performance=quiz_performance,
            time_spent=dict(time_spent),
            difficulty_areas=difficulty_areas,
            recommended_content=recommended_content,
            last_updated=datetime.now()
        )
    
    def _generate_recommendations(self, 
                                  content_completion: Dict[str, float],
                                  quiz_performance: Dict[str, float],
                                  difficulty_areas: List[str]) -> List[str]:
        """推奨コンテンツを生成"""
        recommendations = []
        
        # 苦手分野の復習を優先的に推奨
        for area in difficulty_areas:
            recommendations.append(f"復習推奨: {area}")
        
        # 未完了コンテンツで、完了率が高いものを推奨
        incomplete_content = [
            (content_id, completion) 
            for content_id, completion in content_completion.items()
            if completion < 0.8
        ]
        
        # 完了率順でソート
        incomplete_content.sort(key=lambda x: x[1], reverse=True)
        
        for content_id, _ in incomplete_content[:3]:  # 上位3つを推奨
            recommendations.append(f"継続学習推奨: {content_id}")
        
        return recommendations
    
    def generate_learning_report(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        学習レポートを生成
        
        Args:
            user_id: ユーザーID
            
        Returns:
            学習レポート (HTMLレンダリング用のデータ)
        """
        progress = self.analyze_user_progress(user_id)
        if not progress:
            return None
        
        # レポートデータを構築
        report = {
            'user_id': user_id,
            'generated_at': datetime.now().isoformat(),
            'overall_completion': sum(progress.content_completion.values()) / len(progress.content_completion) if progress.content_completion else 0,
            'average_quiz_score': sum(progress.quiz_performance.values()) / len(progress.quiz_performance) if progress.quiz_performance else 0,
            'total_study_time': sum(progress.time_spent.values()),
            'strengths': [
                quiz_id for quiz_id, score in progress.quiz_performance.items()
                if score >= 0.8
            ],
            'areas_for_improvement': progress.difficulty_areas,
            'recommendations': progress.recommended_content,
            'progress_by_content': progress.content_completion,
            'quiz_scores': progress.quiz_performance
        }
        
        return report
    
    def get_adaptive_content_config(self, user_id: str, content_id: str) -> Dict[str, Any]:
        """
        適応的コンテンツの設定を生成
        学習者の理解度に基づいてコンテンツの表示方法を調整
        
        Args:
            user_id: ユーザーID
            content_id: コンテンツID
            
        Returns:
            適応的設定 (難易度調整、追加説明の表示など)
        """
        progress = self.analyze_user_progress(user_id)
        if not progress:
            return {'difficulty_level': 'standard'}
        
        # そのコンテンツでの性能を確認
        quiz_performance = progress.quiz_performance.get(content_id, 0.5)
        completion_rate = progress.content_completion.get(content_id, 0.0)
        
        config = {
            'difficulty_level': 'standard',
            'show_additional_examples': False,
            'show_prerequisite_review': False,
            'show_advanced_topics': False
        }
        
        # 低い性能の場合：追加サポート
        if quiz_performance < 0.4 or completion_rate < 0.3:
            config.update({
                'difficulty_level': 'beginner',
                'show_additional_examples': True,
                'show_prerequisite_review': True
            })
        
        # 高い性能の場合：発展的内容
        elif quiz_performance > 0.8 and completion_rate > 0.8:
            config.update({
                'difficulty_level': 'advanced',
                'show_advanced_topics': True
            })
        
        return config
    
    def cleanup_old_data(self, days_to_keep: int = 90) -> None:
        """古い分析データを削除"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            deleted_count = 0
            
            for file_path in self.data_dir.glob("events_*.json"):
                # ファイル名から日付を抽出
                try:
                    date_str = file_path.stem.replace('events_', '')
                    file_date = datetime.strptime(date_str, '%Y-%m-%d')
                    
                    if file_date < cutoff_date:
                        file_path.unlink()
                        deleted_count += 1
                        
                except ValueError:
                    logger.warning(f"不正なファイル名をスキップ: {file_path}")
            
            logger.info(f"{deleted_count}個の古いデータファイルを削除しました")
            
        except Exception as e:
            logger.error(f"古いデータの削除中にエラー: {e}")