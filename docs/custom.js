// docs/custom.js

document.addEventListener('DOMContentLoaded', function () {
    // ページ内のすべてのオートハイトIframeを処理
    const iframes = document.querySelectorAll('iframe.auto-height-iframe');

    iframes.forEach(iframe => {
        // Iframeがロードされたときに高さを調整
        iframe.onload = function () {
            try {
                // Iframe内部のドキュメントの高さを取得
                // 同一オリジンポリシーにより、異なるドメインのコンテンツでは動作しません
                const innerDoc = iframe.contentWindow.document.body;
                if (innerDoc) {
                    // スクロール高さを取得し、少し余裕を持たせる
                    const height = innerDoc.scrollHeight + 20; // 20pxは余白
                    iframe.style.height = height + 'px';
                }
            } catch (e) {
                console.warn('Cannot access iframe content due to same-origin policy:', e);
                // クロスオリジンポリシーによりアクセスできない場合、固定高さをフォールバックとして設定
                iframe.style.height = '400px'; // 例えばデフォルトの高さ
            }
        };

        // Iframeがすでにロードされている場合の初期調整
        // ブラウザによってはonloadが発火しない場合があるため、既にロード済みなら手動で実行
        if (iframe.contentWindow && iframe.contentWindow.document.readyState === 'complete') {
            iframe.onload();
        }
    });
});

// docs/js/custom.js

document.addEventListener('DOMContentLoaded', function () {
    const tooltips = document.querySelectorAll('.custom-tooltip');

    tooltips.forEach(tooltip => {
        tooltip.addEventListener('click', function (event) {
            event.stopPropagation(); // ドキュメントクリックでの非表示を防ぐため、イベント伝播を停止
            this.classList.toggle('is-clicked'); // 'is-clicked' クラスをトグル
        });
    });

    // ツールチップ以外の場所をクリックしたら、開いているツールチップを閉じる
    document.addEventListener('click', function (event) {
        tooltips.forEach(tooltip => {
            if (tooltip.classList.contains('is-clicked') && !tooltip.contains(event.target)) {
                tooltip.classList.remove('is-clicked');
            }
        });
    });
});