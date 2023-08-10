// 获取选择框和输入框容器的引用
const optionSelect = document.getElementById('optionSelect');
const inputContainer = document.getElementById('inputContainer');
const secondContainer = document.getElementById('secondContainer');

// 监听选择框的变化事件
optionSelect.addEventListener('change', function() {
  // 清空输入框容器中的内容
  inputContainer.innerHTML = '';
  secondContainer.innerHTML = '';
  // 根据选择的选项生成相应的输入框
  if (optionSelect.value === 'optionA') {
const selectContainer = document.createElement('div');

// 创建选项框A
const selectA = document.createElement('select');
selectA.id = 'start';
selectA.name = 'start';
selectA.className = 'form-control';
selectA.style.marginTop = '10px'; // 添加间隔
inputContainer.appendChild(selectA);

// 创建选项框B
const selectB = document.createElement('select');
selectB.id = 'end';
selectB.name = 'end';
selectB.className = 'form-control';
selectB.style.marginTop = '10px'; // 添加间隔
inputContainer.appendChild(selectB);

const locations = [
  '博学楼', '7号公寓', '图书馆', '恭温楼', '博远楼', '慎思楼', '诚明楼', '笃行楼', '6号公寓', '体育馆',
  '敏行楼', '博纳楼', '校二', '3，4号公寓', '西门', '琢玉讲堂', '三食堂', '南门', '北门', '乒羽馆',
  '青春广场', '行知楼', '二食堂', '澡堂', '赛欧公寓', '经贸广场'
];

// 添加选项框A的选项
for (let i = 0; i < locations.length; i++) {
  const option = document.createElement('option');
  option.value = locations[i];
  option.textContent = locations[i];
  selectA.appendChild(option);
}

// 监听选项框A的变化
selectA.addEventListener('change', () => {
  const selectedValue = selectA.value;

  // 清空选项框B的选项
  selectB.innerHTML = '';

  // 添加选项框B的选项，不包含选项框A的值
  for (let i = 0; i < locations.length; i++) {
    if (locations[i] !== selectedValue) {
      const option = document.createElement('option');
      option.value = locations[i];
      option.textContent = locations[i];
      selectB.appendChild(option);
    }
  }
});
    const submitBtn = document.createElement('button');
    submitBtn.type = 'submit';
    submitBtn.value = 'Submit';
    submitBtn.className = 'theme-btn';
    submitBtn.textContent = '提交';
    submitBtn.style.marginTop = '10px'; // 添加间隔
  inputContainer.appendChild(submitBtn);
  } else if (optionSelect.value === 'optionB') {
    // 创建验证码输入框
    const captchaInput = document.createElement('input');
    captchaInput.type = 'text';
    captchaInput.name = 'vcode';
    captchaInput.id = 'vcode'
    captchaInput.className = 'form-control'
    captchaInput.placeholder = '请输入验证码';
    captchaInput.style.marginBottom = '10px'; // 添加间隔

    // 创建提交按钮
    const submitBtn = document.createElement('button');
    submitBtn.type = 'submit';
    submitBtn.value = 'Submit';
    submitBtn.className = 'theme-btn';
    submitBtn.textContent = '提交';
    submitBtn.style.marginTop = '10px'; // 添加间隔

    // 添加验证码输入框和提交按钮到第二个容器
    secondContainer.appendChild(captchaInput);
    secondContainer.appendChild(submitBtn);
  }

});