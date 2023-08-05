# 什么是vue

[toc]

vue是前端的一种开发框架，它主要解决开发中的核心痛点——复杂的DOM制作

vue拥有以下特点
- 渐进式
- 组件化
- 响应式

vue的应用场景:
- 前台的部分页面
- 中后台的全部页面

https://unpkg.com/vue@3.2.37/dist/vue.global.js

# 注入

# 虚拟 DOM树


# 模板语法

## 内容

vue 中的元素内容使用 mustache 模板引擎进行解析

## 指令

指令会影响元素的渲染行为，指令始终以 v 开头

基础指令：

- v-for: 循环渲染元素
- v-once: 当数据改变时，赋值处的数据不会发生改变
- v-html: 设置元素的 innerHTML，该指令会导致元素的模板内容失效
- v-on: 注册事件
  - 该指令由于十分常用，因此提供了简写 `@`
  - 事件支持一些指令修饰符，如 `prevent`
  - 事件参数会自动传递
- v-bind: 绑定动态属性
  - 该指令由于十分常用，因此提供了简写 `:`
- v-show: 控制元素的可见度
- v-if, v-else-if, v-else: 控制元素生成
- v-model: 双向数据绑定，常用于表单元素
  - 该指令是 v-on 和 v-bind 的复合版


[Vite官方中文文档](https://cn.vitejs.dev/guide/#scaffolding-your-first-vite-project)
[Vue官方文档](https://staging-cn.vuejs.org/)