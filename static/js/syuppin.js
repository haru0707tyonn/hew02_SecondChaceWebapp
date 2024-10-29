// // 1. onchange属性に設定した関数
// function OutputImage(target)
// {
//     // 2. ファイル読み込みクラス
//     var reader = new FileReader();

//     // 3. 読み込みクラスの準備が終わった後、画像の情報を設定
//     reader.onload = function () {
//         $sample2 = $("#sample2");

//         // 4. Imageクラスを使ってdiv要素に画像のheightとwidthのサイズを設定
//         img = new Image();
//         img.src = this.result;
//         img.onload = function() {
//             $sample2.css("width", img.naturalWidth);
//             $sample2.css("height", img.naturalHeight);
//         }
//         // 5. backgroundスタイルを設定
//         $sample2.css("background", "url(" + this.result + ") center center / contain no-repeat");
//     }
//     // 6. 読み込んだ画像ファイルをURLに変換
//     reader.readAsDataURL(target.files[0]);
// }

// function OutputImage(target, callback) {
//     // 画像の最大許容枚数
//     var maxImages = 5;

//     // 現在の画像枚数を取得
//     var currentImageCount = $("#image-container .image-group").length;

//     if (currentImageCount >= maxImages) {
//         console.log("最大許容枚数を超えています。処理を中断します。");
//         alert("最大" + maxImages + "枚までしかアップロードできません。");
//         return;
//     }

//     // 2. ファイル読み込みクラス
//     var reader = new FileReader();

//     // 3. 読み込みクラスの準備が終わった後、画像の情報を設定
//     reader.onload = function () {
//         $sample2 = $("#sample2");

//         // 4. Imageクラスを使ってdiv要素に画像のheightとwidthのサイズを設定
//         img = new Image();
//         img.src = this.result;
//         img.onload = function() {
//             $sample2.css("width", img.naturalWidth);
//             $sample2.css("height", img.naturalHeight);
//         }
//         // 5. backgroundスタイルを設定
//         $sample2.css("background", "url(" + this.result + ") center center / contain no-repeat");
    
//         // コールバック関数を呼び出す
//         if (typeof callback === "function") {
//         callback();
//         }
//     }
//     // 6. 読み込んだ画像ファイルをURLに変換
//     reader.readAsDataURL(target.files[0]);
// }



// $(document).ready(function () {
//     var counter = 1;

//     $('#form').on('change', function (e) {
//         // OutputImage 関数の呼び出し
//         OutputImage(e.target);
//             var reader = new FileReader();

//             reader.onload = function (e) {
//                 var imgId = 'img' + counter;

//                 // 画像要素を作成
//                 var $image = $('<img>', {
//                     'id': imgId,
//                     'src': e.target.result,
//                     'class': 'uploaded-image',
//                 });

//                 // 画像要素を含むグループを作成
//                 var $group = $('<div>', {
//                     'class': 'image-group',
//                 }).append($image);

//                 // 削除ボタンを作成
//                 var $deleteBtn = $('<button>', {
//                     'class': 'delete-btn',
//                     'text': '削除',
//                 });

//                 // 拡大ボタンを作成
//                 var $zoomBtn = $('<button>', {
//                     'class': 'zoom-btn',
//                     'text': '拡大',
//                     'click': function () {
//                         alert('ここに拡大の設定をしてくだしあ');
//                     }
//                 });

//                 // ボタンを横並びに配置するための要素
//                 var $buttonContainer = $('<div>', {
//                     'class': 'button-container',
//                 }).append($deleteBtn, $zoomBtn);

//                 // 画像要素とボタン要素を追加
//                 $group.append($buttonContainer);
//                 $('#image-container').append($group);

//                 counter++;
//             }

//             reader.readAsDataURL(e.target.files[0]);
//     });





function OutputImage(target) {
    return new Promise(function(resolve, reject) {

        // ファイルが選択されていない場合
        if (!target.files || target.files.length === 0) {
            reject("画像が選択されていません。");
            return;
        }


        // 画像の最大許容枚数
        var maxImages = 5;

        // 現在の画像枚数を取得
        var currentImageCount = $("#image-container .image-group").length;

        if (currentImageCount >= maxImages) {
            console.log("最大許容枚数を超えています。処理を中断します。");
            alert("最大" + maxImages + "枚までしかアップロードできません。");
            reject("最大許容枚数を超えています。");
            return;
        }

        // ファイル読み込みクラス
        var reader = new FileReader();

        // 読み込みクラスの準備が終わった後、画像の情報を設定
        reader.onload = function () {
            $sample2 = $("#sample2");

            // Imageクラスを使ってdiv要素に画像のheightとwidthのサイズを設定
            img = new Image();
            img.src = this.result;
            img.onload = function() {
                $sample2.css("width", img.naturalWidth);
                $sample2.css("height", img.naturalHeight);
            }
            // backgroundスタイルを設定
            $sample2.css("background", "url(" + this.result + ") center center / contain no-repeat");

            // 処理が完了したことを通知
            console.log("画像の処理が完了しました。");
            resolve({
                result: "画像の処理が完了しました。",
                imgSrc: this.result // 画像のURLを追加
            });
        }

        // 読み込んだ画像ファイルをURLに変換
        reader.readAsDataURL(target.files[0]);
    });
}

// 画像のURLを保存するためのグローバル変数
var imgSrcList = [];

$(document).ready(function () {
    var counter = 1;

    $('#form').on('change', async function (e) {
        try {
            // OutputImage 関数の呼び出し
            const outputResult = await OutputImage(e.target);
    
            var imgId = 'img' + counter;
    
            // 画像要素を作成
            var $image = $('<img>', {
                'id': imgId,
                'src': outputResult.imgSrc, // 画像のURLを使用
                'class': 'uploaded-image',
            });
    
            // 画像要素を含むグループを作成
            var $group = $('<div>', {
                'class': 'image-group',
            }).append($image);
    
            // 削除ボタンを作成
            var $deleteBtn = $('<button>', {
                'class': 'delete-btn',
                'text': '削除',
            });
    
            // 拡大ボタンを作成
            var $zoomBtn = $('<button>', {
                'class': 'zoom-btn',
                'text': '拡大',
                'click': function () {
                    alert('ここに拡大の設定をしてくだしあ');
                }
            });
    
            // ボタンを横並びに配置するための要素
            var $buttonContainer = $('<div>', {
                'class': 'button-container',
            }).append($deleteBtn, $zoomBtn);
    
            // 画像要素とボタン要素を追加
            $group.append($buttonContainer);
            $('#image-container').append($group);
    
            // 画像のURLを配列に保存
            imgSrcList.push(outputResult.imgSrc);

            // 配列の中身をコンソールに出力
            console.log("画像のURLリスト: ", imgSrcList);
    
            counter++;
        } catch (error) {
            // エラーが発生した場合の処理
            console.error(error);
        }
    });
    
    });


        // 削除ボタンがクリックされた時の処理（イベント委譲）
        $('#image-container').on('click', '.delete-btn', function () {
            $(this).closest('.image-group').remove(); // Remove the closest .image-group
            alert('画像が削除されました');
        });












// $(document).ready(function () {
//     var counter = 1;

//     $('#form').on('change', function (e) {
//         var reader = new FileReader();

//         reader.onload = function (e) {
//             var imgId = 'img' + counter;
//             $('<img>', {
//                 'id': imgId,
//                 'src': e.target.result,
//                 'class': 'uploaded-image',
//             }).appendTo('#image-container');
//             $('<button>', {
//                 'class': 'delete-btn',
//                 'text': '削除',
//                 'click': function () {
//                     $('#' + imgId).remove();
//                     $('#delete-btn-' + imgId).remove();
//                     $('#zoom-btn-' + imgId).remove();
//                 }
//             }).appendTo('#image-container').attr('id', 'delete-btn-' + imgId);
//             $('<button>', {
//                 'class': 'zoom-btn',
//                 'text': '拡大',
//                 'click': function () {
//                     alert('画像を拡大します。');
//                 }
//             }).appendTo('#image-container').attr('id', 'zoom-btn-' + imgId);

//             counter++;
//         }

//         reader.readAsDataURL(e.target.files[0]);
//     });
// });

// $(document).ready(function () {
//     var counter = 1;

//     $('#form').on('change', function (e) {
//         var reader = new FileReader();

//         reader.onload = function (e) {
//             var imgId = 'img' + counter;

//             // 画像要素を作成
//             var $image = $('<img>', {
//                 'id': imgId,
//                 'src': e.target.result,
//                 'class': 'uploaded-image',
//             });

//             // 削除ボタンを作成
//             var $deleteBtn = $('<button>', {
//                 'class': 'delete-btn',
//                 'text': '削除',
//                 'click': function () {
//                     $image.remove();
//                     $group.remove();
//                 }
//             });

//             // 拡大ボタンを作成
//             var $zoomBtn = $('<button>', {
//                 'class': 'zoom-btn',
//                 'text': '拡大',
//                 'click': function () {
//                     alert('画像を拡大します。');
//                 }
//             });

//             // 画像、削除ボタン、拡大ボタンをそれぞれの要素に追加
//             var $group = $('<div>', {
//                 'class': 'image-group',
//             }).append($image);

//             // ボタンを横並びに配置するための要素
//             var $buttonContainer = $('<div>', {
//                 'class': 'button-container',
//             }).append($deleteBtn, $zoomBtn);

//             // 画像要素とボタン要素を追加
//             $('#image-container').append($group, $buttonContainer);

//             counter++;
//         }

//         reader.readAsDataURL(e.target.files[0]);
//     });
// });








