<!-- 关于我 -->
<template>
    <div class="tcommonBox">
        <header>
            <h1>

                    关于我

            </h1>
        </header>
        <section>
           非常喜欢这些文字
            <p >

                <img src="../../../static/img/me.jpg" alt="" class="aboutmeImg">
            </p>

            <p>
                欢迎来到阿T同学！我是yk，是一个黑色boy(太阳的小弟)，立志在后端的路上越走越远，喜欢Python，Go，...喜欢看书和压马路
            </p>
            <p>
                😍后端小萌新
            </p>
            <p>
               他们都说我有多动症😍其实就是闲不住，愿终究为生活所热爱。
            </p>
            <p>
                你说你总想着远方，总感觉有些迷茫，匆忙的路程，鞋子都换了几双。没有雨的日子里，静静思索着前方。曾把心装进盒子里，拿起来却没有力量。
              你总把梦说的很沉重，就像夜空没了月亮，你总要为自己点燃一把火炬，去照亮你未曾到过的地方---yk。
            </p>

          <p>
             感谢帮助我，陪伴我的人们,一起期待生活，不辜负，不怀疑，不犹豫.
          </p>
        </section>
    </div>
</template>

<script>
    export default {
        data() { //选项 / 数据
            return {

            }
        },
        methods: { //事件处理器

        },
        components: { //定义组件

        },
        created() { //生命周期函数

        }
    }
</script>

<style>
.aboutmeImg{
    max-width:100%;
    /*height:300px;*/
}
.tcommonBox p a{
    color:#01AAED!important;
}
.tcommonBox p a:hover{
    color:#48456d!important;
}
.tcommonBox p i{
    font-style: italic;
}
.tcommonBox p b{
    font-weight: bold;
}
</style>
