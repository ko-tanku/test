document.addEventListener('DOMContentLoaded', function() {
    // Mermaid.jsの初期化
    if (typeof mermaid !== 'undefined') {
        mermaid.initialize({
            startOnLoad: true,
            theme: 'default',
            flowchart: {
                useMaxWidth: false,
                htmlLabels: true
            }
        });
    }

    // ツールチップの初期化
    const tooltips = document.querySelectorAll('.custom-tooltip');
    tooltips.forEach(tooltip => {
        const tooltipText = tooltip.getAttribute('data-tooltip');
        if (tooltipText) {
            const tooltipSpan = document.createElement('span');
            tooltipSpan.className = 'tooltiptext';
            tooltipSpan.textContent = tooltipText.replace(/&#10;/g, '\n');
            tooltip.appendChild(tooltipSpan);

            tooltip.addEventListener('mouseenter', function() {
                const rect = this.getBoundingClientRect();
                const spanRect = tooltipSpan.getBoundingClientRect();
                if (rect.top - spanRect.height < 0) {
                    tooltipSpan.style.bottom = 'auto';
                    tooltipSpan.style.top = '125%';
                } else {
                    tooltipSpan.style.top = 'auto';
                    tooltipSpan.style.bottom = '125%';
                }
            });
        }
    });

    // iframeの高さ自動調整
    function adjustIframeHeight() {
        const iframes = document.querySelectorAll('iframe.auto-height-iframe');
        iframes.forEach(iframe => {
            iframe.addEventListener('load', function() {
                try {
                    const body = this.contentWindow.document.body;
                    const html = this.contentWindow.document.documentElement;
                    const height = Math.max(body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight);
                    if (height > 150) { // 最小の高さを設定
                        this.style.height = height + 'px';
                    }
                } catch (e) {
                    console.error("iframeの高さ調整に失敗しました: ", e);
                }
            });
        });
    }

    adjustIframeHeight();
});