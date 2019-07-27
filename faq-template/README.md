## FAQ 
仅供内部使用，用于常见问题答疑。

## 如何使用
用你的鼠标点两下，就会了。

## 如何更新

感觉这个东西，会是个坑，大概率只有我来维护了吧。不过还是写一写如何更新FAQ。

**source** 文件夹只会存在一级子目录，比如：
```
.
├── account
│   └── demo.md
└── basic
    ├── 如何更换绑定手机.md
    ├── 测试图片展示.md
    └── this is a question.md

```
这些子目录会作为FAQ首页左侧分类大项存在，点击分类大项可以跳转到对应的锚点。
子目录内的文件为具体的FAQ解释，该文件格式有点严格，为
```
[question]
问题的描述
[answer]
吧啦吧啦具体的官方解答
```

举个例子：
```
[question]
测试下网页端效果
[answer]
点连接
<a href="http://mars.changba.com/">下载官方最新版本火星直播APP</a>
<br>
第一步：打开“我的”<br>
<img style="width:200px;height:auto;" src="http://aliimg.changbalive.com/photo/banner/WechatIMG240.jpeg" alt="测试图片">
第二步：点击“手机号”<br>
<img style="width:200px;height:auto;" src="http://aliimg.changbalive.com/photo/banner/WechatIMG241.jpeg" alt="测试图片">

第三步：吧啦吧啦吧啦吧啦 ...
```


最后用一个python脚本更新下即可。
```
python faq-generator
```

## reference
reference from [FAQ-template](https://github.com/CodyHouse/faq-template)

