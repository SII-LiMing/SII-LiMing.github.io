# Avatar Adjust Guide

这份文档专门说明：**如何调整网站左侧头像**。

当前头像相关的关键文件只有这几个：

- 头像配置：
  `/Users/syu/LiMing/lm.github.io/_config.yml`

- 当前网站实际使用的头像文件：
  `/Users/syu/LiMing/lm.github.io/images/profile.jpg`

- 你本机当前原始照片：
  `/Users/syu/LiMing/me.jpg`

- 头像样式控制：
  `/Users/syu/LiMing/lm.github.io/_sass/layout/_sidebar.scss`

---

## 1. 最重要的结论

**你平时只需要改这一张文件：**

`/Users/syu/LiMing/lm.github.io/images/profile.jpg`

网站左侧头像现在就是从这张图读出来的。  
也就是说：

- 想调整头像位置
- 想缩放
- 想多露一点头发
- 想多露一点衣领

最直接的方法就是：**重新裁一版 `profile.jpg` 覆盖它**。

---

## 2. 当前头像是怎么被加载的

在 `_config.yml` 里，当前配置是：

```yaml
author:
  avatar: "profile.jpg"
```

模板会自动去读取：

`/Users/syu/LiMing/lm.github.io/images/profile.jpg`

所以：

- 如果你只是想换图，不需要改 `_config.yml`
- 直接替换 `images/profile.jpg` 就行

只有当你想把头像文件改名，比如改成 `avatar_v2.jpg`，才需要同步改 `_config.yml`。

---

## 3. 最简单的调整方法：手动裁剪

这是最推荐的方法。

### 步骤

1. 打开原图：

`/Users/syu/LiMing/me.jpg`

2. 用任意图片工具裁成**正方形**

建议：

- 头顶不要留太多空白
- 下方保留一点领带或衣领
- 脸尽量位于中上位置，不要太靠下

3. 导出为：

`profile.jpg`

4. 覆盖到这里：

`/Users/syu/LiMing/lm.github.io/images/profile.jpg`

5. 提交并部署：

```bash
cd /Users/syu/LiMing/lm.github.io
git add images/profile.jpg
git commit -m "Adjust avatar"
git push origin main
```

---

## 4. 推荐裁剪原则

你这个站点左侧头像是**圆形显示**，所以正方形底图很重要。

建议按下面的原则裁：

- **优先保证脸在中间**
- **头顶空白略少一点**
- **下方保留少量西装/领带**
- **不要把头发边缘切太狠**
- **不要裁得太紧，否则圆形裁切后会显得局促**

一句话：

**宁可稍微多留一点肩膀，也不要让额头上面空太多。**

---

## 5. 如果你想继续用脚本裁图

你也可以用 Python/PIL 自己生成 `profile.jpg`。

示例：

```python
from PIL import Image

src = "/Users/syu/LiMing/me.jpg"
out = "/Users/syu/LiMing/lm.github.io/images/profile.jpg"

img = Image.open(src).convert("RGB")
w, h = img.size

# 这里手动调裁剪框
left = 0
top = 0
side = min(w, h)

crop = img.crop((left, top, left + side, top + side))
crop = crop.resize((720, 720), Image.Resampling.LANCZOS)
crop.save(out, quality=95)
```

你主要调这 3 个变量：

- `left`
- `top`
- `side`

含义：

- `left` 越大，裁剪框越往右
- `top` 越大，裁剪框越往下
- `side` 越小，等价于“放大人像”
- `side` 越大，等价于“缩小人像、保留更多背景”

---

## 6. 什么时候需要改 CSS

大多数情况下**不需要**改 CSS。

当前头像样式在：

`/Users/syu/LiMing/lm.github.io/_sass/layout/_sidebar.scss`

关键设置是：

```scss
.author__avatar img {
  max-width: 175px;
  border-radius: 50%;
}
```

这表示：

- 头像显示宽度最多 `175px`
- 会被裁成圆形

如果你只是觉得“头像里人物位置不对”，不要改 CSS，改图片本身就够了。

只有在你觉得：

- 头像显示太大
- 头像显示太小
- 圆形边框样式不喜欢

这种情况下才去改 `_sidebar.scss`。

---

## 7. 最常见的工作流

以后你自己调头像，最稳流程就是：

1. 改原图或重新裁剪
2. 覆盖：
   `/Users/syu/LiMing/lm.github.io/images/profile.jpg`
3. 提交部署：

```bash
cd /Users/syu/LiMing/lm.github.io
git add images/profile.jpg
git commit -m "Adjust avatar"
git push origin main
```

4. 强制刷新网页缓存看效果

---

## 8. 如果你想保留多个版本

你也可以这样做：

- `profile_v1.jpg`
- `profile_v2.jpg`
- `profile_v3.jpg`

最后确认要用哪一个时：

- 把它复制/改名成 `profile.jpg`

这样最不容易丢历史版本。
