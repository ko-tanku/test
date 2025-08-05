import React from 'react';
import Layout from '@theme/Layout';

// TODO: このデータを`learning-roadmap.json`のような外部ファイルから読み込むようにする
const roadmapData = {
  title: '総合学習ロードマップ',
  description: '文系出身者が組込ソフトウェア専門家になるための学習パスです。',
  courses: [
    // 今後、各コースのメタ情報がここに追加されていく
    { id: 'embedded-system-basics', title: '組込制御の基礎', status: 'completed', prerequisites: [] },
    { id: 'microcontroller-overview', title: 'マイコンの全体像と構成', status: 'inprogress', prerequisites: ['embedded-system-basics'] },
    { id: 'mcu-peripherals', title: 'マイコンの周辺機能', status: 'todo', prerequisites: ['microcontroller-overview'] },
  ]
};

function RoadmapNode({ course }) {
  // TODO: statusに応じてスタイルを変更する
  const nodeStyle = {
    border: '1px solid #ccc',
    padding: '10px',
    margin: '10px',
    borderRadius: '5px',
    backgroundColor: course.status === 'completed' ? '#e6ffed' : (course.status === 'inprogress' ? '#fffbe6' : '#f0f2f5'),
  };

  return (
    <div style={nodeStyle}>
      <h4>{course.title}</h4>
      <p>ステータス: {course.status}</p>
      {/* TODO: クリックしたらコースのページに飛ぶようにする */}
      <a href={`/docs/${course.id}`}>学習を始める</a>
    </div>
  );
}

export default function LearningRoadmap() {
  return (
    <Layout title={roadmapData.title} description={roadmapData.description}>
      <div className="container margin-vert--lg">
        <div className="text--center">
          <h1>{roadmapData.title}</h1>
          <p>{roadmapData.description}</p>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          {/* TODO: D3.jsなどで、コース間の依存関係を線で結ぶ */}
          {roadmapData.courses.map(course => (
            <RoadmapNode key={course.id} course={course} />
          ))}
        </div>
      </div>
    </Layout>
  );
}
