// main.js

function submitForm() {
    var konbiniCheckbox = document.getElementById('konbini');
    var creditCardCheckbox = document.getElementById('creditCard');

    var cardNumberInput = document.getElementsByName('Number')[0];
    console.log(cardNumberInput.value);
    
    console.log('konbini checked:', konbiniCheckbox.checked);
    console.log('creditCard checked:', creditCardCheckbox.checked)
  
    if ((konbiniCheckbox.checked || creditCardCheckbox.checked) && !(konbiniCheckbox.checked && creditCardCheckbox.checked)) {
      document.getElementById('kessai').submit();
    } else {
      alert('どちらかの決済方法を選択してください。');
    }
  }
  
// function onButtonClick() {
// check1 = document.form1.Checkbox1.checked;
// check2 = document.form1.Checkbox2.checked;
// check3 = document.form1.Checkbox3.checked;
// target = document.getElementById("output");
// if (check1 != true && check2 != true && check3 != true ) {
// target.innerHTML = "チェック項目がチェックされていません。";
// }