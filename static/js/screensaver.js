// セットされた時間 (ミリ秒単位)
var idleTime = 10000; 

var screenSaverTimeout;

// マウスが移動したとき、またはキーボードが押されたときにセットされたタイマーをリセットする
function resetTimer() {
    clearTimeout(screenSaverTimeout);
    screenSaverTimeout = setTimeout(showScreenSaver, idleTime);
}

// スクリーンセーバーを表示する
function showScreenSaver() {
    document.getElementById('screenSaver').style.display = 'block';
    // クリック時にスクリーンセーバーを非表示にする
    document.addEventListener('click', hideScreenSaver);
}

// スクリーンセーバーを非表示にする
function hideScreenSaver() {
    document.getElementById('screenSaver').style.display = 'none';
    // 再度タイマーをリセットする
    resetTimer();
    // クリックイベントリスナーを削除する
    document.removeEventListener('click', hideScreenSaver);
}

// ページが読み込まれたときにタイマーをセットする
document.addEventListener('DOMContentLoaded', function () {
    resetTimer();
});

// マウスが動いたときにタイマーをリセットする
document.addEventListener('mousemove', resetTimer);

// キーボードが押されたときにタイマーをリセットする
document.addEventListener('keypress', resetTimer);