<template>
  <div>
<div class="container">



  <el-row :gutter="30">
<el-col v-for="(post, index) in post_list" v-bind:key="index">
  <el-timeline  >
    <el-timeline-item :timestamp='post.timestamp' placement="top"
      type="primary"
      size="large">
      <el-card>
         <el-button type="success" plain>
              <router-link v-bind:to="{ name: 'PostDetail', params: { id: post.id }}" >
          {{post.author.name || post.author.username }}  发布了 {{post.title}}
        </router-link>

         </el-button>




      </el-card>
    </el-timeline-item>

  </el-timeline>
</el-col>
  <el-col class="viewmore">
            <a v-show="hasMore" class="tcolors-bg" href="javascript:void(0);" @click="addMoreFun" >点击加载更多</a>
            <a v-show="!hasMore" class="tcolors-bg" href="javascript:void(0);">暂无更多数据</a>
        </el-col>



</el-row>

</div>
     <wbc-footer></wbc-footer>
    </div>

</template>

<script>

  import footer from '../../components/Base/footer.vue'

    export default {
        name: "Time",


        data () {
    return {

    hasMore:true,
        next:"",
      messages: '',
          post_list:[],
    }
  },
components: { //定义组件

		'wbc-footer': footer
	},
    methods: {


        InitTime() {
            const path = `/api/time/`
            this.$axios.get(path)
                .then((response) => {

                    // let next = response.data.data.next
                    this.post_list = response.data.results

                    console.log(this.post_list)
                    console.log(response.data.next)
                    this.next = response.data.next
                    if (this.next){
                        this.hasMore = true

                    }
                    else {
                        this.hasMore=false
                    }

                })

        },

        addMoreFun(){
             this.$axios.get(this.next)
                .then((response) => {

                    // let next = response.data.data.next
                    this.post_list = this.post_list.concat(response.data.results)

                    this.next = response.data.next
                    if (this.next){
                        this.hasMore = true
                    }
                    else {
                        this.hasMore=false
                    }

                })
        }


    },

     created() { //生命周期函数
            // console.log(this.$route);

           this.InitTime()
        }

    }

</script>


