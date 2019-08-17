<!-- 赞赏模块 -->
<template>
    <div class="tRewardBox tcommonBox">
        <header>
            <h1>

                    赞赏
            </h1>
        </header>
        <section>
            <div class="">
                <img src="../../../static/img/timg.jpg" alt="" class="maxW" >
            </div>
            <h1>@赞赏说明：</h1>
            <p>
                我要变成太阳,热热的晒着你（*/∇＼*）
            </p>
            <p>如果我给你带来过欢乐，或者对你有所帮助，欢迎赞赏支持:)</p>

            <hr>
            <h1>@赞赏方式：</h1>
            <el-row   :gutter="30">
                <el-col  :span="12"   class="donate-item">
                    <div class="donate-tip">
                        <img src="../../../static/img/weixinzhifu.png" :onerror="1">
                        <span>微信扫一扫，向我赞赏</span>
                    </div>
                </el-col>

                <el-col :span="12"  class="donate-item">
                    <div class="donate-tip">
                        <img src="../../../static/img/zhifubaozhifu.jpg" :onerror="1">
                        <span>支付宝扫一扫，向我赞赏</span>
                    </div>
                </el-col>
            </el-row>

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
.tRewardBox section{
    padding-bottom:20px;
}
.tRewardBox section h1{
    margin: 10px 0;
    font-size: 25px;
    font-weight: 700;
    /*text-align: center;*/
    line-height: 30px;
}
.tRewardBox section p{
    margin:10px 0;
    line-height:24px;
}
.tRewardBox section hr{
    background: #ccc;
    margin-bottom: 30px;
}

.tRewardBox .donate-item{
    text-align: right;
    color:#44b549;

}
.tRewardBox .donate-item:last-child{
    text-align: left;
    color:#00a0e9;
}
.tRewardBox .donate-item img{
    width:100%;
    display: block;
    height:auto;
}
.tRewardBox .donate-item div{
    display: inline-block;
    width:150px;
    padding:0 6px;
    text-align: center;
    box-sizing: border-box;
}
.tRewardBox .donate-item div span{
    display: inline-block;
    width:100%;
    margin: 10px 0;
    text-align: center;
}
.tRewardBox .el-table__body-wrapper{
    overflow: hidden;
}
.el-table--enable-row-hover .el-table__body tr:hover>td{
    background: transparent;
}
</style>
