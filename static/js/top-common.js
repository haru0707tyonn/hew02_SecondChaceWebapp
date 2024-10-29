// 初回アクセスフラグをクッキーから取得
var access = $.cookie("access");

// モーダル1(出品・リクエスト)
if (!access) {
  flag1 = false;
  $.cookie("access", false);
} else {
  flag1 = false;
}

// モーダル1を表示
$(".modal-open-1").modaal({
  start_open: flag1,
  overlay_close: true,
  before_open: function () {
    $("html").css("overflow-y", "hidden");
  },
  after_close: function () {
    $("html").css("overflow-y", "scroll");
  },
  width: 400, // 幅を設定
  height: 400, // 高さを設定
});

// モーダル２(出品)
if (!access) {
  flag2 = false;
  $.cookie("access", false);
} else {
  flag2 = false;
}

// モーダル2を表示
$(".modal-open-2").modaal({
  start_open: flag2,
  overlay_close: true,
  before_open: function () {
    $("html").css("overflow-y", "hidden");
  },
  after_close: function () {
    $("html").css("overflow-y", "scroll");
  },
  width: 600, // 幅を設定
  height: 400, // 高さを設定
});
