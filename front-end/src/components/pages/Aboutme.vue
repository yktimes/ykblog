<!-- 关于我 -->
<template>
    <div>

        <div class="container">
            <el-row  :gutter="30">
                <el-col :sm="30" :md="30" style="transition:all .5s ease-out;margin-bottom:30px;">
                    <wbc-about></wbc-about>

                </el-col>

            </el-row>
        </div>
        <wbc-footer></wbc-footer>
    </div>
</template>

<script>

import footer from '../../components/Base/footer.vue'
import temAbout from '../Base/temAbout.vue'

    export default {
        name: 'Aboutme',
        data() { //选项 / 数据
            return {

            }
        },
        methods: { //事件处理器

        },
        components: { //定义组件

            'wbc-about':temAbout,
            'wbc-footer':footer
        },
        created() { //生命周期函数


        }
    }
</script>

<style>

</style>
