// const lt = document.getElementById("lt");
// const gt = document.getElementById("gt");
// const carousel = document.querySelector(".carousel");
// const boxes = document.querySelectorAll(".box");
// let index = 0;

// function updatebtn() {
//   lt.classList.remove("hidden");
//   gt.classList.remove("hidden");

//   if (index === 0) {
//     lt.classList.add("hidden");
//   }

//   if (index === boxes.length - 1) {
//     gt.classList.add("hidden");
//   }
// }

// function moveBoxes() {
//   const boxWidth = boxes[0].getBoundingClientRect().width;
//   carousel.style.transform = `translateX(${-1 * boxWidth * index}px)`;
// }

// updatebtn();

// gt.addEventListener("click", () => {
//   index++;
//   updatebtn();
//   moveBoxes();
// });

// lt.addEventListener("click", () => {
//   index--;
//   updatebtn();
//   moveBoxes();
// });

// window.addEventListener("resize", () => {
//   moveBoxes();
// });

//初回のみモーダルをすぐ出す判定。flagがモーダル表示のstart_open後に代入される

// //モーダル表示
// $(".modal-open").modaal({
//   start_open: flag, // ページロード時に表示するか
//   overlay_close: true, //モーダル背景クリック時に閉じるか
//   before_open: function () {
//     // モーダルが開く前に行う動作
//     $("html").css("overflow-y", "hidden"); /*縦スクロールバーを出さない*/
//   },
//   after_close: function () {
//     // モーダルが閉じた後に行う動作
//     $("html").css("overflow-y", "scroll"); /*縦スクロールバーを出す*/
//   },
// });

// 初回アクセスフラグをクッキーから取得
var access = $.cookie("access");

// モーダルごとの初回表示フラグを設定

// モーダル1(出品・リクエスト)
if (!access) {
  flag1 = false;
  $.cookie("access", false);
} else {
  flag1 = false;
}

// モーダル２(プロフィール)
if (!access) {
  flag2 = false;
  $.cookie("access", false);
} else {
  flag2 = false;
}

// モーダル３(本人情報)
if (!access) {
  flag3 = false;
  $.cookie("access", false);
} else {
  flag3 = false;
}

// モーダル４(住所)
if (!access) {
  flag4 = false;
  $.cookie("access", false);
} else {
  flag4 = false;
}

// モーダル５(電話番号)
if (!access) {
  flag5 = false;
  $.cookie("access", false);
} else {
  flag5 = false;
}

// モーダル６(支払い方法)
if (!access) {
  flag6 = false;
  $.cookie("access", false);
} else {
  flag6 = false;
}

// モーダル７(通知方法)
if (!access) {
  flag7 = false;
  $.cookie("access", false);
} else {
  flag7 = false;
}

// モーダル8(鑑定について)
if (!access) {
  flag8 = false;
  $.cookie("access", false);
} else {
  flag8 = false;
}

// モーダル９(リクエスト機能について)
if (!access) {
  flag9 = false;
  $.cookie("access", false);
} else {
  flag9 = false;
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
  height: 606, // 高さを設定
});

// モーダル３を表示
$(".modal-open-3").modaal({
  start_open: flag3,
  overlay_close: true,
  before_open: function () {
    $("html").css("overflow-y", "hidden");
  },
  after_close: function () {
    $("html").css("overflow-y", "scroll");
  },
  width: 600, // 幅を設定
  height: 530, // 高さを設定
});

// モーダル４を表示
$(".modal-open-4").modaal({
  start_open: flag4,
  overlay_close: true,
  before_open: function () {
    $("html").css("overflow-y", "hidden");
  },
  after_close: function () {
    $("html").css("overflow-y", "scroll");
  },
  width: 600, // 幅を設定
  height: 510, // 高さを設定
});

// モーダル5を表示
$(".modal-open-5").modaal({
  start_open: flag5,
  overlay_close: true,
  before_open: function () {
    $("html").css("overflow-y", "hidden");
  },
  after_close: function () {
    $("html").css("overflow-y", "scroll");
  },
  width: 500, // 幅を設定
  height: 400, // 高さを設定
});

// モーダル6を表示
$(".modal-open-6").modaal({
  start_open: flag6,
  overlay_close: true,
  before_open: function () {
    $("html").css("overflow-y", "hidden");
  },
  after_close: function () {
    $("html").css("overflow-y", "scroll");
  },
  width: 600, // 幅を設定
  height: 600, // 高さを設定
});

// モーダル7を表示
$(".modal-open-7").modaal({
  start_open: flag7,
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

// モーダル8を表示
$(".modal-open-8").modaal({
  start_open: flag8,
  overlay_close: true,
  before_open: function () {
    $("html").css("overflow-y", "hidden");
  },
  after_close: function () {
    $("html").css("overflow-y", "scroll");
  },
  width: 600, // 幅を設定
  height: 350, // 高さを設定
});

// モーダル9を表示
$(".modal-open-9").modaal({
  start_open: flag9,
  overlay_close: true,
  before_open: function () {
    $("html").css("overflow-y", "hidden");
  },
  after_close: function () {
    $("html").css("overflow-y", "scroll");
  },
  width: 600, // 幅を設定
  height: 300, // 高さを設定
});

