import React from 'react';
import Link from '@docusaurus/Link';
import clsx from 'clsx';

export default function ModuleCard({ module }) {
  return (
    <div className={clsx('col col--4 margin-bottom--lg')}>
      <div className="card">
        <div className="card__header">
          <h3>{module.title}</h3>
        </div>
        <div className="card__body">
          <p>{module.description}</p>
        </div>
        <div className="card__footer">
          <Link to={module.link} className="button button--primary button--block">
            学習を開始する
          </Link>
        </div>
      </div>
    </div>
  );
}
